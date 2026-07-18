import { v4 as uuidv4 } from "uuid";

export function getCorrelationId(
  headers: Record<string, string>
): string {
  const incoming = headers["x-correlation-id"];
  if (incoming && typeof incoming === "string" && incoming.length > 0) {
    return incoming;
  }
  return uuidv4();
}

export function addCorrelationHeader(
  response: { headers?: Record<string, string> },
  correlationId: string
): void {
  if (!response.headers) {
    response.headers = {};
  }
  response.headers["x-correlation-id"] = correlationId;
}
