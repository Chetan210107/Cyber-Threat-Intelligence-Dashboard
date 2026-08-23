from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class APISettings:
    """Environment-backed settings for future external intelligence services."""

    nvd_api_key: str | None = None
    virustotal_api_key: str | None = None
    abuseipdb_api_key: str | None = None

    @classmethod
    def from_environment(cls, environ: Mapping[str, str] | None = None) -> "APISettings":
        source = environ if environ is not None else os.environ
        return cls(
            nvd_api_key=source.get("NVD_API_KEY") or None,
            virustotal_api_key=source.get("VIRUSTOTAL_API_KEY") or None,
            abuseipdb_api_key=source.get("ABUSEIPDB_API_KEY") or None,
        )

    def missing_keys(self) -> tuple[str, ...]:
        missing: list[str] = []
        if not self.nvd_api_key:
            missing.append("NVD_API_KEY")
        if not self.virustotal_api_key:
            missing.append("VIRUSTOTAL_API_KEY")
        if not self.abuseipdb_api_key:
            missing.append("ABUSEIPDB_API_KEY")
        return tuple(missing)

    def validate(self, require_all: bool = False) -> None:
        """Validate configuration without ever including secret values in errors."""
        missing = self.missing_keys()
        if require_all and missing:
            raise RuntimeError("Missing required external API credentials: " + ", ".join(missing))


API_SETTINGS = APISettings.from_environment()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "ctid-development-secret-key-change-me-please")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///ctid.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "ctid-development-jwt-secret-key-change-me-please")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "900"))
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", "2592000"))
    JSON_SORT_KEYS = False
    API_SETTINGS = API_SETTINGS


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_ACCESS_TOKEN_EXPIRES = 60
    JWT_REFRESH_TOKEN_EXPIRES = 3600


class ProductionConfig(Config):
    DEBUG = False
