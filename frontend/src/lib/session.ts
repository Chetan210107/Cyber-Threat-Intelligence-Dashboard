export type AuthTokens = {
  access_token: string;
  refresh_token: string;
};

const ACCESS_TOKEN_KEY = "ctid_access_token";
const REFRESH_TOKEN_KEY = "ctid_refresh_token";

export function saveTokens(tokens: AuthTokens): void {
  localStorage.setItem(ACCESS_TOKEN_KEY, tokens.access_token);
  localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh_token);
}

export function getAccessToken(): string | null {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function getRefreshToken(): string | null {
  return localStorage.getItem(REFRESH_TOKEN_KEY);
}

export function clearSession(): void {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
}

export function hasSession(): boolean {
  return getAccessToken() !== null;
}
