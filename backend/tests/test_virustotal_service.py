from __future__ import annotations

import requests
import pytest

from backend.config import APISettings
from backend.services.virustotal_service import VirusTotalError, VirusTotalService


class FakeResponse:
    def __init__(self, status_code: int, payload: dict):
        self.status_code = status_code
        self.payload = payload

    def json(self):
        return self.payload


def test_valid_ip_lookup_normalizes_useful_fields():
    calls = []

    def fake_get(url, **kwargs):
        calls.append((url, kwargs))
        return FakeResponse(
            200,
            {
                "data": {
                    "attributes": {
                        "reputation": 12,
                        "country": "US",
                        "as_owner": "Example Networks",
                        "asn": 64500,
                        "last_analysis_date": 1700000000,
                        "last_analysis_stats": {"malicious": 2, "suspicious": 1, "harmless": 60, "undetected": 5},
                        "last_analysis_results": {
                            "engine-a": {"category": "malicious", "result": "Known threat"},
                            "engine-b": {"category": "harmless", "result": "Clean"},
                        },
                    }
                }
            },
        )

    service = VirusTotalService(APISettings(virustotal_api_key="test-key"), request_get=fake_get)
    result = service.lookup_ip("8.8.8.8")

    assert result["indicator"] == "8.8.8.8"
    assert result["indicator_type"] == "IP"
    assert result["malicious_count"] == 2
    assert result["suspicious_count"] == 1
    assert result["country"] == "US"
    assert result["organization"] == "Example Networks"
    assert result["detection_summary"] == "Known threat"
    assert calls[0][1]["headers"] == {"x-apikey": "test-key"}


@pytest.mark.parametrize(
    ("method_name", "indicator"),
    [("lookup_ip", "not-an-ip"), ("lookup_domain", "localhost"), ("lookup_hash", "1234")],
)
def test_invalid_indicators_are_rejected_before_request(method_name, indicator):
    service = VirusTotalService(APISettings(virustotal_api_key="test-key"), request_get=lambda *args, **kwargs: pytest.fail("request made"))

    with pytest.raises(VirusTotalError, match="Invalid"):
        getattr(service, method_name)(indicator)


def test_missing_api_key_is_reported_without_value_exposure():
    service = VirusTotalService(APISettings(), request_get=lambda *args, **kwargs: pytest.fail("request made"))

    with pytest.raises(VirusTotalError) as error:
        service.lookup_domain("example.com")

    assert str(error.value) == "VirusTotal API key is not configured."


@pytest.mark.parametrize("status_code", [401, 403, 429, 500])
def test_provider_errors_are_safely_mapped(status_code):
    service = VirusTotalService(
        APISettings(virustotal_api_key="test-key"),
        request_get=lambda *args, **kwargs: FakeResponse(status_code, {}),
    )

    with pytest.raises(VirusTotalError) as error:
        service.lookup_domain("example.com")

    assert "test-key" not in str(error.value)
    assert "VirusTotal" in str(error.value)
    expected_status = 429 if status_code == 429 else status_code if status_code in {401, 403} else 502
    assert error.value.status_code == expected_status


def test_not_found_response_is_handled():
    service = VirusTotalService(
        APISettings(virustotal_api_key="test-key"),
        request_get=lambda *args, **kwargs: FakeResponse(404, {}),
    )

    with pytest.raises(VirusTotalError, match="not found"):
        service.lookup_hash("a" * 64)


def test_network_failure_is_handled_without_internal_error():
    def failed_request(*args, **kwargs):
        raise requests.RequestException("private transport details")

    service = VirusTotalService(APISettings(virustotal_api_key="test-key"), request_get=failed_request)

    with pytest.raises(VirusTotalError) as error:
        service.lookup_ip("8.8.8.8")

    assert str(error.value) == "VirusTotal service is unavailable."
    assert "private transport details" not in str(error.value)


def test_virustotal_endpoint_requires_jwt(client):
    response = client.get("/api/v1/virustotal/ip/8.8.8.8")

    assert response.status_code == 401
