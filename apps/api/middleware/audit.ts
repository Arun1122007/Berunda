import { createLogger } from "../common/logger";

const logger = createLogger("audit");

interface AuditEvent {
  action: string;
  resource: string;
  resourceId: string;
  userId: string;
  details: Record<string, unknown>;
  correlationId?: string;
}

export function logAuditEvent(event: AuditEvent): void {
  logger.info(
    `Audit: ${event.action} on ${event.resource}:${event.resourceId} by ${event.userId}`,
    {
      action: event.action,
      resource: event.resource,
      resourceId: event.resourceId,
      userId: event.userId,
      details: event.details,
    },
    event.correlationId
  );
}
