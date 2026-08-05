import type { FormEvent } from "react";
import { useEffect, useState } from "react";

import { getMyProfile, updateProfile, type ProfilePayload, type ProfileResponse } from "../services/profile";

const defaultAvatar = "https://ui-avatars.com/api/?name=CTID&background=0b1220&color=38bdf8&bold=true";

export default function ProfilePage() {
  const [profile, setProfile] = useState<ProfileResponse | null>(null);
  const [form, setForm] = useState<ProfilePayload | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    getMyProfile()
      .then((data) => {
        setProfile(data);
        setForm({
          full_name: data.full_name,
          username: data.username,
          college: data.college,
          course: data.course,
          organization: data.organization ?? "",
          country: data.country,
          bio: data.bio,
          avatar: data.avatar ?? null,
          preferred_theme: data.preferred_theme,
        });
      })
      .catch(() => undefined);
  }, []);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!form) return;
    try {
      const updated = await updateProfile(form);
      setProfile(updated);
      setMessage("Profile updated successfully.");
    } catch (submissionError) {
      setMessage(submissionError instanceof Error ? submissionError.message : "Unable to update profile.");
    }
  }

  if (!profile || !form) return null;

  return (
    <section className="content-panel profile-page-panel">
      <div className="profile-summary-header">
        <img className="profile-avatar-large" src={profile.avatar ?? defaultAvatar} alt="Profile avatar" />
        <div>
          <div className="eyebrow">Profile</div>
          <h2 className="section-title">{profile.full_name}</h2>
          <p className="section-copy">Manage your CTID identity and onboarding data from one place.</p>
        </div>
      </div>

      <div className="profile-meta-list">
        <span><strong>Email:</strong> {profile.email}</span>
        <span><strong>Username:</strong> {profile.username}</span>
        <span><strong>College:</strong> {profile.college}</span>
        <span><strong>Course:</strong> {profile.course}</span>
        <span><strong>Organization:</strong> {profile.organization || "N/A"}</span>
        <span><strong>Role:</strong> {profile.roles.join(", ")}</span>
        <span><strong>Member Since:</strong> {new Date(profile.member_since).toLocaleDateString()}</span>
      </div>

      <form onSubmit={handleSubmit} className="profile-form profile-edit-form">
        {message ? <div className="error-banner">{message}</div> : null}
        <div className="field"><label>Full Name</label><input value={form.full_name} onChange={(event) => setForm({ ...form, full_name: event.target.value })} /></div>
        <div className="field"><label>Username</label><input value={form.username} onChange={(event) => setForm({ ...form, username: event.target.value })} /></div>
        <div className="field"><label>College</label><input value={form.college} onChange={(event) => setForm({ ...form, college: event.target.value })} /></div>
        <div className="field"><label>Course</label><input value={form.course} onChange={(event) => setForm({ ...form, course: event.target.value })} /></div>
        <div className="field"><label>Organization</label><input value={form.organization ?? ""} onChange={(event) => setForm({ ...form, organization: event.target.value })} /></div>
        <div className="field"><label>Country</label><input value={form.country} onChange={(event) => setForm({ ...form, country: event.target.value })} /></div>
        <div className="field"><label>Bio</label><textarea rows={4} value={form.bio} onChange={(event) => setForm({ ...form, bio: event.target.value })} /></div>
        <div className="field"><label>Avatar Upload</label><input type="file" accept="image/*" onChange={async (event) => {
          const file = event.target.files?.[0];
          if (!file) return;
          const reader = new FileReader();
          reader.onload = () => {
            const value = typeof reader.result === "string" ? reader.result : null;
            setForm({ ...form, avatar: value });
            setProfile({ ...profile, avatar: value });
          };
          reader.readAsDataURL(file);
        }} /></div>
        <div className="field">
          <label>Preferred Theme</label>
          <select value={form.preferred_theme} onChange={(event) => setForm({ ...form, preferred_theme: event.target.value as ProfilePayload["preferred_theme"] })}>
            <option value="dark">Dark</option>
            <option value="light">Light</option>
            <option value="system">System</option>
          </select>
        </div>
        <button className="submit-button" type="submit">Save Changes</button>
      </form>
    </section>
  );
}
