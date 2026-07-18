import { useState, useEffect, useCallback } from "react";
import { authService } from "@/services/auth";
import type { User } from "@/types/api";

interface UseAuthReturn {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

export function useAuth(): UseAuthReturn {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const init = async () => {
      try {
        if (authService.isAuthenticated()) {
          const currentUser = await authService.getCurrentUser();
          setUser(currentUser);
        }
      } catch {
        setError("Failed to restore session");
      } finally {
        setIsLoading(false);
      }
    };
    init();
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await authService.login(email, password);
      setUser(response.user);
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Login failed";
      setError(message);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const logout = useCallback(async () => {
    setIsLoading(true);
    try {
      await authService.logout();
      setUser(null);
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Logout failed";
      setError(message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  return {
    user,
    isAuthenticated: authService.isAuthenticated(),
    isLoading,
    error,
    login,
    logout,
  };
}
