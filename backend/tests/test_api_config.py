from __future__ import annotations

import pytest

from backend.config import APISettings


def test_api_settings_load_environment_variables():
    settings = APISettings.from_environment(
        {
            "NVD_API_KEY": "nvd-test-secret",
            "VIRUSTOTAL_API_KEY": "vt-test-secret",
            "ABUSEIPDB_API_KEY": "abuse-test-secret",
        }
    )

    assert settings.nvd_api_key == "nvd-test-secret"
    assert settings.virustotal_api_key == "vt-test-secret"
    assert settings.abuseipdb_api_key == "abuse-test-secret"
    assert settings.missing_keys() == ()


def test_missing_api_keys_are_reported_by_name_only():
    settings = APISettings.from_environment({"NVD_API_KEY": "nvd-test-secret"})

    assert settings.missing_keys() == ("VIRUSTOTAL_API_KEY", "ABUSEIPDB_API_KEY")


def test_required_configuration_validation_does_not_expose_secret_values():
    settings = APISettings.from_environment({"NVD_API_KEY": "do-not-expose-this-secret"})

    with pytest.raises(RuntimeError) as error:
        settings.validate(require_all=True)

    message = str(error.value)
    assert "VIRUSTOTAL_API_KEY" in message
    assert "ABUSEIPDB_API_KEY" in message
    assert "do-not-expose-this-secret" not in message


def test_optional_validation_allows_local_startup_without_credentials():
    settings = APISettings.from_environment({})

    settings.validate()
    assert len(settings.missing_keys()) == 3
