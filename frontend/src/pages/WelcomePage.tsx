import { useNavigate } from "react-router-dom";

export default function WelcomePage() {
  const navigate = useNavigate();

  return (
    <main className="page-shell">
      <section className="page-grid single-column">
        <div className="hero-panel onboarding-panel">
          <div className="logo-mark">CTID</div>
          <div className="eyebrow">Welcome to CTID</div>
          <h1 className="hero-title">Complete your profile before entering the dashboard.</h1>
          <p className="hero-copy">
            CTID uses a short onboarding step to personalize analyst identity, avatar, and workspace preferences before
            you reach the main intelligence dashboard.
          </p>

          <div className="progress-track" aria-label="Onboarding progress">
            <div className="progress-fill" style={{ width: "35%" }} />
          </div>
          <div className="progress-text">Step 1 of 3: Welcome</div>

          <button className="submit-button onboarding-button" onClick={() => navigate("/profile/complete")}>Continue</button>
        </div>
      </section>
    </main>
  );
}
