"""User Authentication and Account Management API Routes.

Provides endpoints for:
- POST /api/v1/auth/login - Login user with username/email and password
- GET /api/v1/auth/users - List user accounts (Administrator only)
- GET /api/v1/auth/me - Current user details
"""

import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

# Add parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

# User Database / Account Registry
USERS_DB = [
    {
        "id": "usr_001",
        "username": "waseem",
        "email": "waseem@bbqrestaurant.com",
        "password": "iba@123",
        "name": "Waseem",
        "role": "Administrator",
        "title": "Account Manager",
        "status": "Active",
        "permissions": ["all", "read", "write", "admin", "dashboard_access", "settings_access"],
        "createdAt": "2026-01-01T00:00:00Z"
    },
    {
        "id": "usr_002",
        "username": "demo",
        "email": "demo@bbqrestaurant.com",
        "password": "demo",
        "name": "Demo Manager",
        "role": "Manager",
        "title": "Restaurant Manager",
        "status": "Active",
        "permissions": ["read", "dashboard_access"],
        "createdAt": "2026-01-15T00:00:00Z"
    }
]

# Schemas
class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, description="Username or Email address")
    password: str = Field(..., min_length=1, description="Account password")

class UserProfile(BaseModel):
    id: str
    username: str
    email: str
    name: str
    role: str
    title: str
    status: str
    permissions: List[str]

class LoginResponse(BaseModel):
    success: bool
    message: str
    token: str
    user: UserProfile
    loginTime: str

@router.post("/login", response_model=LoginResponse)
def login(req: LoginRequest):
    """Authenticate user with username/email and password."""
    target = req.username.strip().lower()
    
    user = None
    for u in USERS_DB:
        if u["username"].lower() == target or u["email"].lower() == target:
            if u["password"] == req.password:
                user = u
                break
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username/email or password")
    
    user_profile = UserProfile(
        id=user["id"],
        username=user["username"],
        email=user["email"],
        name=user["name"],
        role=user["role"],
        title=user["title"],
        status=user["status"],
        permissions=user["permissions"]
    )
    
    return LoginResponse(
        success=True,
        message="Login successful",
        token=f"token_bbq_{user['id']}_{int(datetime.now().timestamp())}",
        user=user_profile,
        loginTime=datetime.now().isoformat()
    )

@router.get("/users", response_model=List[UserProfile])
def get_users():
    """List registered user accounts in the system."""
    return [
        UserProfile(
            id=u["id"],
            username=u["username"],
            email=u["email"],
            name=u["name"],
            role=u["role"],
            title=u["title"],
            status=u["status"],
            permissions=u["permissions"]
        )
        for u in USERS_DB
    ]

@router.get("/me", response_model=UserProfile)
def get_current_user(username: Optional[str] = Query("waseem")):
    """Get current user details."""
    target = username.lower()
    for u in USERS_DB:
        if u["username"].lower() == target or u["email"].lower() == target:
            return UserProfile(
                id=u["id"],
                username=u["username"],
                email=u["email"],
                name=u["name"],
                role=u["role"],
                title=u["title"],
                status=u["status"],
                permissions=u["permissions"]
            )
    
    # Default fallback to waseem admin
    u = USERS_DB[0]
    return UserProfile(
        id=u["id"],
        username=u["username"],
        email=u["email"],
        name=u["name"],
        role=u["role"],
        title=u["title"],
        status=u["status"],
        permissions=u["permissions"]
    )
