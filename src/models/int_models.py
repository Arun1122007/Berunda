"""Intelligence schema models — int_ tables for entity resolution, graphs, risk, etc."""

from __future__ import annotations

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.types import TypeDecorator

from src.models.base import Base


class VectorFallback(TypeDecorator):
    impl = Text
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            try:
                from pgvector.sqlalchemy import Vector
                return dialect.type_descriptor(Vector(1536))
            except ImportError:
                pass
        return dialect.type_descriptor(Text())


class PersonEntity(Base):
    __tablename__ = "int_PersonEntity"

    PersonEntityID = Column(Integer, primary_key=True)
    CanonicalName = Column(String(200), nullable=False, index=True)
    DOB = Column(DateTime)
    Gender = Column(String(1))
    PrimaryDistrictID = Column(Integer, ForeignKey("src_District.DistrictID"))
    RiskScoreID = Column(Integer, ForeignKey("int_RiskScore.RiskScoreID"))
    CreatedAt = Column(DateTime, server_default=func.now())
    UpdatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now())

    links = relationship("PersonEntityLink", back_populates="person_entity")
    edges_a = relationship(
        "RelationshipEdge",
        foreign_keys="RelationshipEdge.PersonEntityA",
        back_populates="person_a",
    )
    edges_b = relationship(
        "RelationshipEdge",
        foreign_keys="RelationshipEdge.PersonEntityB",
        back_populates="person_b",
    )
    risk_scores = relationship(
        "RiskScore",
        back_populates="person_entity",
        foreign_keys="RiskScore.PersonEntityID",
    )


class PersonEntityLink(Base):
    __tablename__ = "int_PersonEntityLink"

    PersonEntityLinkID = Column(Integer, primary_key=True)
    PersonEntityID = Column(Integer, ForeignKey("int_PersonEntity.PersonEntityID"), nullable=False)
    SourceTable = Column(String(50))
    SourceRecordID = Column(Integer)
    CaseMasterID = Column(Integer, ForeignKey("src_CaseMaster.CaseMasterID"))
    Confidence = Column(Float)
    IsReviewed = Column(Integer, default=0)
    ReviewedBy = Column(Integer, ForeignKey("src_Employee.EmployeeID"))
    ReviewedAt = Column(DateTime)
    CreatedAt = Column(DateTime, server_default=func.now())

    __table_args__ = (
        CheckConstraint('Confidence >= 0.0 AND Confidence <= 1.0', name='check_pelink_confidence'),
    )

    person_entity = relationship("PersonEntity", back_populates="links")


class RelationshipEdge(Base):
    __tablename__ = "int_RelationshipEdge"

    RelationshipEdgeID = Column(Integer, primary_key=True)
    PersonEntityA = Column(Integer, ForeignKey("int_PersonEntity.PersonEntityID"), nullable=False)
    PersonEntityB = Column(Integer, ForeignKey("int_PersonEntity.PersonEntityID"), nullable=False)
    RelationshipType = Column(String(50))
    SourceCaseID = Column(Integer, ForeignKey("src_CaseMaster.CaseMasterID"))
    Confidence = Column(Float)
    DiscoveredAt = Column(DateTime)
    CreatedAt = Column(DateTime, server_default=func.now())

    __table_args__ = (
        CheckConstraint('Confidence >= 0.0 AND Confidence <= 1.0', name='check_reledge_confidence'),
    )

    person_a = relationship(
        "PersonEntity",
        foreign_keys=[PersonEntityA],
        back_populates="edges_a",
    )
    person_b = relationship(
        "PersonEntity",
        foreign_keys=[PersonEntityB],
        back_populates="edges_b",
    )


class VehicleLink(Base):
    __tablename__ = "int_VehicleLink"

    VehicleLinkID = Column(Integer, primary_key=True)
    VehicleNumber = Column(String(50), nullable=False)
    CaseMasterID = Column(Integer, ForeignKey("src_CaseMaster.CaseMasterID"))
    Confidence = Column(Float)
    Source = Column(String(50))
    CreatedAt = Column(DateTime, server_default=func.now())

    __table_args__ = (
        CheckConstraint('Confidence >= 0.0 AND Confidence <= 1.0', name='check_vlink_confidence'),
    )


class RiskScore(Base):
    __tablename__ = "int_RiskScore"

    RiskScoreID = Column(Integer, primary_key=True)
    PersonEntityID = Column(Integer, ForeignKey("int_PersonEntity.PersonEntityID"), nullable=False)
    Score = Column(Float, nullable=False)
    ModelVersion = Column(String(20))
    FeaturesJSON = Column(Text)
    ComputedAt = Column(DateTime)
    CreatedAt = Column(DateTime, server_default=func.now())

    __table_args__ = (
        CheckConstraint('Score >= 0.0 AND Score <= 1.0', name='check_risk_score_range'),
    )

    person_entity = relationship(
        "PersonEntity",
        back_populates="risk_scores",
        foreign_keys=[PersonEntityID],
    )
    feature_importances = relationship("RiskScoreFeatureImportance", back_populates="risk_score")


