type LogLevel = "debug" | "info" | "warn" | "error";

interface LogEntry {
  timestamp: string;
  level: LogLevel;
  service: string;
  correlationId?: string;
  message: string;
  data?: Record<string, unknown>;
  error?: {
    name: string;
    message: string;
    stack?: string;
  };
}

class Logger {
  private service: string;

  constructor(service: string) {
    this.service = service;
  }

  private log(
    level: LogLevel,
    message: string,
    data?: Record<string, unknown>,
    correlationId?: string
  ): void {
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      service: this.service,
      message,
      ...(correlationId && { correlationId }),
      ...(data && { data }),
    };

    const output = JSON.stringify(entry);

    switch (level) {
      case "error":
        console.error(output);
        break;
      case "warn":
        console.warn(output);
        break;
      case "debug":
        console.debug(output);
        break;
      default:
        console.log(output);
    }
  }

  info(message: string, data?: Record<string, unknown>, correlationId?: string): void {
    this.log("info", message, data, correlationId);
  }

  warn(message: string, data?: Record<string, unknown>, correlationId?: string): void {
    this.log("warn", message, data, correlationId);
  }

  error(
    message: string,
    err?: Error,
    data?: Record<string, unknown>,
    correlationId?: string
  ): void {
    const errorData = err
      ? { ...data, error: { name: err.name, message: err.message, stack: err.stack } }
      : data;
    this.log("error", message, errorData, correlationId);
  }

  debug(message: string, data?: Record<string, unknown>, correlationId?: string): void {
    this.log("debug", message, data, correlationId);
  }
}

export function createLogger(service: string): Logger {
  return new Logger(service);
}
