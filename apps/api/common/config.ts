interface Config {
  orgId: string;
  projectId: string;
  environment: string;
  catalystAuthEndpoint: string;
  catalystDataStoreEndpoint: string;
  catalystQuickmlEndpoint: string;
  logLevel: string;
  rateLimitWindowMs: number;
  rateLimitMaxRequests: number;
  jwtSecret: string;
}

const requiredVars: string[] = [
  "CATALYST_ORG_ID",
  "CATALYST_PROJECT_ID",
  "CATALYST_AUTH_ENDPOINT",
  "JWT_SECRET",
];

function getEnv(key: string, fallback?: string): string {
  const value = process.env[key] || fallback;
  if (value === undefined) {
    throw new Error(`Missing required environment variable: ${key}`);
  }
  return value;
}

let configInstance: Config | null = null;

export function loadConfig(): Config {
  if (configInstance) return configInstance;

  for (const v of requiredVars) {
    getEnv(v);
  }

  configInstance = {
    orgId: getEnv("CATALYST_ORG_ID"),
    projectId: getEnv("CATALYST_PROJECT_ID"),
    environment: getEnv("CATALYST_ENVIRONMENT", "Development"),
    catalystAuthEndpoint: getEnv("CATALYST_AUTH_ENDPOINT"),
    catalystDataStoreEndpoint: getEnv(
      "CATALYST_DATASTORE_ENDPOINT",
      "https://datastore.catalyst.zoho.com"
    ),
    catalystQuickmlEndpoint: getEnv(
      "CATALYST_QUICKML_ENDPOINT",
      "https://quickml.catalyst.zoho.com"
    ),
    logLevel: getEnv("LOG_LEVEL", "info"),
    rateLimitWindowMs: parseInt(getEnv("RATE_LIMIT_WINDOW_MS", "60000"), 10),
    rateLimitMaxRequests: parseInt(
      getEnv("RATE_LIMIT_MAX_REQUESTS", "100"),
      10
    ),
    jwtSecret: getEnv("JWT_SECRET"),
  };

  return configInstance;
}
