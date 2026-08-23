import axios from "axios";
import type { FormEvent } from "react";
import { useState } from "react";

import { lookupVirusTotal, type VirusTotalIndicatorType, type VirusTotalResult } from "../services/virustotal";

const indicatorLabels: Record<VirusTotalIndicatorType, string> = {
  ip: "IP address",
  domain: "Domain",
  hash: "File hash",
};

function displayDate(value: number | string): string {
  if (typeof value !== "number") return value || "N/A";
  return new Date(value * 1000).toLocaleString();
}

export default function VirusTotalPage() {
  const [type, setType] = useState<VirusTotalIndicatorType>("ip");
  const [indicator, setIndicator] = useState("");
  const [result, setResult] = useState<VirusTotalResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!indicator.trim()) {
      setError(`Enter a ${indicatorLabels[type].toLowerCase()} to search.`);
      setResult(null);
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);
    try {
      setResult(await lookupVirusTotal(type, indicator.trim()));
    } catch (lookupError) {
      const message = axios.isAxiosError(lookupError)
        ? lookupError.response?.data?.message ?? "VirusTotal lookup failed."
        : lookupError instanceof Error
          ? lookupError.message
          : "VirusTotal lookup failed.";
      setError(message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="content-panel virustotal-page">
      <div>
        <div className="eyebrow">External Intelligence</div>
        <h2 className="section-title">VirusTotal</h2>
        <p className="section-copy">Review reputation and analysis information for an IP address, domain, or file hash.</p>
      </div>

      <form className="virustotal-search-form" onSubmit={handleSubmit}>
        <div className="field">
          <label htmlFor="indicator-type">Indicator type</label>
          <select id="indicator-type" value={type} onChange={(event) => setType(event.target.value as VirusTotalIndicatorType)}>
            <option value="ip">IP address</option>
            <option value="domain">Domain</option>
            <option value="hash">File hash</option>
          </select>
        </div>
        <div className="field virustotal-indicator-field">
          <label htmlFor="indicator">Indicator</label>
          <input id="indicator" value={indicator} onChange={(event) => setIndicator(event.target.value)} placeholder={`Enter ${indicatorLabels[type].toLowerCase()}`} />
        </div>
        <button className="submit-button virustotal-search-button" type="submit" disabled={loading}>
          {loading ? "Searching..." : "Search VirusTotal"}
        </button>
      </form>

      {error ? <div className="error-banner">{error}</div> : null}
      {!loading && !error && !result ? <div className="empty-state">Enter an indicator to view VirusTotal results.</div> : null}

      {result ? (
        <div className="virustotal-results">
          <div className="result-heading">
            <div>
              <div className="eyebrow">Result</div>
              <h3 className="result-indicator">{result.indicator}</h3>
            </div>
            <span className="result-type">{result.indicator_type}</span>
          </div>

          <div className="result-stat-grid">
            <div className="result-stat"><span>Reputation</span><strong>{result.reputation}</strong></div>
            <div className="result-stat"><span>Malicious</span><strong>{result.malicious_count}</strong></div>
            <div className="result-stat"><span>Suspicious</span><strong>{result.suspicious_count}</strong></div>
            <div className="result-stat"><span>Harmless</span><strong>{result.harmless_count}</strong></div>
            <div className="result-stat"><span>Undetected</span><strong>{result.undetected_count}</strong></div>
          </div>

          <dl className="result-detail-grid">
            <div><dt>Last analysis</dt><dd>{displayDate(result.last_analysis_date)}</dd></div>
            <div><dt>Country</dt><dd>{result.country}</dd></div>
            <div><dt>Organization</dt><dd>{result.organization}</dd></div>
            <div><dt>ASN</dt><dd>{result.asn}</dd></div>
            <div><dt>Detection summary</dt><dd>{result.detection_summary}</dd></div>
          </dl>
        </div>
      ) : null}
    </section>
  );
}
