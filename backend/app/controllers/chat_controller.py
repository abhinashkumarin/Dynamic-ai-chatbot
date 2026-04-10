"""
Chat Controller — REST API + WebSocket dono use karte hain.
MongoDB mein save + analytics track karta hai.
"""

from datetime import datetime
from typing import Optional
from loguru import logger

from app.core.database import get_db
from app.services.nlp_engine import nlp_engine
from app.services.ml_model import ml_model
from app.services.analytics_service import analytics_service


async def process_chat(
    message:    str,
    session_id: str,
    user_id:    Optional[str] = None,
    source:     str = "rest_api",
) -> dict:
    """
    Main chat processing — NLP pipeline + MongoDB save + Analytics track.
    REST API aur WebSocket dono yahi use karte hain.
    """
    # ── NLP Pipeline ─────────────────────────────────────────────────────────
    result  = await nlp_engine.process(message, session_id)
    ml_pred = ml_model.predict(message)

    # ── Track Analytics ───────────────────────────────────────────────────────
    try:
        analytics_service.track(
            intent             = result["metadata"]["intent"]["intent"],
            sentiment_label    = result["metadata"]["sentiment"]["label"],
            processing_time_ms = result["metadata"]["processing_time_ms"],
            confidence         = result["metadata"]["intent"]["confidence"],
            session_id         = session_id,
        )
    except Exception as e:
        logger.warning(f"Analytics track failed: {e}")

    # ── Save to MongoDB ───────────────────────────────────────────────────────
    db = get_db()
    if db is not None:
        try:
            doc = {
                "session_id":         session_id,
                "user_id":            user_id,
                "user_message":       message,
                "bot_response":       result["response"],
                "intent":             result["metadata"].get("intent"),
                "emotion":            result["metadata"].get("emotion"),
                "sentiment":          result["metadata"].get("sentiment"),
                "turn_count":         result["metadata"].get("turn_count"),
                "processing_time_ms": result["metadata"].get("processing_time_ms"),
                "ml_prediction":      ml_pred,
                "source":             source,
                "created_at":         datetime.utcnow(),
            }
            await db.conversations.insert_one(doc)
            logger.debug(f"💾 Saved — session: {session_id}, source: {source}")
        except Exception as e:
            logger.warning(f"⚠️ MongoDB save failed (non-critical): {e}")

    return {
        "response":   result["response"],
        "metadata":   {**result["metadata"], "ml_prediction": ml_pred},
        "session_id": session_id,
    }


async def get_conversation_history(session_id: str, limit: int = 50) -> list:
    """MongoDB se past conversations fetch karo."""
    db = get_db()
    if db is None:
        return []
    try:
        cursor = db.conversations.find(
            {"session_id": session_id}, {"_id": 0}
        ).sort("created_at", -1).limit(limit)
        docs = await cursor.to_list(length=limit)
        return list(reversed(docs))
    except Exception as e:
        logger.warning(f"Could not fetch history: {e}")
        return []


async def get_all_sessions(limit: int = 100) -> list:
    """All sessions ka list with message counts."""
    db = get_db()
    if db is None:
        return []
    try:
        pipeline = [
            {"$group": {
                "_id":           "$session_id",
                "message_count": {"$sum": 1},
                "last_message":  {"$max": "$created_at"},
                "user_id":       {"$first": "$user_id"},
                "last_intent":   {"$last": "$intent.intent"},
            }},
            {"$sort":  {"last_message": -1}},
            {"$limit": limit},
        ]
        cursor = db.conversations.aggregate(pipeline)
        return await cursor.to_list(length=limit)
    except Exception as e:
        logger.warning(f"Could not fetch sessions: {e}")
        return []