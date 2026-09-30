import { API_BASE_URL } from "../config/appConfig";

export class ApiError extends Error {
  constructor(message, status, data = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.data = data;
  }
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      ...(options.headers || {}),
    },
  });

  if (response.status === 204) {
    return null;
  }

  const contentType = response.headers.get("content-type") || "";
  let data = null;

  if (contentType.includes("application/json")) {
    data = await response.json();
  } else {
    const text = await response.text();
    data = text ? { detail: text } : null;
  }

  if (!response.ok) {
    const message =
      data?.detail ||
      data?.message ||
      `Request failed with status ${response.status}.`;

    throw new ApiError(message, response.status, data);
  }

  return data;
}

export function toAbsoluteMediaUrl(path) {
  if (!path) return null;
  if (/^https?:\/\//i.test(path)) return path;
  return `${API_BASE_URL}${path.startsWith("/") ? path : `/${path}`}`;
}

export const api = {
  health() {
    return request("/api/v1/health");
  },

  createInspection(file) {
    const formData = new FormData();
    formData.append("file", file);

    return request("/api/v1/inspections", {
      method: "POST",
      body: formData,
    });
  },

  listInspections({ limit = 20, offset = 0 } = {}) {
    const params = new URLSearchParams({
      limit: String(limit),
      offset: String(offset),
    });

    return request(`/api/v1/inspections?${params.toString()}`);
  },

  getInspection(id) {
    return request(`/api/v1/inspections/${id}`);
  },

  deleteInspection(id) {
    return request(`/api/v1/inspections/${id}`, {
      method: "DELETE",
    });
  },

  getAnalyticsSummary() {
    return request("/api/v1/analytics/summary");
  },

  getDamageDistribution() {
    return request("/api/v1/analytics/damage-distribution");
  },

  getModelInfo() {
    return request("/api/v1/model");
  },
};
