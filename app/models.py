from sqlalchemy import Column, Integer, String, Text, Float
from app.database import Base


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    period = Column(String, nullable=False)
    transcript = Column(Text, nullable=False)

    filename = Column(String, nullable=True)
    source_type = Column(String, nullable=False, default="text")

    sentiment_compound = Column(Float, nullable=False)
    normalized_sentiment = Column(Integer, nullable=False)
    risk_count = Column(Integer, nullable=False)
    risk_penalty = Column(Integer, nullable=False)
    signal_score = Column(Integer, nullable=False)
    signal_label = Column(String, nullable=False)

    matched_risk_keywords = Column(Text, nullable=False, default="")
    analysis_summary = Column(Text, nullable=False, default="")

    most_positive_sentence = Column(Text, nullable=True)
    most_negative_sentence = Column(Text, nullable=True)