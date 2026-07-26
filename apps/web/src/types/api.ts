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

// ── Phase 4: Investigation Notes ──
export interface InvestigationNoteResponse {
  noteId: number;
  caseMasterId: number;
  authorId: number;
  noteType: string | null;
  content: string;
  isAmendment: boolean;
  originalNoteId: number | null;
  visibility: string | null;
  createdAt: string | null;
  updatedAt: string | null;
}

export interface InvestigationNote {
  noteId: number;
  caseMasterId: number;
  authorId: number;
  noteType?: string;
  content: string;
  isAmendment: boolean;
  originalNoteId?: number;
  visibility?: string;
  createdAt?: string;
  updatedAt?: string;
}

export interface InvestigationNoteCreate {
  content: string;
  noteType?: string;
  visibility?: string;
}

// ── Phase 4: Case Assignment ──
export interface CaseAssignmentResponse {
  assignmentId: number;
  caseMasterId: number;
  assignedOfficerId: number;
  assignedByUserId: number;
  assignmentReason: string | null;
  status: string | null;
  assignedAt: string | null;
  endedAt: string | null;
}

export interface CaseAssignment {
  assignmentId: number;
  caseMasterId: number;
  assignedOfficerId: number;
  assignedByUserId: number;
  assignmentReason?: string;
  status?: string;
  assignedAt?: string;
  endedAt?: string;
}

export interface CaseAssignmentCreate {
  assignedOfficerId: number;
  assignmentReason?: string;
}

// ── Phase 4: Supervisor Review ──
export interface SupervisorReviewResponse {
  reviewId: number;
  caseMasterId: number;
  supervisorId: number;
  reviewType: string | null;
  status: string | null;
  comments: string | null;
  actionRequested: string | null;
  reviewedAt: string | null;
}

export interface SupervisorReview {
  reviewId: number;
  caseMasterId: number;
  supervisorId: number;
  reviewType?: string;
  status?: string;
  comments?: string;
  actionRequested?: string;
  reviewedAt?: string;
}

// ── Phase 4: Timeline ──
export interface TimelineEvent {
  type: string;
  timestamp?: string;
  description?: string;
  noteId?: number;
  assignmentId?: number;
  reviewId?: number;
}

// ── Phase 4: Related Cases ──
export interface RelatedCaseSuggestion {
  suggestionId: number;
  sourceFirId: number;
  candidateFirId: number;
  confidenceScore: number;
  supportingSignals: string;
  explanation: string;
  modelVersion?: string;
  reviewStatus?: string;
  reviewedByUserId?: number;
  reviewReason?: string;
  reviewedAt?: string;
  createdAt?: string;
  candidateCrimeNo?: string;
  candidateStatusId?: number;
}

export interface RelatedCaseSuggestionResponse {
  suggestionId: number;
  sourceFIRId: number;
  candidateFIRId: number;
  confidenceScore: number;
  supportingSignals: string;
  explanation: string;
  modelVersion: string | null;
  reviewStatus: string | null;
  reviewedByUserId: number | null;
  reviewReason: string | null;
  reviewedAt: string | null;
  createdAt: string | null;
  candidateCrimeNo: string | null;
  candidateStatusId: number | null;
}

export interface RelatedCaseReviewRequest {
  reviewStatus: "accepted" | "rejected";
  reviewReason?: string;
}

// ── Phase 4: Evidence ──
export interface EvidenceItem {
  evidenceId: number;
  caseMasterId: number;
  evidenceType?: string;
  description?: string;
  storagePath?: string;
  status?: string;
  sensitivity?: string;
  createdAt?: string;
}

export interface EvidenceMetadata {
  evidenceId: number;
  caseMasterId: number;
  evidenceType: string | null;
  description: string | null;
  storagePath: string | null;
  collectedAt: string | null;
  collectedBy: string | null;
  source: string | null;
  location: string | null;
  checksum: string | null;
  fileType: string | null;
  fileSize: number | null;
  status: string | null;
  sensitivity: string | null;
  createdAt: string | null;
  updatedAt: string | null;
}

export interface EvidenceStatusUpdate {
  status: string;
}

// ── Phase 4: Vehicles ──
export interface VehicleLink {
  vehicleLinkId: number;
  vehicleNumber: string;
  caseMasterId?: number;
  confidence?: number;
  source?: string;
  createdAt?: string;
}

// ── Phase 4: Dashboard ──
export interface DashboardMetrics {
  totalFirs: number;
  statusCounts: Record<string, number>;
  pendingReviewCount: number;
  unassignedCount: number;
  assignedToMeCount: number;
  recentActivityCount: number;
}

export interface SupervisorDashboardMetrics {
  totalFirs: number;
  statusCounts: Record<string, number>;
  pendingReviewCount: number;
  unassignedCount: number;
  activeOfficerCount: number;
  casesPerOfficer: Record<string, number>;
}

export interface RecentActivityItem {
  caseMasterId: number;
  crimeNo?: string;
  activityType: string;
  description?: string;
  timestamp?: string;
}

// ── Phase 4: Reports ──
export interface ReportRequest {
  reportId: string;
  requestedByUserId: number;
  reportType: string;
  parameters?: string;
  status: string;
  storageObjectRef?: string;
  fileFormat?: string;
  errorMessage?: string;
  createdAt?: string;
  completedAt?: string;
  expiresAt?: string;
}

export interface ReportRequestCreate {
  reportType: string;
  parameters?: string;
  fileFormat?: string;
}

// ── Phase 4: Search ──
export interface SearchFilters {
  query?: string;
  crimeNo?: string;
  dateFrom?: string;
  dateTo?: string;
  statusId?: number;
  policeStationId?: number;
  assignedOfficerId?: number;
  crimeMajorHeadId?: number;
  personName?: string;
  vehicleNumber?: string;
  page: number;
  pageSize: number;
  semantic?: boolean;
}

export interface SearchResultItem {
  caseMasterId: number;
  crimeNo?: string;
  crimeRegisteredDate?: string;
  policeStationId?: number;
  caseStatusId?: number;
  briefFacts?: string;
  confidence?: number;
  matchReason?: string;
}

export interface SearchResponse {
  items: SearchResultItem[];
  total: number;
  page: number;
  pageSize: number;
  semanticUsed: boolean;
}
