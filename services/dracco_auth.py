import hashlib
import secrets
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

logger = logging.getLogger(__name__)

# Simple in-memory token store (for MVP)
_tokens: dict[str, dict] = {}

LEVEL_LABELS = {
    100: "Admin Master",
    80: "Super Usuário",
    60: "Gerente de Base",
    40: "Auxiliar",
    30: "Motorista",
    20: "Entregador",
}

LEVEL_ROLES = {
    100: ["ADMINISTRADOR", "GESTOR", "AUXILIAR", "MOTORISTA", "ENTREGADOR"],
    80: ["GESTOR", "AUXILIAR", "MOTORISTA", "ENTREGADOR"],
    60: ["GESTOR", "AUXILIAR", "MOTORISTA", "ENTREGADOR"],
    40: ["AUXILIAR"],
    30: ["MOTORISTA"],
    20: ["ENTREGADOR"],
}

SESSION_TIMEOUT_HOURS = 1


def hash_password(password: str) -> str:
    """Hash password with SHA-256 + salt."""
    salt = "dracco_salt_2026"
    return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash."""
    return hash_password(password) == hashed


def create_token(user_id: int, user_data: dict) -> str:
    """Create a session token."""
    token = secrets.token_hex(32)
    _tokens[token] = {
        "user_id": user_id,
        "user_data": user_data,
        "created_at": datetime.now(timezone.utc),
        "last_activity": datetime.now(timezone.utc),
    }
    return token


def validate_token(token: str) -> Optional[dict]:
    """Validate token and check expiry."""
    if not token or token not in _tokens:
        return None
    session = _tokens[token]
    elapsed = datetime.now(timezone.utc) - session["last_activity"]
    if elapsed > timedelta(hours=SESSION_TIMEOUT_HOURS):
        del _tokens[token]
        return None
    session["last_activity"] = datetime.now(timezone.utc)
    return session["user_data"]


def invalidate_token(token: str):
    """Remove a token."""
    _tokens.pop(token, None)


def get_roles_for_level(level: int) -> list[str]:
    """Get available roles for a given level."""
    return LEVEL_ROLES.get(level, [])


def get_level_label(level: int) -> str:
    """Get human-readable label for level."""
    return LEVEL_LABELS.get(level, f"Nível {level}")


def get_all_online_tokens() -> list[dict]:
    """Get all active sessions."""
    now = datetime.now(timezone.utc)
    active = []
    expired_keys = []
    for token, session in _tokens.items():
        elapsed = now - session["last_activity"]
        if elapsed > timedelta(hours=SESSION_TIMEOUT_HOURS):
            expired_keys.append(token)
        else:
            data = session["user_data"].copy()
            data["active_since"] = session["created_at"].isoformat()
            data["last_activity"] = session["last_activity"].isoformat()
            active.append(data)
    for k in expired_keys:
        del _tokens[k]
    return active