class RiskScoreFeatureImportance(Base):
    __tablename__ = "int_RiskScoreFeatureImportance"

    RiskScoreImportanceID = Column(Integer, primary_key=True)
    RiskScoreID = Column(Integer, ForeignKey("int_RiskScore.RiskScoreID"), nullable=False)
    FeatureName = Column(String(100), nullable=False)
    ImportanceValue = Column(Float, nullable=False)
    CreatedAt = Column(DateTime, server_default=func.now())

    risk_score = relationship("RiskScore", back_populates="feature_importances")


class MoPattern(Base):
    __tablename__ = "int_MoPattern"

    MoPatternID = Column(Integer, primary_key=True)
    PatternName = Column(String(200), nullable=False)
    Embedding = Column(VectorFallback)
    CreatedAt = Column(DateTime, server_default=func.now())

    links = relationship("MoPatternLink", back_populates="pattern")


class MoPatternLink(Base):
    __tablename__ = "int_MoPatternLink"

    MoPatternLinkID = Column(Integer, primary_key=True)
    MoPatternID = Column(Integer, ForeignKey("int_MoPattern.MoPatternID"), nullable=False)
    CaseMasterID = Column(Integer, ForeignKey("src_CaseMaster.CaseMasterID"))
    SimilarityScore = Column(Float)
    CreatedAt = Column(DateTime, server_default=func.now())

    __table_args__ = (
        CheckConstraint('SimilarityScore >= 0.0 AND SimilarityScore <= 1.0', name='check_mopattern_similarity'),
    )

    pattern = relationship("MoPattern", back_populates="links")


class AnomalyAlert(Base):
    __tablename__ = "int_AnomalyAlert"

    AnomalyAlertID = Column(Integer, primary_key=True)
    DistrictID = Column(Integer, ForeignKey("src_District.DistrictID"))
    CrimeHeadID = Column(Integer, ForeignKey("src_CrimeHead.CrimeHeadID"))
    WeekStart = Column(DateTime)
    ObservedCount = Column(Integer)
    BaselineMean = Column(Float)
    StdDev = Column(Float)
    ZScore = Column(Float)
    AlertLevel = Column(Integer)
    CreatedAt = Column(DateTime, server_default=func.now())


class HotspotLayer(Base):
    __tablename__ = "int_HotspotLayer"

    HotspotLayerID = Column(Integer, primary_key=True)
    DistrictID = Column(Integer, ForeignKey("src_District.DistrictID"))
    TileX = Column(Integer)
    TileY = Column(Integer)
    DensityScore = Column(Float)
    WeekStart = Column(DateTime)
    WeekEnd = Column(DateTime)
    CreatedAt = Column(DateTime, server_default=func.now())


class RAGCorpusChunk(Base):
    __tablename__ = "int_RAGCorpusChunk"

    ChunkID = Column(Integer, primary_key=True)
    CaseMasterID = Column(Integer, ForeignKey("src_CaseMaster.CaseMasterID"))
    ChunkIndex = Column(Integer)
    ChunkText = Column(Text)
    Embedding = Column(VectorFallback)
    TenantDistrictID = Column(Integer, ForeignKey("src_District.DistrictID"))
    SourceDocument = Column(String(255))
    ChunkHash = Column(String(64))
    CreatedAt = Column(DateTime, server_default=func.now())


class AIExtractionQueue(Base):
    __tablename__ = "int_AIExtractionQueue"

    ExtractionID = Column(Integer, primary_key=True)
    CaseMasterID = Column(Integer, ForeignKey("src_CaseMaster.CaseMasterID"), nullable=False)
    Status = Column(String(50), default="PENDING")
    ModelUsed = Column(String(100))
    RawJSON = Column(Text)
    ReviewedBy = Column(Integer, ForeignKey("auth_User.UserID"))
    CreatedAt = Column(DateTime, server_default=func.now())
    UpdatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now())


class ERMergeCandidate(Base):
    __tablename__ = "int_ERMergeCandidate"

    CandidateID = Column(Integer, primary_key=True)
    EntityA = Column(Integer, ForeignKey("int_PersonEntity.PersonEntityID"), nullable=False)
    EntityB = Column(Integer, ForeignKey("int_PersonEntity.PersonEntityID"), nullable=False)
    SimilarityScore = Column(Float)
    Status = Column(String(50), default="PENDING")
    ReviewedBy = Column(Integer, ForeignKey("auth_User.UserID"))
    CreatedAt = Column(DateTime, server_default=func.now())


