"""
Analytics API — Fully Working
Sab endpoints properly data return karte hain
"""

import time
from datetime import datetime
from fastapi import APIRouter

from app.services.analytics_service import analytics_service
from app.services.nlp_engine import nlp_engine
from app.services.ml_model import ml_model

router = APIRouter()

_start_time = time.time()


@router.get("/dashboard")
async def get_dashboard():
    """Full analytics dashboard — sab data ek jagah."""
    stats    = analytics_service.get_stats()
    ml_stats = ml_model.get_stats()

    # System stats
    try:
        import psutil
        mem = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=0.1)
        memory_mb = round(mem.used / 1024 / 1024, 1)
    except Exception:
        memory_mb = 0
        cpu       = 0

    uptime = int(time.time() - _start_time)

    return {
        "realtime": {
            "server_uptime_seconds": uptime,
            "memory_usage_mb":       memory_mb,
            "cpu_percent":           cpu,
            "nlp_engine_ready":      nlp_engine.is_ready,
            "ml_model_ready":        ml_model.is_ready,
            "active_sessions":       len(nlp_engine.context_manager.sessions),
        },
        "session_stats": {
            "total_messages":         stats.get("total_messages", 0),
            "total_sessions":         stats.get("total_sessions", 0),
            "avg_response_time_ms":   stats.get("avg_response_time_ms", 0),
            "avg_confidence":         stats.get("avg_confidence", 0),
            "intent_distribution":    stats.get("intent_distribution", {}),
            "sentiment_distribution": stats.get("sentiment_distribution", {}),
            "hourly_activity":        stats.get("hourly_activity", {}),
            "uptime_seconds":         stats.get("uptime_seconds", 0),
        },
        "model_stats": {
            "is_ready":       ml_stats.get("is_ready", False),
            "feedback_count": ml_stats.get("feedback_count", 0),
            "retrain_count":  ml_stats.get("retrain_count", 0),
            "architecture":   ml_stats.get("architecture", "MLP [9→64→32→16→7]"),
            "features":       ml_stats.get("features", []),
            "output_labels":  ml_stats.get("output_labels", []),
        },
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/intents")
async def get_intent_stats():
    """Intent distribution data."""
    stats = analytics_service.get_stats()
    dist  = stats.get("intent_distribution", {})
    total = sum(dist.values()) if dist else 0
    return {
        "distribution": dist,
        "total":        total,
        "top_intent":   max(dist, key=dist.get) if dist else None,
        "intent_count": len(dist),
    }


@router.get("/sentiment")
async def get_sentiment_stats():
    """Sentiment breakdown."""
    stats = analytics_service.get_stats()
    dist  = stats.get("sentiment_distribution", {})
    total = sum(dist.values()) if dist else 0
    positive = dist.get("positive", 0) + dist.get("very_positive", 0)
    negative = dist.get("negative", 0) + dist.get("very_negative", 0)
    return {
        "distribution":    dist,
        "total":           total,
        "positivity_rate": round(positive / total * 100, 1) if total else 0,
        "negativity_rate": round(negative / total * 100, 1) if total else 0,
    }


@router.get("/performance")
async def get_performance():
    """Performance metrics."""
    stats = analytics_service.get_stats()
    return {
        "avg_response_time_ms": stats.get("avg_response_time_ms", 0),
        "avg_confidence":       stats.get("avg_confidence", 0),
        "total_messages":       stats.get("total_messages", 0),
        "total_sessions":       stats.get("total_sessions", 0),
        "hourly_activity":      stats.get("hourly_activity", {}),
    }


@router.get("/sessions")
async def get_sessions():
    """Active sessions info."""
    sessions = nlp_engine.context_manager.sessions
    session_list = []
    for sid, data in list(sessions.items())[:20]:
        session_list.append({
            "session_id":    sid[:8] + "...",
            "turn_count":    data.get("turn_count", 0),
            "last_intent":   data.get("last_intent"),
            "last_emotion":  data.get("last_emotion"),
            "has_been_sad":  data.get("has_been_sad", False),
            "created_at":    data.get("created_at", datetime.utcnow()).isoformat(),
        })
    return {
        "active_sessions": len(sessions),
        "sessions":        session_list,
    }