import { AuthError } from "../common/errors";

interface AuthenticatedRequest {
  headers: Record<string, string>;
  user?: {
    userId: string;
    email: string;
    role: string;
    permissions: string[];
  };
}

export function authenticate(
  req: AuthenticatedRequest
): AuthenticatedRequest["user"] {
  const authHeader = req.headers["authorization"];

  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    throw new AuthError("Missing or invalid authorization header");
  }

  const token = authHeader.slice(7);

  try {
    const payload = JSON.parse(
      Buffer.from(token.split(".")[1], "base64url").toString()
    );

    const user = {
      userId: payload.sub || payload.user_id,
      email: payload.email,
      role: payload.role || "viewer",
      permissions: payload.permissions || [],
    };

    req.user = user;
    return user;
  } catch {
    throw new AuthError("Invalid token");
  }
}

export function requireRole(...roles: string[]) {
  return (req: AuthenticatedRequest): void => {
    authenticate(req);

    if (!req.user) {
      throw new AuthError("Authentication required");
    }

    if (req.user.role !== "admin" && !roles.includes(req.user.role)) {
      throw new AuthError(
        `Access denied. Required role: ${roles.join(" or ")}`
      );
    }
  };
}
