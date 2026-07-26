"""Authentication schema models — auth_ tables for users, roles, and sessions."""

from __future__ import annotations

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.models.base import Base


class User(Base):
    __tablename__ = "auth_User"

    UserID = Column(Integer, primary_key=True)
    Email = Column(String(255), unique=True, nullable=False, index=True)
    HashedPassword = Column(String(255), nullable=False)
    Role = Column(String(50), nullable=False)
    DistrictID = Column(Integer, ForeignKey("src_District.DistrictID"), nullable=True)
    IsActive = Column(Boolean, default=True)
    CreatedAt = Column(DateTime, server_default=func.now())
    UpdatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now())

    district = relationship("District")
    sessions = relationship("Session", back_populates="user")


class Session(Base):
    __tablename__ = "auth_Session"

    SessionID = Column(Integer, primary_key=True)
    UserID = Column(Integer, ForeignKey("auth_User.UserID"), nullable=False)
    TokenHash = Column(String(255), unique=True, nullable=False, index=True)
    ExpiresAt = Column(DateTime, nullable=False)
    RevokedAt = Column(DateTime, nullable=True)
    CreatedAt = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="sessions")


class Permission(Base):
    __tablename__ = "auth_Permission"

    PermissionID = Column(Integer, primary_key=True)
    Role = Column(String(50), nullable=False, index=True)
    Resource = Column(String(100), nullable=False)
    Action = Column(String(50), nullable=False)
    CreatedAt = Column(DateTime, server_default=func.now())
