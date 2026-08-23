# External API Configuration Foundation

The backend now provides one reusable `APISettings` configuration object for the future NVD, VirusTotal, and AbuseIPDB services.

## Local Configuration

1. Copy `.env.example` to `.env`.
2. Add provider credentials to the matching environment variables.
3. Keep `.env` local and never commit it.

Expected variables:

```text
NVD_API_KEY=
VIRUSTOTAL_API_KEY=
ABUSEIPDB_API_KEY=
```

The values are loaded with `python-dotenv` and are available through `Config.API_SETTINGS`. Missing credentials can be checked with `API_SETTINGS.missing_keys()` or enforced with `API_SETTINGS.validate(require_all=True)` by a future integration service.

Validation errors contain only variable names. Credential values are never returned, logged, or included in test output. This milestone does not make external requests.
