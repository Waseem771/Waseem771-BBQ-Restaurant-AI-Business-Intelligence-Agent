"""Authentication routes backed by hashed credentials in the local data store."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from ... import db
from ...config import ACCESS_TOKEN_EXPIRE_MINUTES, DEMO_MODE
from ...security import create_access_token, ensure_user_table, verify_password

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=254)
    password: str = Field(..., min_length=1, max_length=256)


class UserProfile(BaseModel):
    id: str
    username: str
    email: str
    name: str
    role: str
    title: str
    status: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserProfile


def _profile(row: dict) -> UserProfile:
    return UserProfile(
        id=row["id"], username=row["username"], email=row["email"], name=row["name"],
        role=row["role"], title=row["title"], status=row["status"],
    )


@router.post("/login", response_model=LoginResponse)
def login(req: LoginRequest) -> LoginResponse:
    ensure_user_table()
    identifier = req.username.strip().lower()
    rows = db.query_rows("SELECT * FROM app_users WHERE username = ? OR email = ? LIMIT 1", (identifier, identifier))
    if not rows or rows[0]["status"] != "Active" or not verify_password(req.password, rows[0]["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    user = _profile(rows[0])
    return LoginResponse(
        access_token=create_access_token(user.id, user.role),
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=user,
    )


@router.post("/demo", response_model=LoginResponse, include_in_schema=False)
def demo_login() -> LoginResponse:
    """Development-only demo endpoint; disabled unless DEMO_MODE=true."""
    if not DEMO_MODE:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Demo access is disabled")
    user = UserProfile(
        id="demo", username="demo", email="demo@example.invalid", name="Demo Manager",
        role="Manager", title="Restaurant Manager", status="Active",
    )
    return LoginResponse(
        access_token=create_access_token(user.id, user.role),
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=user,
    )
