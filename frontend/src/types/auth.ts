export type AuthUser = {
  id: number;
  email: string;
  full_name: string;
  roles: string[];
  mfa_enabled: boolean;
  is_active: boolean;
};

export type AuthResponse = {
  success: boolean;
  message: string;
  data?: {
    user: AuthUser;
    profile_completed: boolean;
    access_token: string;
    refresh_token: string;
    token_type: string;
    expires_in: number;
  };
};
