import { RateLimitError } from "../common/errors";

interface RateLimitEntry {
  count: number;
  resetAt: number;
}

const store = new Map<string, RateLimitEntry>();

export interface RateLimitConfig {
  windowMs: number;
  maxRequests: number;
}

export function checkRateLimit(
  key: string,
  config: RateLimitConfig
): void {
  const now = Date.now();
  const entry = store.get(key);

  if (!entry || now > entry.resetAt) {
    store.set(key, { count: 1, resetAt: now + config.windowMs });
    return;
  }

  if (entry.count >= config.maxRequests) {
    const retryAfter = Math.ceil((entry.resetAt - now) / 1000);
    throw new RateLimitError(retryAfter);
  }

  entry.count++;
}

export function createRateLimiter(config: RateLimitConfig) {
  return (key: string): void => {
    checkRateLimit(key, config);
  };
}
