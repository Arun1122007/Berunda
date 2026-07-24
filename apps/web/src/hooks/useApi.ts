import { useState, useEffect, useCallback } from "react";
import { apiClient, ApiError } from "@/services/api-client";

interface UseQueryState<T> {
  data: T | null;
  isLoading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export function useQuery<T>(
  endpoint: string,
  options?: { enabled?: boolean; params?: Record<string, string> }
): UseQueryState<T> {
  const [data, setData] = useState<T | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await apiClient.get<T>(endpoint, {
        params: options?.params,
      });
      setData(result);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError("An unexpected error occurred");
      }
    } finally {
      setIsLoading(false);
    }
  }, [endpoint, JSON.stringify(options?.params)]);

  useEffect(() => {
    if (options?.enabled === false) {
      setIsLoading(false);
      return;
    }
    fetchData();
  }, [fetchData, options?.enabled]);

  return { data, isLoading, error, refetch: fetchData };
}

interface UseMutationState<T> {
  isLoading: boolean;
  error: string | null;
  mutate: (body?: unknown) => Promise<T | null>;
  reset: () => void;
}

export function useMutation<T>(
  endpoint: string,
  method: "POST" | "PUT" | "DELETE" = "POST"
): UseMutationState<T> {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const mutate = useCallback(
    async (body?: unknown): Promise<T | null> => {
      setIsLoading(true);
      setError(null);
      try {
        let result: T | null = null;
        if (method === "POST") {
          result = await apiClient.post<T>(endpoint, body);
        } else if (method === "PUT") {
          result = await apiClient.put<T>(endpoint, body);
        } else if (method === "DELETE") {
          result = await apiClient.delete<T>(endpoint);
        }
        return result;
      } catch (err) {
        if (err instanceof ApiError) {
          setError(err.message);
        } else {
          setError("An unexpected error occurred");
        }
        return null;
      } finally {
        setIsLoading(false);
      }
    },
    [endpoint, method]
  );

  const reset = useCallback(() => {
    setError(null);
    setIsLoading(false);
  }, []);

  return { isLoading, error, mutate, reset };
}
