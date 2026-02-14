// This is the "main address" of your backend server.
// If you set VITE_API_BASE_URL in .env, it will use that.
// If not, it will use http://127.0.0.1:8000 by default.
export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

// This is a helper that sends requests to your backend.
// Think of it like: "go to this backend URL, ask for data, and return the answer".
export async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  // Send the request to the backend (like calling the backend through the internet)
  const res = await fetch(`${API_BASE_URL}${path}`, {
    // Tell the backend: "I am sending/receiving JSON data"
    headers: { "Content-Type": "application/json", ...(options?.headers || {}) },
    ...options,
  });

  // If the backend did NOT respond successfully (example: 400, 500 errors)
  if (!res.ok) {
    // Read the error message if the backend sent one
    const text = await res.text();
    // Stop and throw an error so the page can show an error message
    throw new Error(text || `Request failed: ${res.status}`);
  }

  // If backend returns "no content" (204), return null.
  // Otherwise, read the JSON response and return it.
  return res.status === 204 ? (null as T) : ((await res.json()) as T);
}