class InvestigationNote(Base):
    __tablename__ = "int_InvestigationNote"

    NoteID = Column(Integer, primary_key=True)
    CaseMasterID = Column(Integer, ForeignKey("src_CaseMaster.CaseMasterID"), nullable=False, index=True)
    AuthorID = Column(Integer, ForeignKey("auth_User.UserID"), nullable=False)
    NoteType = Column(String(50), default="general")
    Content = Column(Text, nullable=False)
    IsAmendment = Column(Boolean, default=False)
    OriginalNoteID = Column(Integer, ForeignKey("int_InvestigationNote.NoteID"), nullable=True)
    Visibility = Column(String(50), default="station")
    CreatedAt = Column(DateTime, server_default=func.now())
    UpdatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now())

    case = relationship("CaseMaster", back_populates="notes")
    author = relationship("User")


class CaseAssignment(Base):
    __tablename__ = "int_CaseAssignment"

    AssignmentID = Column(Integer, primary_key=True)
    CaseMasterID = Column(Integer, ForeignKey("src_CaseMaster.CaseMasterID"), nullable=False, index=True)
    AssignedOfficerID = Column(Integer, ForeignKey("src_Employee.EmployeeID"), nullable=False, index=True)
    AssignedByUserID = Column(Integer, ForeignKey("auth_User.UserID"), nullable=False)
    AssignmentReason = Column(String(500), nullable=True)
    Status = Column(String(50), default="active")
    AssignedAt = Column(DateTime, server_default=func.now())
    EndedAt = Column(DateTime, nullable=True)

    case = relationship("CaseMaster", back_populates="assignments")
    officer = relationship("Employee")
    assigned_by = relationship("User")


class SupervisorReview(Base):
    __tablename__ = "int_SupervisorReview"

    ReviewID = Column(Integer, primary_key=True)
    CaseMasterID = Column(Integer, ForeignKey("src_CaseMaster.CaseMasterID"), nullable=False, index=True)
    SupervisorID = Column(Integer, ForeignKey("auth_User.UserID"), nullable=False)
    ReviewType = Column(String(50), default="periodic")
    Status = Column(String(50), default="pending")
    Comments = Column(Text, nullable=True)
    ActionRequested = Column(String(200), nullable=True)
    ReviewedAt = Column(DateTime, server_default=func.now())

    case = relationship("CaseMaster", back_populates="reviews")
    supervisor = relationship("User")


class RelatedCaseSuggestion(Base):
    __tablename__ = "int_RelatedCaseSuggestion"

    SuggestionID = Column(Integer, primary_key=True)
    SourceFIRID = Column(Integer, ForeignKey("src_CaseMaster.CaseMasterID"), nullable=False, index=True)
    CandidateFIRID = Column(Integer, ForeignKey("src_CaseMaster.CaseMasterID"), nullable=False, index=True)
    ConfidenceScore = Column(Float, nullable=False)
    SupportingSignals = Column(Text, nullable=False)
    Explanation = Column(Text, nullable=False)
    ModelVersion = Column(String(50), default="hybrid-v1.0")
    ReviewStatus = Column(String(50), default="suggested")
    ReviewedByUserID = Column(Integer, ForeignKey("auth_User.UserID"), nullable=True)
    ReviewReason = Column(String(500), nullable=True)
    ReviewedAt = Column(DateTime, nullable=True)
    CreatedAt = Column(DateTime, server_default=func.now())

    source_case = relationship("CaseMaster", foreign_keys=[SourceFIRID])
    candidate_case = relationship("CaseMaster", foreign_keys=[CandidateFIRID])
    reviewed_by = relationship("User")


class ReportRequest(Base):
    __tablename__ = "int_ReportRequest"

    ReportID = Column(String(50), primary_key=True)
    RequestedByUserID = Column(Integer, ForeignKey("auth_User.UserID"), nullable=False, index=True)
    ReportType = Column(String(50), nullable=False)
    Parameters = Column(Text, nullable=True)
    Status = Column(String(50), default="requested")
    StorageObjectRef = Column(String(500), nullable=True)
    FileFormat = Column(String(20), default="pdf")
    ErrorMessage = Column(Text, nullable=True)
    CreatedAt = Column(DateTime, server_default=func.now())
    CompletedAt = Column(DateTime, nullable=True)
    ExpiresAt = Column(DateTime, nullable=True)

    requested_by = relationship("User")


class BackgroundJob(Base):
    __tablename__ = "int_BackgroundJob"

    JobID = Column(String(50), primary_key=True)
    JobType = Column(String(100), nullable=False)
    Payload = Column(Text, nullable=True)
    IdempotencyKey = Column(String(100), unique=True, index=True, nullable=True)
    RequestedByUserID = Column(Integer, ForeignKey("auth_User.UserID"), nullable=True)
    Status = Column(String(50), default="queued")
    AttemptCount = Column(Integer, default=0)
    MaxAttempts = Column(Integer, default=3)
    ResultRef = Column(String(500), nullable=True)
    ErrorMessage = Column(Text, nullable=True)
    CreatedAt = Column(DateTime, server_default=func.now())
    StartedAt = Column(DateTime, nullable=True)
    CompletedAt = Column(DateTime, nullable=True)

    requested_by = relationship("User")

