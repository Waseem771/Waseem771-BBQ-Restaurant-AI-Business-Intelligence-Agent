"""Authentication primitives for the API.

Passwords are stored as PBKDF2 hashes and access tokens are signed JWTs.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status

from . import config, db

_HASH_ITERATIONS = 600_000


def hash_password(password: str) -> str:
    """Create a salted PBKDF2-SHA256 password hash."""
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, _HASH_ITERATIONS)
    return "pbkdf2_sha256${}${}${}".format(
        _HASH_ITERATIONS, base64.urlsafe_b64encode(salt).decode(), base64.urlsafe_b64encode(digest).decode()
    )


def verify_password(password: str, encoded: str) -> bool:
    """Constant-time verification for hashes created by :func:`hash_password`."""
    try:
        algorithm, iterations, salt, expected = encoded.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), base64.urlsafe_b64decode(salt), int(iterations))
        return hmac.compare_digest(actual, base64.urlsafe_b64decode(expected))
    except (TypeError, ValueError):
        return False


def create_access_token(subject: str, role: str) -> str:
    now = datetime.now(timezone.utc)
    return jwt.encode(
        {"sub": subject, "role": role, "iat": now, "exp": now + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)},
        config.JWT_SECRET_KEY,
        algorithm="HS256",
    )


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, config.JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


def ensure_user_table() -> None:
    """Create the minimal local user table if the SQLite data store exists."""
    db.execute_write(
        """CREATE TABLE IF NOT EXISTS app_users (
            id TEXT PRIMARY KEY, username TEXT NOT NULL UNIQUE, email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL, name TEXT NOT NULL, role TEXT NOT NULL DEFAULT 'Manager',
            title TEXT NOT NULL DEFAULT 'Restaurant Manager', status TEXT NOT NULL DEFAULT 'Active',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )"""
    )
