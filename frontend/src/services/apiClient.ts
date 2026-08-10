import type { ApiErrorBody } from "@/types/api";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "/api/v1";

export class ApiError extends Error {
  code: string;
  status: number;
  details?: unknown;

  constructor(status: number, code: string, message: string, details?: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

interface RequestOptions {
  lang?: string;
  params?: Record<string, string | number | boolean | undefined>;
  method?: "GET" | "POST";
  body?: unknown;
}

export async function apiFetch<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { lang, params, method = "GET", body } = options;

  const url = new URL(`${API_BASE_URL}${path}`, window.location.origin);
  if (lang) url.searchParams.set("lang", lang);
  if (params) {
    for (const [key, value] of Object.entries(params)) {
      if (value !== undefined && value !== "") url.searchParams.set(key, String(value));
    }
  }

  const response = await fetch(url.toString().replace(window.location.origin, ""), {
    method,
    headers: body ? { "Content-Type": "application/json" } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    let errorBody: ApiErrorBody | null = null;
    try {
      errorBody = (await response.json()) as ApiErrorBody;
    } catch {
      // Response had no JSON body; fall through to a generic error.
    }
    throw new ApiError(
      response.status,
      errorBody?.error.code ?? "unknown_error",
      errorBody?.error.message ?? "Something went wrong. Please try again.",
      errorBody?.error.details,
    );
  }

  return (await response.json()) as T;
}
