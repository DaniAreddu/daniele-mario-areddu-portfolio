import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import { adminApiFetch } from "@/admin/api/adminApiClient";
import type { AdminLoginResult, AdminUser } from "@/admin/types";

type AdminAuthStatus = "loading" | "signed-out" | "mfa-required" | "authenticated";

interface AdminAuthContextValue {
  status: AdminAuthStatus;
  user: AdminUser | null;
  login: (email: string, password: string) => Promise<AdminLoginResult>;
  verifyTotp: (code: string) => Promise<AdminLoginResult>;
  logout: () => Promise<void>;
  refresh: () => Promise<void>;
}

const AdminAuthContext = createContext<AdminAuthContextValue | null>(null);

export function AdminAuthProvider({ children }: { children: ReactNode }) {
  const [status, setStatus] = useState<AdminAuthStatus>("loading");
  const [user, setUser] = useState<AdminUser | null>(null);

  const refresh = useCallback(async () => {
    try {
      const me = await adminApiFetch<AdminUser>("/auth/me");
      setUser(me);
      setStatus("authenticated");
    } catch {
      setUser(null);
      setStatus("signed-out");
    }
  }, []);

  useEffect(() => {
    void refresh();
    // Only on mount: login()/verifyTotp() below call refresh() themselves
    // at the right point in the two-step flow — an automatic re-run here
    // would race with the deliberate "mfa-required" state.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const login = useCallback(
    async (email: string, password: string) => {
      const result = await adminApiFetch<AdminLoginResult>("/auth/login", {
        method: "POST",
        body: { email, password },
      });
      if (result.status === "mfa_required") {
        setStatus("mfa-required");
      } else {
        await refresh();
      }
      return result;
    },
    [refresh],
  );

  const verifyTotp = useCallback(
    async (code: string) => {
      const result = await adminApiFetch<AdminLoginResult>("/auth/totp/verify", {
        method: "POST",
        body: { code },
      });
      await refresh();
      return result;
    },
    [refresh],
  );

  const logout = useCallback(async () => {
    await adminApiFetch("/auth/logout", { method: "POST" });
    setUser(null);
    setStatus("signed-out");
  }, []);

  const value = useMemo(
    () => ({ status, user, login, verifyTotp, logout, refresh }),
    [status, user, login, verifyTotp, logout, refresh],
  );

  return <AdminAuthContext.Provider value={value}>{children}</AdminAuthContext.Provider>;
}

export function useAdminAuth(): AdminAuthContextValue {
  const context = useContext(AdminAuthContext);
  if (!context) {
    throw new Error("useAdminAuth must be used within an AdminAuthProvider");
  }
  return context;
}
