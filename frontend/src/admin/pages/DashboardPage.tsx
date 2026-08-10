import { useAdminAuth } from "@/admin/auth/AdminAuthContext";

export default function DashboardPage() {
  const { user } = useAdminAuth();

  return (
    <div>
      <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">Dashboard</p>
      <h1 className="mt-2 font-serif text-3xl text-ink">
        Welcome back{user ? `, ${user.email}` : ""}.
      </h1>
      <p className="mt-4 max-w-xl text-ink-soft">
        The full content dashboard (published/draft counts, upcoming appearances, recent
        activity) lands as each content module ships. For now, head to Security to set up
        two-factor authentication.
      </p>
    </div>
  );
}
