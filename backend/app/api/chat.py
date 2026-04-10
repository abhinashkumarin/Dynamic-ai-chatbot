"""
Chat REST API — Properly calls analytics after every message.
MongoDB mein save hota hai.
"""

import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, BackgroundTasks
from loguru import logger

from app.models.schemas import ChatRequest, ChatResponse, FeedbackRequest, AnalyzeRequest
from app.services.nlp_engine import nlp_engine
from app.services.ml_model import ml_model
from app.services.analytics_service import analytics_service
from app.core.database import get_db

router = APIRouter()

# In-memory fallback when MongoDB unavailable
_conversations: dict = {}
_feedback_store: list = []


async def _save_conversation(
    session_id: str,
    user_id: str,
    user_message: str,
    bot_response: str,
    metadata: dict,
    source: str = "rest_api",
):
    """MongoDB mein save karo — in-memory fallback with."""
    record = {
        "session_id":   session_id,
        "user_id":      user_id,
        "user_message": user_message,
        "bot_response": bot_response,
        "intent":       metadata.get("intent", {}).get("intent", "unknown"),
        "confidence":   metadata.get("intent", {}).get("confidence", 0),
        "emotion":      metadata.get("emotion"),
        "sentiment_label": metadata.get("sentiment", {}).get("label", "neutral"),
        "sentiment_score": metadata.get("sentiment", {}).get("score", 0),
        "processing_time_ms": metadata.get("processing_time_ms", 0),
        "turn_count":   metadata.get("turn_count", 0),
        "source":       source,
        "created_at":   datetime.utcnow(),
    }

    # Try MongoDB
    db = get_db()
    if db is not None:
        try:
            result = await db.conversations.insert_one(record)
            if result.inserted_id:
                logger.debug(f"💾 MongoDB saved: {session_id}")
                return
        except Exception as e:
            logger.warning(f"⚠️ MongoDB save failed: {e}")

    # In-memory fallback
    if session_id not in _conversations:
        _conversations[session_id] = []
    _conversations[session_id].append(record)
    if len(_conversations[session_id]) > 100:
        _conversations[session_id] = _conversations[session_id][-50:]


# ─── POST /api/chat/message ───────────────────────────────────────────────────
@router.post("/message", response_model=ChatResponse)
async def send_message(body: ChatRequest, background_tasks: BackgroundTasks):
    if not nlp_engine.is_ready:
        raise HTTPException(503, "NLP Engine initializing — please wait.")

    session_id = body.session_id or str(uuid.uuid4())
    user_id    = body.user_id or "anonymous"

    # ── Full NLP Pipeline ─────────────────────────────────────────────────────
    result  = await nlp_engine.process(body.message, session_id)
    ml_pred = ml_model.predict(body.message)
    if ml_pred:
        result["metadata"]["ml_prediction"] = ml_pred

    # ── Track Analytics (background) ─────────────────────────────────────────
    background_tasks.add_task(
        analytics_service.track,
        intent            = result["metadata"]["intent"]["intent"],
        sentiment_label   = result["metadata"]["sentiment"]["label"],
        processing_time_ms= result["metadata"]["processing_time_ms"],
        confidence        = result["metadata"]["intent"]["confidence"],
        session_id        = session_id,
    )

    # ── Save to MongoDB (background) ──────────────────────────────────────────
    background_tasks.add_task(
        _save_conversation,
        session_id   = session_id,
        user_id      = user_id,
        user_message = body.message,
        bot_response = result["response"],
        metadata     = result["metadata"],
        source       = "rest_api",
    )

    return ChatResponse(
        session_id = session_id,
        message    = result["response"],
        metadata   = result["metadata"],
    )


# ─── GET /api/chat/history/{session_id} ──────────────────────────────────────
@router.get("/history/{session_id}")
async def get_history(session_id: str, limit: int = 50):
    db = get_db()
    if db is not None:
        try:
            cursor = db.conversations.find(
                {"session_id": session_id}, {"_id": 0}
            ).sort("created_at", 1).limit(limit)
            msgs = await cursor.to_list(length=limit)
            if msgs:
                return {"session_id": session_id, "messages": msgs,
                        "count": len(msgs), "source": "mongodb"}
        except Exception as e:
            logger.warning(f"DB history fetch failed: {e}")

    msgs = _conversations.get(session_id, [])[-limit:]
    return {"session_id": session_id, "messages": msgs,
            "count": len(msgs), "source": "memory"}


# ─── DELETE /api/chat/history/{session_id} ───────────────────────────────────
@router.delete("/history/{session_id}")
async def clear_history(session_id: str):
    db = get_db()
    deleted = 0
    if db is not None:
        try:
            r = await db.conversations.delete_many({"session_id": session_id})
            deleted = r.deleted_count
        except Exception as e:
            logger.warning(f"DB clear failed: {e}")

    _conversations.pop(session_id, None)
    nlp_engine.context_manager.clear_session(session_id)
    return {"message": "History cleared", "session_id": session_id,
            "deleted_from_db": deleted}


# ─── POST /api/chat/feedback ──────────────────────────────────────────────────
@router.post("/feedback")
async def submit_feedback(body: FeedbackRequest, background_tasks: BackgroundTasks):
    if body.correct_intent:
        ml_model.add_feedback(
            body.message_content, body.correct_intent, body.was_helpful
        )

    record = {**body.model_dump(), "created_at": datetime.utcnow()}
    db = get_db()
    if db is not None:
        try:
            await db.feedback.insert_one(record)
        except Exception as e:
            logger.warning(f"Feedback DB save failed: {e}")
            _feedback_store.append(record)
    else:
        _feedback_store.append(record)

    return {"message": "Feedback received! Thank you! 🙏"}


# ─── POST /api/chat/analyze ───────────────────────────────────────────────────
@router.post("/analyze")
async def analyze_text(body: AnalyzeRequest):
    """Full NLP analysis — no response generated."""
    intent        = nlp_engine.intent_classifier.predict(body.text)
    sentiment     = nlp_engine.sentiment_analyzer.analyze(body.text)
    emotion       = nlp_engine.emotion_detector.detect(body.text)
    entities      = nlp_engine.ner_processor.extract(body.text)
    multi_intents = nlp_engine.multi_intent_detector.detect(
        body.text, nlp_engine.intent_classifier
    )
    ml_pred = ml_model.predict(body.text)

    return {
        "text":     body.text,
        "analysis": {
            "intent":        intent,
            "emotion":       emotion,
            "sentiment":     sentiment,
            "entities":      entities,
            "multi_intents": multi_intents,
            "ml_prediction": ml_pred,
            "word_count":    len(body.text.split()),
            "char_count":    len(body.text),
        },
    }