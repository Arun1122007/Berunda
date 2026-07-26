import { apiClient } from "./api-client";
import type { User, AuthResponse } from "@/types/api";

const TOKEN_KEY = "auth_token";
const REFRESH_TOKEN_KEY = "refresh_token";
const USER_KEY = "current_user";

export class AuthService {
  async login(email: string, password: string): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>("/auth/login", {
      email,
      password,
    });
    this.setTokens(response);
    return response;
  }

  async demoLogin(): Promise<AuthResponse> {
    const payload = btoa(JSON.stringify({ sub: 1, exp: Math.floor(Date.now() / 1000) + 86400, role: "admin" }));
    const response: AuthResponse = {
      token: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.${payload}.demo`,
      refreshToken: `demo_refresh_${Date.now()}`,
      expiresIn: 86400,
      user: {
        userId: 1,
        email: "admin@berunda.gov",
        name: "Demo Admin",
        role: "admin",
        district: "Bengaluru Urban",
        permissions: ["read", "write", "admin"],
      },
    };
    this.setTokens(response);
    return response;
  }

  async logout(): Promise<void> {
    try {
      await apiClient.post("/auth/logout");
    } catch {
      // Ignore logout API errors
    }
    this.clearTokens();
  }

  async refreshToken(): Promise<AuthResponse> {
    const refreshToken = sessionStorage.getItem(REFRESH_TOKEN_KEY);
    if (!refreshToken) {
      throw new Error("No refresh token available");
    }
    const response = await apiClient.post<AuthResponse>("/auth/refresh", {
      refreshToken,
    });
    this.setTokens(response);
    return response;
  }

  async getCurrentUser(): Promise<User | null> {
    const cached = sessionStorage.getItem(USER_KEY);
    if (cached) {
      return JSON.parse(cached);
    }
    try {
      const user = await apiClient.get<User>("/auth/me");
      sessionStorage.setItem(USER_KEY, JSON.stringify(user));
      return user;
    } catch {
      return null;
    }
  }

  getToken(): string | null {
    return sessionStorage.getItem(TOKEN_KEY);
  }

  isAuthenticated(): boolean {
    const token = this.getToken();
    if (!token) return false;
    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
      return payload.exp * 1000 > Date.now();
    } catch {
      return false;
    }
  }

  private setTokens(response: AuthResponse): void {
    sessionStorage.setItem(TOKEN_KEY, response.token);
    sessionStorage.setItem(REFRESH_TOKEN_KEY, response.refreshToken);
    sessionStorage.setItem(USER_KEY, JSON.stringify(response.user));
  }

  private clearTokens(): void {
    sessionStorage.removeItem(TOKEN_KEY);
    sessionStorage.removeItem(REFRESH_TOKEN_KEY);
    sessionStorage.removeItem(USER_KEY);
  }
}

export const authService = new AuthService();
