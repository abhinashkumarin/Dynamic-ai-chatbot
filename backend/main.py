"""
Dynamic AI Chatbot — FastAPI Backend
WebSocket + REST API + Analytics + MongoDB
"""

import asyncio
from contextlib import asynccontextmanager
from datetime import datetime

import socketio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import Response
from loguru import logger

from app.api import chat, analytics, auth, websocket
from app.core.config import settings
from app.core.database import connect_db, disconnect_db
from app.services.nlp_engine import nlp_engine
from app.services.ml_model import ml_model
from app.services.analytics_service import analytics_service


# ─── Lifespan ─────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting Dynamic AI Chatbot Server...")
    await connect_db()
    await nlp_engine.initialize()
    logger.info("🧠 NLP Engine v5.0 initialized")
    await ml_model.initialize()
    logger.info("🤖 ML Model initialized")
    logger.info(f"✅ Server ready at http://{settings.HOST}:{settings.PORT}")
    logger.info("📡 WebSocket: Active | REST API: Active | Analytics: Active")
    yield
    logger.info("🛑 Shutting down...")
    await disconnect_db()


# ─── FastAPI App ──────────────────────────────────────────────────────────────
app = FastAPI(
    title       = "Dynamic AI Chatbot API",
    description = "Advanced NLP-powered conversational AI — Internship Project",
    version     = "5.0.0",
    docs_url    = "/docs",
    redoc_url   = "/redoc",
    lifespan    = lifespan,
)

# ─── Middleware ───────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# ─── Socket.IO ────────────────────────────────────────────────────────────────
sio = socketio.AsyncServer(
    async_mode       = "asgi",
    cors_allowed_origins = "*",
    logger           = False,
    engineio_logger  = False,
)
socket_app        = socketio.ASGIApp(sio, other_asgi_app=app)
app.state.sio     = sio

# ─── Routers ─────────────────────────────────────────────────────────────────
app.include_router(auth.router,      prefix="/api/auth",      tags=["Auth"])
app.include_router(chat.router,      prefix="/api/chat",      tags=["Chat"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(websocket.router, prefix="/api/ws",        tags=["WS Info"])


# ─── Favicon (remove 404 noise) ───────────────────────────────────────────────
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)


# ─── Health Check ─────────────────────────────────────────────────────────────
@app.get("/api/health", tags=["Health"])
async def health_check():
    stats = analytics_service.get_stats()
    return {
        "status":       "healthy",
        "version":      "5.0.0",
        "nlp_engine":   nlp_engine.is_ready,
        "ml_model":     ml_model.is_ready,
        "environment":  settings.ENVIRONMENT,
        "total_messages": stats["total_messages"],
        "total_sessions": stats["total_sessions"],
    }


# ─── Socket.IO Events ─────────────────────────────────────────────────────────
connected_users: dict = {}


@sio.event
async def connect(sid, environ, auth=None):
    connected_users[sid] = {"session_id": None, "message_count": 0}
    await sio.emit("connected", {
        "socket_id": sid,
        "message":   "Connected to Dynamic AI Chatbot! 🤖",
    }, to=sid)
    await sio.emit("user_count", {"count": len(connected_users)})
    logger.info(f"🔌 Socket connected: {sid}")


@sio.event
async def disconnect(sid):
    connected_users.pop(sid, None)
    await sio.emit("user_count", {"count": len(connected_users)})
    logger.info(f"🔌 Socket disconnected: {sid}")


@sio.event
async def chat_message(sid, data):
    message    = data.get("message", "").strip()
    session_id = data.get("session_id", sid)
    user_id    = data.get("user_id")

    if not message or len(message) > 1000:
        await sio.emit("error", {"message": "Invalid message"}, to=sid)
        return

    if sid in connected_users:
        connected_users[sid]["session_id"]    = session_id
        connected_users[sid]["message_count"] += 1

    await sio.emit("bot_typing", {"typing": True}, to=sid)

    try:
        # Natural typing delay
        await asyncio.sleep(0.3 + len(message) * 0.003)

        # ── NLP Pipeline ──────────────────────────────────────────────────────
        result  = await nlp_engine.process(message, session_id)
        ml_pred = ml_model.predict(message)

        # ── Track Analytics ───────────────────────────────────────────────────
        analytics_service.track(
            intent             = result["metadata"]["intent"]["intent"],
            sentiment_label    = result["metadata"]["sentiment"]["label"],
            processing_time_ms = result["metadata"]["processing_time_ms"],
            confidence         = result["metadata"]["intent"]["confidence"],
            session_id         = session_id,
        )

        # ── Save to MongoDB ───────────────────────────────────────────────────
        from app.core.database import get_db
        db = get_db()
        if db is not None:
            try:
                await db.conversations.insert_one({
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
                    "source":             "websocket",
                    "created_at":         datetime.utcnow(),
                })
                logger.debug(f"💾 WS conversation saved: {session_id}")
            except Exception as db_err:
                logger.warning(f"⚠️ WS DB save failed: {db_err}")

        await sio.emit("bot_typing", {"typing": False}, to=sid)
        await sio.emit("bot_response", {
            "message":    result["response"],
            "metadata":   {**result["metadata"], "ml_prediction": ml_pred},
            "session_id": session_id,
        }, to=sid)

    except Exception as e:
        logger.error(f"Socket message error: {e}")
        await sio.emit("bot_typing",   {"typing": False}, to=sid)
        await sio.emit("bot_response", {
            "message":  "⚠️ Temporary glitch. Please try again!",
            "metadata": {"intent": {"intent": "error", "confidence": 0},
                         "sentiment": {"label": "neutral", "score": 0, "emoji": "😐",
                                       "positive_words": [], "negative_words": []}},
        }, to=sid)


@sio.event
async def user_typing(sid, data):
    pass  # Future: broadcast to admin dashboard


@sio.event
async def clear_session(sid, data):
    session_id = data.get("session_id", sid)
    nlp_engine.context_manager.clear_session(session_id)
    await sio.emit("session_cleared", {"session_id": session_id}, to=sid)


@sio.event
async def feedback(sid, data):
    message_content = data.get("message_content", "")
    correct_intent  = data.get("correct_intent")
    was_helpful     = data.get("was_helpful", True)
    if correct_intent and message_content:
        ml_model.add_feedback(message_content, correct_intent, was_helpful)
    await sio.emit("feedback_received", {"message": "Thank you! 🙏"}, to=sid)


# ─── Run ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run(
        "main:socket_app",
        host      = settings.HOST,
        port      = settings.PORT,
        reload    = settings.DEBUG,
        log_level = "info",
    )