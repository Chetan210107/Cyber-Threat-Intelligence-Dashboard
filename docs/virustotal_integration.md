# VirusTotal Integration

## What VirusTotal Is

VirusTotal is an indicator intelligence service that aggregates security analysis from multiple sources. CTID uses it as a read-only enrichment service for analyst lookups.

## Supported Indicators

- IP addresses
- Domains
- File hashes using MD5, SHA-1, or SHA-256 formats

File upload, URL scanning, sandboxing, and automated analysis are outside this milestone.

## API Flow

1. An authenticated user selects an indicator type and enters an indicator.
2. The CTID frontend calls the protected internal endpoint.
3. The backend validates the indicator before making any provider request.
4. The backend sends the request to the matching VirusTotal v3 resource.
5. CTID normalizes reputation, analysis counts, network details, and detection names.
6. The frontend receives only the normalized result, never the raw provider response or API key.

## API Key Configuration

Add the key locally to `.env`:

```text
VIRUSTOTAL_API_KEY=your_virustotal_api_key
```

The key is loaded through the existing `APISettings` configuration layer. `.env` is ignored by Git and `.env.example` contains placeholders only.

## Security Considerations

- All CTID VirusTotal endpoints require JWT authentication.
- Input is validated before an external request is attempted.
- The API key is sent only from the backend to VirusTotal.
- Provider and network errors are mapped to safe application messages.
- Raw provider responses are not returned to the browser.
- Automated tests use mocked responses and never call VirusTotal.

## Current Limitations

- Lookups are synchronous and read-only.
- No caching, background jobs, or rate-limit queue is included.
- No file upload, URL scanning, malware sandbox, AI analysis, or SIEM integration is included.
- The frontend displays provider values as returned by the normalized service, using `N/A` when unavailable.
