import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
from app.risk_keywords import RISK_KEYWORDS

nltk.download("vader_lexicon", quiet=True)
nltk.download("punkt")

sia = SentimentIntensityAnalyzer()


def find_risk_keywords(text: str) -> list[str]:
    text_lower = text.lower()
    matched = []

    for keyword in RISK_KEYWORDS:
        if re.search(rf"\b{re.escape(keyword)}\b", text_lower):
            matched.append(keyword)

    return matched


def get_signal_label(signal_score: int) -> str:
    if signal_score < 40:
        return "Negative"
    if signal_score < 70:
        return "Mixed"
    return "Positive"


def build_summary(signal_label: str, risk_count: int, sentiment_compound: float) -> str:
    if signal_label == "Positive":
        if risk_count == 0:
            return "Strongly positive document with little visible risk language."
        return "Overall positive document, though some risk-related language is present."

    if signal_label == "Mixed":
        return "Mixed signals: some positive sentiment is present, but risk language reduces confidence."

    return "Negative or cautious overall tone with meaningful risk language."

def sentence_sentiment_analysis(text: str):
    sentences = sent_tokenize(text)

    if not sentences:
        return None, None

    scores = []
    for s in sentences:
        scores.append((s, sia.polarity_scores(s)["compound"]))

    most_positive = max(scores, key=lambda x: x[1])
    most_negative = min(scores, key=lambda x: x[1])

    return most_positive, most_negative

def compute_signal_scores(transcript: str) -> dict:
    if not transcript or len(transcript.strip()) < 50:
        raise ValueError("Transcript is too short for reliable analysis.")

    sentiment = sia.polarity_scores(transcript)
    compound = sentiment["compound"]

    normalized_sentiment = int(((compound + 1) / 2) * 100)

    matched_risk_keywords = find_risk_keywords(transcript)
    risk_count = len(matched_risk_keywords)

    risk_penalty = min(risk_count * 2, 30)

    signal_score = max(0, min(100, normalized_sentiment - risk_penalty))
    signal_label = get_signal_label(signal_score)
    analysis_summary = build_summary(signal_label, risk_count, compound)

    most_positive, most_negative = sentence_sentiment_analysis(transcript)

    return {
        "sentiment_compound": round(compound, 4),
        "normalized_sentiment": normalized_sentiment,
        "risk_count": risk_count,
        "matched_risk_keywords": matched_risk_keywords,
        "risk_penalty": risk_penalty,
        "signal_score": signal_score,
        "signal_label": signal_label,
        "analysis_summary": analysis_summary,
        "most_positive_sentence": most_positive[0] if most_positive else None,
        "most_negative_sentence": most_negative[0] if most_negative else None,
    }