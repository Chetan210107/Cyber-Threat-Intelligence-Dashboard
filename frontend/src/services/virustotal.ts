import { api } from "./api";

export type VirusTotalIndicatorType = "ip" | "domain" | "hash";

export type VirusTotalResult = {
  indicator: string;
  indicator_type: string;
  reputation: number | string;
  malicious_count: number | string;
  suspicious_count: number | string;
  harmless_count: number | string;
  undetected_count: number | string;
  last_analysis_date: number | string;
  country: string;
  organization: string;
  asn: number | string;
  detection_summary: string;
};

export async function lookupVirusTotal(type: VirusTotalIndicatorType, indicator: string): Promise<VirusTotalResult> {
  const response = await api.get<{ success: boolean; message: string; data?: VirusTotalResult }>(
    `/virustotal/${type}/${encodeURIComponent(indicator)}`,
  );
  if (!response.data.data) {
    throw new Error(response.data.message || "VirusTotal lookup failed.");
  }
  return response.data.data;
}
