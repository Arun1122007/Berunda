import { AppError } from "../common/errors";
import { createLogger } from "../common/logger";
import { error as errorResponse } from "../common/response";

const logger = createLogger("error-handler");

export interface ErrorHandlerContext {
  correlationId?: string;
  functionName: string;
}

export function handleError(
  err: Error,
  context: ErrorHandlerContext
): {
  statusCode: number;
  body: Record<string, unknown>;
} {
  if (err instanceof AppError) {
    logger.warn(
      `AppError: ${err.code} — ${err.message}`,
      { statusCode: err.statusCode, code: err.code },
      context.correlationId
    );

    return {
      statusCode: err.statusCode,
      body: errorResponse(
        err.code,
        err.message,
        err.details,
        context.correlationId
      ),
    };
  }

  logger.error(
    `Unhandled error in ${context.functionName}: ${err.message}`,
    err,
    {},
    context.correlationId
  );

  return {
    statusCode: 500,
    body: errorResponse(
      "INTERNAL_ERROR",
      "An unexpected error occurred. Please try again later.",
      undefined,
      context.correlationId
    ),
  };
}
