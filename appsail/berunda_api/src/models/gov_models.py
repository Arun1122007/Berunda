"""Governance schema models — gov_ tables for audit, fairness, and provenance."""

from __future__ import annotations

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from src.models.base import Base


class AuditLog(Base):
    __tablename__ = "gov_AuditLog"

    AuditLogID = Column(Integer, primary_key=True)
    CorrelationID = Column(String(100))
    UserID = Column(Integer, ForeignKey("src_Employee.EmployeeID"))
    Action = Column(String(50), nullable=False)
    EntityType = Column(String(50))
    EntityID = Column(Integer)
    OldValue = Column(Text)
    NewValue = Column(Text)
    Timestamp = Column(DateTime, server_default=func.now())
    IPAddress = Column(String(45))


class FairnessCheckResult(Base):
    __tablename__ = "gov_FairnessCheckResult"

    FairnessCheckID = Column(Integer, primary_key=True)
    CheckType = Column(String(50), nullable=False)
    Timestamp = Column(DateTime, server_default=func.now())
    Passed = Column(Integer)
    Details = Column(Text)
    CheckedBy = Column(String(100))


class DataProvenanceRecord(Base):
    __tablename__ = "gov_DataProvenanceRecord"

    ProvenanceID = Column(Integer, primary_key=True)
    TargetTable = Column(String(50), nullable=False)
    TargetRecordID = Column(Integer)
    SourceTable = Column(String(50))
    SourceRecordID = Column(Integer)
    TransformationDescription = Column(String(500))
    CreatedAt = Column(DateTime, server_default=func.now())
