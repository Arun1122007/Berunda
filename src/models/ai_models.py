"""AI schema models — ai_ tables for usage tracking, prompts, and conversations."""

from __future__ import annotations

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.models.base import Base


class AIUsageRecord(Base):
    __tablename__ = "ai_UsageRecord"

    UsageID = Column(Integer, primary_key=True)
    Provider = Column(String(50), nullable=False)
    Model = Column(String(100), nullable=False)
    Feature = Column(String(100), nullable=False)
    TokensIn = Column(Integer, default=0)
    TokensOut = Column(Integer, default=0)
    CostUSD = Column(Float, default=0.0)
    LatencyMs = Column(Integer, default=0)
    UserID = Column(Integer, ForeignKey("auth_User.UserID"), nullable=True)
    DistrictID = Column(Integer, ForeignKey("src_District.DistrictID"), nullable=True)
    CreatedAt = Column(DateTime, server_default=func.now())

    user = relationship("User")
    district = relationship("District")


class PromptVersion(Base):
    __tablename__ = "ai_PromptVersion"

    PromptVersionID = Column(Integer, primary_key=True)
    PromptName = Column(String(100), nullable=False, index=True)
    Version = Column(String(20), nullable=False)
    Template = Column(Text, nullable=False)
    ModelConfig = Column(JSON)
    IsActive = Column(Boolean, default=True)
    CreatedAt = Column(DateTime, server_default=func.now())


class AIConversation(Base):
    __tablename__ = "ai_Conversation"

    ConversationID = Column(Integer, primary_key=True)
    UserID = Column(Integer, ForeignKey("auth_User.UserID"), nullable=False)
    AgentType = Column(String(50), nullable=False)
    Title = Column(String(200))
    CreatedAt = Column(DateTime, server_default=func.now())
    UpdatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now())

    messages = relationship("AIMessage", back_populates="conversation", cascade="all, delete-orphan")


class AIMessage(Base):
    __tablename__ = "ai_Message"

    MessageID = Column(Integer, primary_key=True)
    ConversationID = Column(Integer, ForeignKey("ai_Conversation.ConversationID"), nullable=False)
    Role = Column(String(20), nullable=False)  # system, user, assistant, tool
    Content = Column(Text, nullable=False)
    ToolCalls = Column(JSON, nullable=True)
    CreatedAt = Column(DateTime, server_default=func.now())

    conversation = relationship("AIConversation", back_populates="messages")


class AIFeedback(Base):
    __tablename__ = "ai_Feedback"

    FeedbackID = Column(Integer, primary_key=True)
    MessageID = Column(Integer, ForeignKey("ai_Message.MessageID"), nullable=False)
    UserID = Column(Integer, ForeignKey("auth_User.UserID"), nullable=False)
    IsPositive = Column(Boolean, nullable=False)
    Comments = Column(Text, nullable=True)
    CreatedAt = Column(DateTime, server_default=func.now())
