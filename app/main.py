from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.database import Base, engine, SessionLocal
from app.models import AnalysisResult
from app.schemas import AnalysisCreate, AnalysisResponse
from app.scoring import compute_signal_scores
from app.file_utils import extract_text_from_file

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SignalIQ Backend")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def to_response(result: AnalysisResult) -> dict:
    return {
        "id": result.id,
        "company": result.company,
        "period": result.period,
        "transcript": result.transcript,
        "filename": result.filename,
        "source_type": result.source_type,
        "sentiment_compound": result.sentiment_compound,
        "normalized_sentiment": result.normalized_sentiment,
        "risk_count": result.risk_count,
        "risk_penalty": result.risk_penalty,
        "signal_score": result.signal_score,
        "signal_label": result.signal_label,
        "matched_risk_keywords": result.matched_risk_keywords.split(",") if result.matched_risk_keywords else [],
        "analysis_summary": result.analysis_summary,
        "most_positive_sentence": result.most_positive_sentence,
        "most_negative_sentence": result.most_negative_sentence,
    }

@app.post("/analyze", response_model=AnalysisResponse)
def analyze_transcript(payload: AnalysisCreate, db: Session = Depends(get_db)):
    if not payload.company.strip():
        raise HTTPException(status_code=400, detail="Company must not be empty.")
    if not payload.period.strip():
        raise HTTPException(status_code=400, detail="Period must not be empty.")

    try:
        scores = compute_signal_scores(payload.transcript)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    result = AnalysisResult(
        company=payload.company,
        period=payload.period,
        transcript=payload.transcript,
        filename=None,
        source_type="text",
        sentiment_compound=scores["sentiment_compound"],
        normalized_sentiment=scores["normalized_sentiment"],
        risk_count=scores["risk_count"],
        risk_penalty=scores["risk_penalty"],
        signal_score=scores["signal_score"],
        signal_label=scores["signal_label"],
        matched_risk_keywords=",".join(scores["matched_risk_keywords"]),
        analysis_summary=scores["analysis_summary"],
        most_positive_sentence=scores["most_positive_sentence"],
        most_negative_sentence=scores["most_negative_sentence"],
    )

    db.add(result)
    db.commit()
    db.refresh(result)
    return to_response(result)


@app.post("/analyze/file", response_model=AnalysisResponse)
async def analyze_file(
    company: str = Form(...),
    period: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not company.strip():
        raise HTTPException(status_code=400, detail="Company must not be empty.")
    if not period.strip():
        raise HTTPException(status_code=400, detail="Period must not be empty.")

    file_bytes = await file.read()

    try:
        transcript, source_type = extract_text_from_file(file.filename, file_bytes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not transcript.strip():
        raise HTTPException(status_code=400, detail="Could not extract readable text from file.")

    try:
        scores = compute_signal_scores(transcript)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    result = AnalysisResult(
        company=company,
        period=period,
        transcript=transcript,
        filename=file.filename,
        source_type=source_type,
        sentiment_compound=scores["sentiment_compound"],
        normalized_sentiment=scores["normalized_sentiment"],
        risk_count=scores["risk_count"],
        risk_penalty=scores["risk_penalty"],
        signal_score=scores["signal_score"],
        signal_label=scores["signal_label"],
        matched_risk_keywords=",".join(scores["matched_risk_keywords"]),
        analysis_summary=scores["analysis_summary"],
        most_positive_sentence=scores["most_positive_sentence"],
        most_negative_sentence=scores["most_negative_sentence"],
    )

    db.add(result)
    db.commit()
    db.refresh(result)
    return to_response(result)


@app.get("/analyses", response_model=list[AnalysisResponse])
def get_all_analyses(db: Session = Depends(get_db)):
    results = db.query(AnalysisResult).order_by(AnalysisResult.id.desc()).all()
    return [to_response(r) for r in results]