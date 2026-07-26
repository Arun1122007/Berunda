import { User } from '../types/api';

/**
 * Validates if the given user has permission to create a new FIR.
 */
export function canCreateFir(user: User | null): boolean {
  if (!user) return false;
  return ['officer', 'supervisor', 'admin'].includes(user.role);
}

/**
 * Validates if the given user has permission to edit an existing FIR.
 */
export function canEditFir(user: User | null, firAssignedToId?: string): boolean {
  if (!user) return false;
  if (user.role === 'supervisor' || user.role === 'admin') return true;
  if (user.role === 'officer' && firAssignedToId === user.id) return true;
  return false;
}

/**
 * Validates if the given user has permission to upload a document to an FIR.
 */
export function canUploadEvidence(user: User | null, firAssignedToId?: string): boolean {
  return canEditFir(user, firAssignedToId);
}

/**
 * Validates if the given user has permission to review AI suggestions.
 */
export function canReviewAi(user: User | null): boolean {
  if (!user) return false;
  return ['officer', 'supervisor'].includes(user.role);
}

/**
 * Validates if the user has access to administration views.
 */
export function canAccessAdministration(user: User | null): boolean {
  if (!user) return false;
  return user.role === 'admin';
}

/**
 * Validates if the user can view audit logs.
 */
export function canViewAudit(user: User | null): boolean {
  if (!user) return false;
  return ['supervisor', 'admin'].includes(user.role);
}
