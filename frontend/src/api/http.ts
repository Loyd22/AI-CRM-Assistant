// frontend/src/api/http.ts
// Purpose: central fetch wrapper that normalizes backend errors for the UI.
// Inputs: path, RequestInit options
// Output: typed response JSON (or null for 204)
// Side effects: throws Error with a clean message on non-2xx

export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

type FastApiValidationError = {
  detail?: Array<{
    loc?: (string | number)[];
    msg?: string;
    type?: string;
  }>;
};

type FastApiError = {
  detail?: string | any;
};

function buildErrorMessage(status: number, data: any, fallbackText: string) {
  // 422: FastAPI/Pydantic validation errors
  if (status === 422 && data?.detail && Array.isArray(data.detail)) {
    const first = data.detail[0];
    const field = first?.loc?.slice(-1)?.[0];
    const msg = first?.msg || "Validation error";
    return field ? `${String(field)}: ${msg}` : msg;
  }

  // detail can be string or object
  if (typeof data?.detail === "string") return data.detail;

  // if backend returns something else
  if (fallbackText) return fallbackText;

  return `Request failed (${status})`;
}

export async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });

  if (!res.ok) {
    const contentType = res.headers.get("content-type") || "";
    let data: FastApiError | FastApiValidationError | any = null;
    let text = "";

    try {
      if (contentType.includes("application/json")) data = await res.json();
      else text = await res.text();
    } catch {
      // ignore parse errors
    }

    const message = buildErrorMessage(res.status, data, text);
    throw new Error(message);
  }

  return res.status === 204 ? (null as T) : ((await res.json()) as T);
}