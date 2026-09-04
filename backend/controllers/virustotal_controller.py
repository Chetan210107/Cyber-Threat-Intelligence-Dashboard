from __future__ import annotations

from backend.services.virustotal_service import VirusTotalError, VirusTotalService
from backend.utils.responses import api_response


class VirusTotalController:
    def __init__(self, service: VirusTotalService | None = None) -> None:
        self.service = service or VirusTotalService()

    def lookup_ip(self, indicator: str) -> tuple[dict, int]:
        return self._lookup(self.service.lookup_ip, indicator)

    def lookup_domain(self, indicator: str) -> tuple[dict, int]:
        return self._lookup(self.service.lookup_domain, indicator)

    def lookup_hash(self, indicator: str) -> tuple[dict, int]:
        return self._lookup(self.service.lookup_hash, indicator)

    @staticmethod
    def _lookup(lookup, indicator: str) -> tuple[dict, int]:
        try:
            return api_response(True, "VirusTotal lookup completed.", lookup(indicator)), 200
        except VirusTotalError as error:
            return api_response(False, str(error)), error.status_code
