// ── Auth ──
export interface User {
  userId: number;
  email: string;
  name: string;
  role: string;
  district?: string;
  policeStation?: string;
  permissions: string[];
}

export interface AuthResponse {
  token: string;
  refreshToken: string;
  expiresIn: number;
  user: User;
}

// ── FIR / Cases ──
export interface Case {
  caseMasterId: number;
  crimeNo: string;
  caseNo?: string;
  crimeRegisteredDate?: string;
  policeStationId?: number;
  caseStatusId?: number;
  crimeMajorHeadId?: number;
  crimeMinorHeadId?: number;
  incidentFromDate?: string;
  incidentToDate?: string;
  latitude?: number;
  longitude?: number;
  briefFacts?: string;
}

export interface CaseListResponse {
  items: Case[];
  total: number;
  page: number;
  pageSize: number;
}

export interface CaseDetail extends Case {
  complainants: Record<string, unknown>[];
  victims: Record<string, unknown>[];
  accused: Record<string, unknown>[];
  actSections: Record<string, unknown>[];
}

// ── Person / Entity ──
export interface PersonEntity {
  personEntityId: number;
  canonicalName: string;
  dob?: string;
  gender?: string;
  primaryDistrictId?: number;
  riskScoreId?: number;
  createdAt?: string;
  updatedAt?: string;
}

export interface PersonEntityLink {
  personEntityLinkId: number;
  personEntityId: number;
  sourceTable?: string;
  sourceRecordId?: number;
  caseMasterId?: number;
  confidence?: number;
  isReviewed?: number;
}

// ── Graph ──
export interface GraphNode {
  id: string;
  label: string;
  type: string;
  properties?: Record<string, unknown>;
}

export interface GraphEdge {
  source: string;
  target: string;
  label: string;
  weight: number;
  properties?: Record<string, unknown>;
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

// ── Hotspot ──
export interface HotspotLayer {
  hotspotLayerId: number;
  districtId?: number;
  tileX?: number;
  tileY?: number;
  densityScore?: number;
  weekStart?: string;
  weekEnd?: string;
}

// ── Anomaly ──
export interface AnomalyAlert {
  anomalyAlertId: number;
  districtId?: number;
  crimeHeadId?: number;
  weekStart?: string;
  observedCount?: number;
  baselineMean?: number;
  stdDev?: number;
  zScore?: number;
  alertLevel?: number;
}

// ── Risk ──
export interface RiskScore {
  riskScoreId: number;
  personEntityId: number;
  score: number;
  modelVersion?: string;
  featuresJson?: string;
  computedAt?: string;
}

// ── RAG ──
export interface RAGQuery {
  query: string;
  topK?: number;
  districtId?: number;
  crimeHeadId?: number;
}

export interface RAGCitation {
  caseMasterId: number;
  chunkText: string;
  relevance: number;
  crimeNo?: string;
}

export interface RAGResponse {
  answer: string;
  citations: RAGCitation[];
  confidence: number;
  processingTimeMs: number;
}

// ── Audit ──
export interface AuditEntry {
  auditLogId: number;
  userId?: number;
  action?: string;
  entityType?: string;
  entityId?: number;
  timestamp?: string;
  ipAddress?: string;
}
