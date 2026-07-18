export interface FIR {
  firId: string;
  caseNumber: string;
  district: string;
  policeStation: string;
  dateFiled: string;
  sections: string[];
  narrative: string;
  status: "active" | "closed" | "under-investigation";
  createdAt: string;
  updatedAt: string;
}

export interface Case {
  caseId: string;
  firId: string;
  caseNumber: string;
  district: string;
  policeStation: string;
  crimeType: string;
  status: string;
  filedAt: string;
  registeredAt: string;
  summary: string;
  persons: PersonEntityLink[];
  vehicles: VehicleLink[];
  locations: LocationEntity[];
}

export interface Person {
  personId: string;
  name: string;
  aliases: string[];
  dateOfBirth?: string;
  age?: number;
  gender?: string;
  addresses: string[];
  idMarks: string[];
  phoneNumbers: string[];
  riskScore?: RiskScore;
}

export interface PersonEntityLink {
  personId: string;
  caseId: string;
  role: "accused" | "victim" | "witness" | "complainant" | "informant";
  name: string;
  firMention: string;
  confidence: number;
}

export interface VehicleLink {
  vehicleId: string;
  caseId: string;
  registrationNumber: string;
  type: string;
  make?: string;
  model?: string;
  ownerName?: string;
  confidence: number;
}

export interface HotspotData {
  district: string;
  policeStation: string;
  crimeType: string;
  lat: number;
  lng: number;
  intensity: number;
  trend: "increasing" | "decreasing" | "stable";
  period: string;
}

export interface AnomalyAlert {
  alertId: string;
  district: string;
  crimeType: string;
  observedCount: number;
  expectedCount: number;
  zScore: number;
  severity: "low" | "medium" | "high" | "critical";
  detectedAt: string;
  period: string;
  acknowledged: boolean;
}

export interface RiskScore {
  personId: string;
  score: number;
  level: "low" | "medium" | "high" | "critical";
  features: Record<string, number>;
  explanation: string;
  computedAt: string;
  modelVersion: string;
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface GraphNode {
  id: string;
  label: string;
  type: "person" | "vehicle" | "location" | "case" | "organization";
  properties: Record<string, unknown>;
}

export interface GraphEdge {
  source: string;
  target: string;
  label: string;
  weight: number;
  properties: Record<string, unknown>;
}

export interface RAGQuery {
  query: string;
  filters?: {
    districts?: string[];
    crimeTypes?: string[];
    dateRange?: { start: string; end: string };
  };
  topK?: number;
}

export interface RAGResponse {
  answer: string;
  citations: RAGCitation[];
  confidence: number;
  processingTimeMs: number;
}

export interface RAGCitation {
  caseNumber: string;
  snippet: string;
  relevance: number;
  source: string;
}

export interface AuditEntry {
  auditId: string;
  userId: string;
  action: string;
  resource: string;
  resourceId: string;
  details: Record<string, unknown>;
  ipAddress: string;
  userAgent: string;
  timestamp: string;
}

export interface User {
  userId: string;
  email: string;
  name: string;
  role: "admin" | "analyst" | "viewer";
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
