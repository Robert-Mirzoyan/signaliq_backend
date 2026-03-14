from __future__ import annotations

from typing import Optional
from pydantic import BaseModel


class AnalysisCreate(BaseModel):
    company: str
    period: str
    transcript: str


class AnalysisResponse(BaseModel):
    id: int
    company: str
    period: str
    transcript: str
    filename: Optional[str]
    source_type: str
    sentiment_compound: float
    normalized_sentiment: int
    risk_count: int
    risk_penalty: int
    signal_score: int
    signal_label: str
    matched_risk_keywords: list[str]
    analysis_summary: str
    most_positive_sentence: str
    most_negative_sentence: str

    class Config:
        from_attributes = True