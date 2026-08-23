from __future__ import annotations

import ipaddress
import re
from typing import Any, Callable

import requests

from backend.config import APISettings


class VirusTotalError(Exception):
    """Safe application error for VirusTotal lookup failures."""


class VirusTotalService:
    BASE_URL = "https://www.virustotal.com/api/v3"
    HASH_PATTERN = re.compile(r"^(?:[a-fA-F0-9]{32}|[a-fA-F0-9]{40}|[a-fA-F0-9]{64})$")
    DOMAIN_PATTERN = re.compile(
        r"^(?=.{1,253}$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}$"
    )

    def __init__(
        self,
        api_settings: APISettings | None = None,
        request_get: Callable[..., requests.Response] | None = None,
    ) -> None:
        self.api_settings = api_settings or APISettings.from_environment()
        self.request_get = request_get or requests.get

    def lookup_ip(self, indicator: str) -> dict[str, Any]:
        normalized = self._validate_ip(indicator)
        return self._lookup("ip_addresses", normalized, "IP")

    def lookup_domain(self, indicator: str) -> dict[str, Any]:
        normalized = self._validate_domain(indicator)
        return self._lookup("domains", normalized, "Domain")

    def lookup_hash(self, indicator: str) -> dict[str, Any]:
        normalized = self._validate_hash(indicator)
        return self._lookup("files", normalized, "File hash")

    def _lookup(self, resource: str, indicator: str, indicator_type: str) -> dict[str, Any]:
        if not self.api_settings.virustotal_api_key:
            raise VirusTotalError("VirusTotal API key is not configured.")

        try:
            response = self.request_get(
                f"{self.BASE_URL}/{resource}/{indicator}",
                headers={"x-apikey": self.api_settings.virustotal_api_key},
                timeout=10,
            )
        except requests.RequestException as error:
            raise VirusTotalError("VirusTotal service is unavailable.") from error

        if response.status_code == 404:
            raise VirusTotalError("Indicator was not found in VirusTotal.")
        if response.status_code in {401, 403}:
            raise VirusTotalError("VirusTotal API authentication failed.")
        if response.status_code >= 400:
            raise VirusTotalError("VirusTotal returned an API error.")

        try:
            payload = response.json()
        except ValueError as error:
            raise VirusTotalError("VirusTotal returned an invalid response.") from error

        return self._normalize(payload, indicator, indicator_type)

    @staticmethod
    def _normalize(payload: dict[str, Any], indicator: str, indicator_type: str) -> dict[str, Any]:
        data = payload.get("data") or {}
        attributes = data.get("attributes") or {}
        stats = attributes.get("last_analysis_stats") or {}
        results = attributes.get("last_analysis_results") or {}

        detection_names = [
            str(result.get("result"))
            for result in results.values()
            if isinstance(result, dict) and result.get("category") == "malicious" and result.get("result")
        ]
        network = attributes.get("network") or {}
        country = attributes.get("country") or network.get("country")
        organization = attributes.get("as_owner") or attributes.get("organization")
        asn = attributes.get("asn") or network.get("asn")
        last_analysis_date = attributes.get("last_analysis_date") or "N/A"

        return {
            "indicator": indicator,
            "indicator_type": indicator_type,
            "reputation": attributes.get("reputation", "N/A"),
            "malicious_count": stats.get("malicious", "N/A"),
            "suspicious_count": stats.get("suspicious", "N/A"),
            "harmless_count": stats.get("harmless", "N/A"),
            "undetected_count": stats.get("undetected", "N/A"),
            "last_analysis_date": last_analysis_date,
            "country": country or "N/A",
            "organization": organization or "N/A",
            "asn": asn or "N/A",
            "detection_summary": ", ".join(detection_names) if detection_names else "N/A",
        }

    @staticmethod
    def _validate_ip(indicator: str) -> str:
        try:
            return str(ipaddress.ip_address(indicator.strip()))
        except ValueError as error:
            raise VirusTotalError("Invalid IP address.") from error

    @classmethod
    def _validate_domain(cls, indicator: str) -> str:
        normalized = indicator.strip().lower().rstrip(".")
        if not cls.DOMAIN_PATTERN.fullmatch(normalized):
            raise VirusTotalError("Invalid domain.")
        return normalized

    @classmethod
    def _validate_hash(cls, indicator: str) -> str:
        normalized = indicator.strip().lower()
        if not cls.HASH_PATTERN.fullmatch(normalized):
            raise VirusTotalError("Invalid file hash.")
        return normalized
