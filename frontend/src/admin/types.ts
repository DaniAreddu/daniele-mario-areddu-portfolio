export interface AdminUser {
  id: number;
  email: string;
  role: string;
  totp_enabled: boolean;
}

export interface AdminLoginResult {
  status: "mfa_required" | "authenticated";
}

export interface AdminTotpEnroll {
  secret: string;
  otpauth_uri: string;
  qr_data_uri: string;
}

export interface AdminRecoveryCodes {
  codes: string[];
}
