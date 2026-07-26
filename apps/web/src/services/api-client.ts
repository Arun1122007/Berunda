const BASE_URL: string =
  (import.meta as Record<string, any>).env?.VITE_API_BASE_URL ||
  (import.meta as Record<string, any>).env?.VITE_API_URL ||
  "/api/v1";

interface RequestConfig extends RequestInit {
  params?: Record<string, string>;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    config: RequestConfig = {}
  ): Promise<T> {
    const token = sessionStorage.getItem("auth_token");
    const correlationId = crypto.randomUUID();

    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      "X-Correlation-ID": correlationId,
      ...(config.headers as Record<string, string>),
    };

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    let url = `${this.baseUrl}${endpoint}`;
    if (config.params) {
      const params = new URLSearchParams(config.params);
      url += `?${params.toString()}`;
    }

    const response = await fetch(url, {
      ...config,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new ApiError(
        error.message || `Request failed with status ${response.status}`,
        response.status,
        correlationId
      );
    }

    return response.json();
  }

  get<T>(endpoint: string, config?: RequestConfig): Promise<T> {
    return this.request<T>(endpoint, { ...config, method: "GET" });
  }

  post<T>(endpoint: string, body?: unknown, config?: RequestConfig): Promise<T> {
    return this.request<T>(endpoint, {
      ...config,
      method: "POST",
      body: body ? JSON.stringify(body) : undefined,
    });
  }

  put<T>(endpoint: string, body?: unknown, config?: RequestConfig): Promise<T> {
    return this.request<T>(endpoint, {
      ...config,
      method: "PUT",
      body: body ? JSON.stringify(body) : undefined,
    });
  }

  delete<T>(endpoint: string, config?: RequestConfig): Promise<T> {
    return this.request<T>(endpoint, { ...config, method: "DELETE" });
  }

  upload<T>(endpoint: string, formData: FormData): Promise<T> {
    const token = sessionStorage.getItem("auth_token");
    const headers: Record<string, string> = {};
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }
    return this.request<T>(endpoint, {
      method: "POST",
      body: formData,
      headers,
    });
  }

  uploadWithProgress<T>(endpoint: string, formData: FormData, onProgress?: (pct: number) => void): Promise<T> {
    return new Promise((resolve, reject) => {
      const token = sessionStorage.getItem("auth_token");
      const xhr = new XMLHttpRequest();
      xhr.open("POST", `${this.baseUrl}${endpoint}`);
      if (token) xhr.setRequestHeader("Authorization", `Bearer ${token}`);
      xhr.responseType = "json";

      if (onProgress && xhr.upload) {
        xhr.upload.addEventListener("progress", (e) => {
          if (e.lengthComputable) onProgress(Math.round((e.loaded / e.total) * 100));
        });
      }

      xhr.onload = () => {
        if (xhr.status >= 200 && xhr.status < 300) resolve(xhr.response);
        else reject(new ApiError(xhr.response?.detail || `Upload failed (${xhr.status})`, xhr.status, ""));
      };
      xhr.onerror = () => reject(new ApiError("Network error during upload", 0, ""));
      xhr.send(formData);
    });
  }
}

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public correlationId: string
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export const apiClient = new ApiClient(BASE_URL);
