import type { FormEvent } from "react";
import { useMemo, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

import { saveTokens } from "../lib/session";
import { login, register } from "../services/auth";

type Mode = "login" | "register";

export default function AuthPage() {
  const navigate = useNavigate();
  const [mode, setMode] = useState<Mode>("login");
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const headline = useMemo(
    () => (mode === "login" ? "Threat-ready access for SOC operators." : "Provision a secure CTID workspace account."),
    [mode],
  );

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      if (mode === "login") {
        const response = await login({ email, password });
        const profileCompleted = Boolean(response.data?.profile_completed);
        saveTokens({
          access_token: response.data?.access_token ?? "",
          refresh_token: response.data?.refresh_token ?? "",
        });
        navigate(profileCompleted ? "/dashboard" : "/welcome", { replace: true });
      } else {
        const response = await register({ email, password, full_name: fullName });
        saveTokens({
          access_token: response.data?.access_token ?? "",
          refresh_token: response.data?.refresh_token ?? "",
        });
        navigate("/welcome", { replace: true });
      }
    } catch (submissionError) {
      if (axios.isAxiosError(submissionError)) {
        const backendMessage = submissionError.response?.data?.message;
        setError(
          backendMessage ??
            `Unable to reach the authentication service at ${import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:5000/api/v1"}`,
        );
      } else {
        setError(submissionError instanceof Error ? submissionError.message : "Authentication failed.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="auth-shell">
      <section className="auth-grid">
        <aside className="hero-panel">
          <div className="eyebrow">Cyber Threat Intelligence Dashboard</div>
          <h1 className="hero-title">{headline}</h1>
          <p className="hero-copy">
            CTID is shaped for analysts who need fast, secure access to threat intelligence workflows, with a security-first
            authentication surface and an enterprise control model underneath.
          </p>

          <div className="signal-grid" aria-label="Authentication security signals">
            <div className="signal-card">
              <span className="signal-label">Access policy</span>
              <span className="signal-value">RBAC</span>
            </div>
            <div className="signal-card">
              <span className="signal-label">Session type</span>
              <span className="signal-value">JWT</span>
            </div>
            <div className="signal-card">
              <span className="signal-label">Audit mode</span>
              <span className="signal-value">On</span>
            </div>
          </div>
        </aside>

        <section className="form-panel">
          <div className="tab-bar" role="tablist" aria-label="Authentication mode">
            <button
              type="button"
              className={`tab-button ${mode === "login" ? "is-active" : ""}`}
              onClick={() => setMode("login")}
            >
              Sign in
            </button>
            <button
              type="button"
              className={`tab-button ${mode === "register" ? "is-active" : ""}`}
              onClick={() => setMode("register")}
            >
              Register
            </button>
          </div>

          <form onSubmit={handleSubmit}>
            {error ? <div className="error-banner">{error}</div> : null}

            {mode === "register" ? (
              <div className="field">
                <label htmlFor="full-name">Full name</label>
                <input
                  id="full-name"
                  name="full_name"
                  value={fullName}
                  onChange={(event) => setFullName(event.target.value)}
                  placeholder="Alex Morgan"
                  autoComplete="name"
                />
              </div>
            ) : null}

            <div className="field">
              <label htmlFor="email">Work email</label>
              <input
                id="email"
                name="email"
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="analyst@company.com"
                autoComplete="email"
              />
            </div>

            <div className="field">
              <label htmlFor="password">Password</label>
              <div className="password-row">
                <input
                  id="password"
                  name="password"
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  placeholder="Enter your secure password"
                  autoComplete={mode === "login" ? "current-password" : "new-password"}
                />
                <button type="button" className="toggle-button" onClick={() => setShowPassword((visible) => !visible)}>
                  {showPassword ? "Hide" : "Show"}
                </button>
              </div>
            </div>

            <button className="submit-button" type="submit" disabled={loading}>
              {loading ? "Processing..." : mode === "login" ? "Sign in to CTID" : "Create secure account"}
            </button>
          </form>

          <div className="support-row">
            <span>Session policy: short-lived access, rotated refresh tokens.</span>
            <a href="#security-review">Security review</a>
          </div>
        </section>
      </section>
    </main>
  );
}
