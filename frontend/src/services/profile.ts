import { api } from "./api";

export type ProfilePayload = {
  full_name: string;
  username: string;
  college: string;
  course: string;
  organization?: string | null;
  country: string;
  bio: string;
  avatar?: string | null;
  preferred_theme: "dark" | "light" | "system";
};

export type ProfileResponse = {
  id: number;
  user_id: number;
  full_name: string;
  username: string;
  college: string;
  course: string;
  organization?: string | null;
  country: string;
  bio: string;
  avatar?: string | null;
  preferred_theme: "dark" | "light" | "system";
  email: string;
  roles: string[];
  member_since: string;
};

export async function getMyProfile(): Promise<ProfileResponse> {
  const response = await api.get<{ success: boolean; message: string; data?: ProfileResponse }>("/profile/me");
  if (!response.data.data) {
    throw new Error("Profile not found.");
  }
  return response.data.data;
}

export async function createProfile(payload: ProfilePayload): Promise<ProfileResponse> {
  const response = await api.post<{ success: boolean; message: string; data?: ProfileResponse }>("/profile/me", payload);
  if (!response.data.data) {
    throw new Error("Profile creation failed.");
  }
  return response.data.data;
}

export async function updateProfile(payload: ProfilePayload): Promise<ProfileResponse> {
  const response = await api.put<{ success: boolean; message: string; data?: ProfileResponse }>("/profile/me", payload);
  if (!response.data.data) {
    throw new Error("Profile update failed.");
  }
  return response.data.data;
}

export async function checkUsernameAvailability(username: string): Promise<boolean> {
  const response = await api.get<{ success: boolean; message: string; data?: { available: boolean } }>(
    "/profile/username-availability",
    { params: { username } },
  );
  return Boolean(response.data.data?.available);
}
