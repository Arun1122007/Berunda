export class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number = 500,
    public code: string = "INTERNAL_ERROR",
    public details?: Record<string, unknown>
  ) {
    super(message);
    this.name = this.constructor.name;
  }

  toJSON(): Record<string, unknown> {
    return {
      error: {
        code: this.code,
        message: this.message,
        statusCode: this.statusCode,
        details: this.details,
      },
    };
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string, id?: string) {
    super(
      id ? `${resource} with id '${id}' not found` : `${resource} not found`,
      404,
      "NOT_FOUND"
    );
  }
}

export class ValidationError extends AppError {
  constructor(message: string, details?: Record<string, unknown>) {
    super(message, 400, "VALIDATION_ERROR", details);
  }
}

export class AuthError extends AppError {
  constructor(message: string = "Authentication required") {
    super(message, 401, "AUTH_ERROR");
  }
}

export class RateLimitError extends AppError {
  constructor(retryAfter: number = 60) {
    super(
      "Too many requests. Please try again later.",
      429,
      "RATE_LIMIT_ERROR",
      { retryAfter }
    );
  }
}
