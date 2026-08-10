import type { ApiErrorBody } from "@/types/api";

// Every admin request goes through the same Nginx gateway as the public
// API (see docs/architecture.md) — this is a same-origin path, not a
// separate host, which is what makes the SameSite=Strict session cookie
// work at all.
const ADMIN_API_BASE_URL = `${import.meta.env.VITE_API_BASE_URL ?? "/api/v1"}/admin`;

export class AdminApiError extends Error {
  code: string;
  status: number;
  details?: unknown;

  constructor(status: number, code: string, message: string, details?: unknown) {
    super(message);
    this.name = "AdminApiError";
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

interface AdminRequestOptions {
  method?: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  body?: unknown;
}

export async function adminApiFetch<T>(
  path: string,
  options: AdminRequestOptions = {},
): Promise<T> {
  const { method = "GET", body } = options;
  const isMutating = method !== "GET";

  const headers: Record<string, string> = {};
  if (body !== undefined) headers["Content-Type"] = "application/json";
  // Cheap CSRF defense-in-depth alongside the SameSite=Strict session
  // cookie — see backend app/api/deps.py::require_admin_spa_header.
  if (isMutating) headers["X-Requested-With"] = "admin-spa";

  const response = await fetch(`${ADMIN_API_BASE_URL}${path}`, {
    method,
    credentials: "include",
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    let errorBody: ApiErrorBody | null = null;
    try {
      errorBody = (await response.json()) as ApiErrorBody;
    } catch {
      // Response had no JSON body; fall through to a generic error.
    }
    throw new AdminApiError(
      response.status,
      errorBody?.error.code ?? "unknown_error",
      errorBody?.error.message ?? "Something went wrong. Please try again.",
      errorBody?.error.details,
    );
  }

  if (response.status === 204) {
    return undefined as T;
  }
  return (await response.json()) as T;
}
