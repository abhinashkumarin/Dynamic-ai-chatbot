"""Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field


# ─── Chat Schemas ─────────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    session_id: Optional[str] = None
    user_id: Optional[str] = "anonymous"


class SentimentResult(BaseModel):
    label: str
    score: float
    emoji: str
    intensity: str
    positive_words: list[str] = []
    negative_words: list[str] = []
    compound: float = 0.0


class EntityResult(BaseModel):
    emails: list[str] = []
    phones: list[str] = []
    urls: list[str] = []
    dates: list[str] = []
    currencies: list[str] = []
    locations: list[str] = []
    persons: list[str] = []
    organizations: list[str] = []


class IntentResult(BaseModel):
    intent: str
    confidence: float
    all_scores: dict[str, float] = {}


class ChatMetadata(BaseModel):
    intent: IntentResult
    sentiment: SentimentResult
    entities: EntityResult
    processing_time_ms: float
    turn_count: int
    contextual: bool
    ml_prediction: Optional[dict] = None


class ChatResponse(BaseModel):
    session_id: str
    message: str
    metadata: ChatMetadata
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)


# ─── Feedback Schema ──────────────────────────────────────────────────────────
class FeedbackRequest(BaseModel):
    session_id: str
    message_content: str
    rating: int = Field(..., ge=1, le=5)
    was_helpful: bool
    correct_intent: Optional[str] = None
    comment: Optional[str] = None


# ─── Auth Schemas ─────────────────────────────────────────────────────────────
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: Optional[str] = None
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


# ─── Analytics Schemas ────────────────────────────────────────────────────────
class DashboardResponse(BaseModel):
    realtime: dict
    session_stats: dict
    model_stats: dict
    timestamp: datetime = Field(default_factory=datetime.utcnow)
