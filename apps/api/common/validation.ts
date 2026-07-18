import { ValidationError } from "./errors";

interface ValidationRule {
  field: string;
  type: "string" | "number" | "boolean" | "object" | "array";
  required?: boolean;
  min?: number;
  max?: number;
  pattern?: RegExp;
  enum?: string[];
  message?: string;
}

export function validateSchema(
  data: Record<string, unknown>,
  rules: ValidationRule[]
): void {
  const errors: Record<string, string> = {};

  for (const rule of rules) {
    const value = data[rule.field];

    if (rule.required && (value === undefined || value === null)) {
      errors[rule.field] = rule.message || `${rule.field} is required`;
      continue;
    }

    if (value === undefined || value === null) continue;

    if (typeof value !== rule.type) {
      errors[rule.field] =
        rule.message || `${rule.field} must be of type ${rule.type}`;
      continue;
    }

    if (rule.type === "string") {
      const str = value as string;
      if (rule.min !== undefined && str.length < rule.min) {
        errors[rule.field] =
          rule.message || `${rule.field} must be at least ${rule.min} characters`;
      }
      if (rule.max !== undefined && str.length > rule.max) {
        errors[rule.field] =
          rule.message || `${rule.field} must be at most ${rule.max} characters`;
      }
      if (rule.pattern && !rule.pattern.test(str)) {
        errors[rule.field] =
          rule.message || `${rule.field} format is invalid`;
      }
      if (rule.enum && !rule.enum.includes(str)) {
        errors[rule.field] =
          rule.message || `${rule.field} must be one of: ${rule.enum.join(", ")}`;
      }
    }

    if (rule.type === "number") {
      const num = value as number;
      if (rule.min !== undefined && num < rule.min) {
        errors[rule.field] =
          rule.message || `${rule.field} must be at least ${rule.min}`;
      }
      if (rule.max !== undefined && num > rule.max) {
        errors[rule.field] =
          rule.message || `${rule.field} must be at most ${rule.max}`;
      }
    }
  }

  if (Object.keys(errors).length > 0) {
    throw new ValidationError("Validation failed", { fields: errors });
  }
}
