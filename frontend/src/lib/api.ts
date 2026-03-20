const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

// ── Auth ─────────────────────────────────────────────────

export async function register(email: string, password: string, fullName: string) {
  const res = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password, full_name: fullName }),
  });
  if (!res.ok) throw new Error((await res.json()).detail || "Registration failed");
  return res.json();
}

export async function login(email: string, password: string) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) throw new Error((await res.json()).detail || "Login failed");
  return res.json();
}

// ── Jobs ─────────────────────────────────────────────────

export async function fetchJobs(params?: {
  location?: string;
  role?: string;
  experience_level?: string;
  posted_within_hours?: number;
  skip?: number;
  limit?: number;
}) {
  const query = new URLSearchParams();
  if (params?.location) query.set("location", params.location);
  if (params?.role) query.set("role", params.role);
  if (params?.experience_level) query.set("experience_level", params.experience_level);
  if (params?.posted_within_hours) query.set("posted_within_hours", String(params.posted_within_hours));
  if (params?.skip) query.set("skip", String(params.skip));
  if (params?.limit) query.set("limit", String(params.limit));

  const res = await fetch(`${API_BASE}/jobs?${query.toString()}`);
  if (!res.ok) throw new Error("Failed to fetch jobs");
  return res.json();
}

export async function fetchJobById(id: number) {
  const res = await fetch(`${API_BASE}/jobs/${id}`);
  if (!res.ok) throw new Error("Failed to fetch job");
  return res.json();
}

// ── Resume ───────────────────────────────────────────────

export async function uploadResume(file: File, token: string) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/resume/upload`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: formData,
  });
  if (!res.ok) throw new Error((await res.json()).detail || "Upload failed");
  return res.json();
}

// ── Recommendations ──────────────────────────────────────

export async function fetchRecommendations(token: string, topK: number = 10) {
  const res = await fetch(`${API_BASE}/recommendations?top_k=${topK}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Failed to fetch recommendations");
  return res.json();
}

export async function askQuestion(question: string, token: string) {
  const res = await fetch(`${API_BASE}/recommendations/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ question }),
  });
  if (!res.ok) throw new Error("Failed to get answer");
  return res.json();
}
