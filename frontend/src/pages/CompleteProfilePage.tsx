import type { ChangeEvent, FormEvent } from "react";
import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import { checkUsernameAvailability, createProfile, getMyProfile, type ProfilePayload } from "../services/profile";

const defaultAvatar = "https://ui-avatars.com/api/?name=CTID&background=0b1220&color=38bdf8&bold=true";

type FieldErrors = Partial<Record<keyof ProfilePayload, string>> & { general?: string };

const emptyProfile: ProfilePayload = {
  full_name: "",
  username: "",
  college: "",
  course: "",
  organization: "",
  country: "",
  bio: "",
  avatar: null,
  preferred_theme: "dark",
};

export default function CompleteProfilePage() {
  const navigate = useNavigate();
  const [form, setForm] = useState<ProfilePayload>(emptyProfile);
  const [avatarPreview, setAvatarPreview] = useState<string | null>(null);
  const [usernameStatus, setUsernameStatus] = useState<string>("Enter a username to check availability.");
  const [errors, setErrors] = useState<FieldErrors>({});
  const [loading, setLoading] = useState(false);
  const [checkingUsername, setCheckingUsername] = useState(false);

  useEffect(() => {
    getMyProfile()
      .then(() => navigate("/dashboard", { replace: true }))
      .catch(() => undefined);
  }, [navigate]);

  useEffect(() => {
    if (form.username.trim().length < 3) {
      setUsernameStatus("Username must be at least 3 characters.");
      return undefined;
    }

    setCheckingUsername(true);
    const timeoutId = window.setTimeout(() => {
      checkUsernameAvailability(form.username)
        .then((available) => {
          setUsernameStatus(available ? "Available" : "Already taken");
        })
        .catch(() => setUsernameStatus("Unable to check availability right now."))
        .finally(() => setCheckingUsername(false));
    }, 350);

    return () => window.clearTimeout(timeoutId);
  }, [form.username]);

  const isUsernameAvailable = useMemo(() => usernameStatus === "Available", [usernameStatus]);

  function updateField<K extends keyof ProfilePayload>(field: K, value: ProfilePayload[K]) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  function validate(): boolean {
    const nextErrors: FieldErrors = {};
    if (form.full_name.trim().length < 2) nextErrors.full_name = "Full name is required.";
    if (form.username.trim().length < 3) nextErrors.username = "Username is required.";
    if (form.college.trim().length < 2) nextErrors.college = "College is required.";
    if (form.course.trim().length < 2) nextErrors.course = "Course is required.";
    if (form.country.trim().length < 2) nextErrors.country = "Country is required.";
    if (form.bio.trim().length < 10) nextErrors.bio = "Bio must be at least 10 characters.";
    if (!isUsernameAvailable) nextErrors.username = "Username is already taken.";
    setErrors(nextErrors);
    return Object.keys(nextErrors).length === 0;
  }

  async function handleAvatarChange(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) {
      updateField("avatar", null);
      setAvatarPreview(null);
      return;
    }

    const reader = new FileReader();
    reader.onload = () => {
      const result = typeof reader.result === "string" ? reader.result : null;
      setAvatarPreview(result);
      updateField("avatar", result);
    };
    reader.readAsDataURL(file);
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setErrors({});
    if (!validate()) return;

    setLoading(true);
    try {
      await createProfile(form);
      navigate("/dashboard", { replace: true });
    } catch (submissionError) {
      setErrors({ general: submissionError instanceof Error ? submissionError.message : "Unable to save profile." });
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page-shell">
      <section className="page-grid onboarding-grid">
        <div className="hero-panel onboarding-panel">
          <div className="eyebrow">Complete Profile</div>
          <h1 className="hero-title">Tell CTID who you are.</h1>
          <p className="hero-copy">
            Fill in your analyst identity so the dashboard can personalize reports, profile cards, and future SOC views.
          </p>

          <div className="progress-track"><div className="progress-fill" style={{ width: "68%" }} /></div>
          <div className="progress-text">Step 2 of 3: Profile</div>

          <div className="avatar-preview-wrap">
            <img className="avatar-preview" src={avatarPreview ?? defaultAvatar} alt="Avatar preview" />
          </div>
        </div>

        <div className="form-panel">
          <form onSubmit={handleSubmit} className="profile-form">
            {errors.general ? <div className="error-banner">{errors.general}</div> : null}

            <div className="field"><label>Full Name</label><input value={form.full_name} onChange={(event) => updateField("full_name", event.target.value)} /><span className="field-error">{errors.full_name}</span></div>
            <div className="field">
              <label>Username</label>
              <input value={form.username} onChange={(event) => updateField("username", event.target.value)} />
              <div className={`inline-status ${isUsernameAvailable ? "status-ok" : "status-warn"}`}>
                {checkingUsername ? "Checking..." : usernameStatus}
              </div>
              <span className="field-error">{errors.username}</span>
            </div>
            <div className="field"><label>College</label><input value={form.college} onChange={(event) => updateField("college", event.target.value)} /><span className="field-error">{errors.college}</span></div>
            <div className="field"><label>Course</label><input value={form.course} onChange={(event) => updateField("course", event.target.value)} /><span className="field-error">{errors.course}</span></div>
            <div className="field"><label>Organization (optional)</label><input value={form.organization ?? ""} onChange={(event) => updateField("organization", event.target.value)} /></div>
            <div className="field"><label>Country</label><input value={form.country} onChange={(event) => updateField("country", event.target.value)} /><span className="field-error">{errors.country}</span></div>
            <div className="field"><label>Bio</label><textarea value={form.bio} onChange={(event) => updateField("bio", event.target.value)} rows={4} /><span className="field-error">{errors.bio}</span></div>
            <div className="field">
              <label>Avatar Upload</label>
              <input type="file" accept="image/*" onChange={handleAvatarChange} />
            </div>
            <div className="field">
              <label>Preferred Theme</label>
              <select value={form.preferred_theme} onChange={(event) => updateField("preferred_theme", event.target.value as ProfilePayload["preferred_theme"]) }>
                <option value="dark">Dark</option>
                <option value="light">Light</option>
                <option value="system">System</option>
              </select>
            </div>
            <button className="submit-button" type="submit" disabled={loading}>{loading ? "Saving..." : "Save Profile"}</button>
          </form>
        </div>
      </section>
    </main>
  );
}
