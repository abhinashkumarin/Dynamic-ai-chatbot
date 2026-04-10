"""Authentication REST API Endpoints."""

import uuid
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from loguru import logger

from app.core.config import settings
from app.core.database import get_db
from app.models.schemas import UserRegister, UserLogin, TokenResponse

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# In-memory user store (fallback when no MongoDB)
_users_store: dict[str, dict] = {}


def create_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({**data, "exp": expire}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


@router.post("/register", response_model=TokenResponse)
async def register(body: UserRegister):
    db = get_db()
    user_id = str(uuid.uuid4())

    if db is not None:
        try:
            existing = await db.users.find_one({"username": body.username})
            if existing:
                raise HTTPException(400, "Username already taken")
            user = {
                "_id": user_id, "username": body.username,
                "email": body.email, "password_hash": hash_password(body.password),
                "role": "user", "created_at": datetime.utcnow(),
            }
            await db.users.insert_one(user)
        except HTTPException:
            raise
        except Exception as e:
            logger.warning(f"DB register failed: {e}")

    # In-memory fallback
    if body.username in _users_store:
        raise HTTPException(400, "Username already taken")
    _users_store[body.username] = {
        "id": user_id, "username": body.username,
        "password_hash": hash_password(body.password), "role": "user",
    }

    token = create_token({"sub": body.username, "user_id": user_id, "role": "user"})
    return TokenResponse(
        access_token=token,
        user={"id": user_id, "username": body.username, "role": "user"},
    )


@router.post("/login", response_model=TokenResponse)
async def login(body: UserLogin):
    db = get_db()

    # Try MongoDB
    if db is not None:
        try:
            user = await db.users.find_one({"username": body.username})
            if user and verify_password(body.password, user["password_hash"]):
                token = create_token({"sub": user["username"], "user_id": str(user["_id"]), "role": user.get("role", "user")})
                return TokenResponse(
                    access_token=token,
                    user={"id": str(user["_id"]), "username": user["username"], "role": user.get("role", "user")},
                )
        except Exception as e:
            logger.debug(f"DB login failed: {e}")

    # In-memory fallback
    user = _users_store.get(body.username)
    if not user or not verify_password(body.password, user["password_hash"]):
        raise HTTPException(401, "Invalid credentials")

    token = create_token({"sub": user["username"], "user_id": user["id"], "role": user["role"]})
    return TokenResponse(
        access_token=token,
        user={"id": user["id"], "username": user["username"], "role": user["role"]},
    )


@router.get("/verify")
async def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return {"valid": True, "user": payload}
    except JWTError:
        raise HTTPException(401, "Invalid or expired token")
