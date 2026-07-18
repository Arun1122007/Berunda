export interface ApiSuccessResponse<T> {
  success: true;
  data: T;
  meta?: Record<string, unknown>;
  correlationId?: string;
}

export interface ApiErrorResponse {
  success: false;
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
  };
  correlationId?: string;
}

export function success<T>(
  data: T,
  meta?: Record<string, unknown>,
  correlationId?: string
): ApiSuccessResponse<T> {
  return {
    success: true,
    data,
    ...(meta && { meta }),
    ...(correlationId && { correlationId }),
  };
}

export function error(
  code: string,
  message: string,
  details?: Record<string, unknown>,
  correlationId?: string
): ApiErrorResponse {
  return {
    success: false,
    error: { code, message, ...(details && { details }) },
    ...(correlationId && { correlationId }),
  };
}

export interface PaginationMeta {
  page: number;
  pageSize: number;
  total: number;
  totalPages: number;
}

export function paginated<T>(
  data: T[],
  pagination: PaginationMeta,
  correlationId?: string
): ApiSuccessResponse<T[]> {
  return success(data, { pagination }, correlationId);
}
