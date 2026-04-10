"""WebSocket info endpoint."""
from fastapi import APIRouter

router = APIRouter()

@router.get("/info")
async def websocket_info():
    return {
        "protocol": "Socket.IO",
        "url": "ws://localhost:8000",
        "events": {
            "client_to_server": ["chat_message", "user_typing", "clear_session", "feedback"],
            "server_to_client": ["connected", "bot_typing", "bot_response", "user_count", "session_cleared", "feedback_received"],
        },
        "docs": "Connect via socket.io-client from frontend",
    }
