"""FastAPI backend for the BBQ Restaurant AI BI platform (MVP).

Exposes the analytics layer and the AI assistant as a documented REST API.
Business logic lives in :mod:`app.analytics` / :mod:`app.ai_assistant`; these
handlers stay thin (CLAUDE.md sec. 31).

Run:  uvicorn app.main:app --port 8000    (then open http://127.0.0.1:8000/docs)
"""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, Field

from . import analytics, ai_assistant, config, db
from .api.routes import anomalies, websocket, models, auth
from .websocket.monitor import start_realtime_monitor, stop_realtime_monitor
from .security import decode_access_token, ensure_user_table


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app startup and shutdown events.

    Startup: Start the real-time monitoring background task.
    Shutdown: Stop the monitoring task gracefully.
    """
    config.validate_security_config()
    ensure_user_table()
    await start_realtime_monitor()
    yield
    # Shutdown
    await stop_realtime_monitor()


app = FastAPI(
    title="BBQ Restaurant AI BI API",
    version="0.1.0",
    description="Analytics + grounded natural-language assistant over the BBQ dataset.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(config.CORS_ORIGINS),
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.middleware("http")
async def require_api_authentication(request: Request, call_next):
    """Protect all versioned business endpoints with a bearer token."""
    path = request.url.path
    public_paths = {"/api/v1/auth/login", "/api/v1/auth/demo"}
    if path.startswith("/api/v1") and path not in public_paths and request.method != "OPTIONS":
        scheme, _, token = request.headers.get("Authorization", "").partition(" ")
        if scheme.lower() != "bearer" or not token:
            return JSONResponse(status_code=401, content={"detail": "Authentication required"})
        try:
            request.state.user = decode_access_token(token)
        except HTTPException as exc:
            return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    return await call_next(request)

# Include API route routers
app.include_router(anomalies.router)
app.include_router(websocket.router)
app.include_router(models.router)
app.include_router(auth.router)

# Include new products router
from app.api.routes import products
app.include_router(products.router)

API = "/api/v1"


def _run(fn, *args, **kwargs):
    """Call an analytics function, mapping failures to clean HTTP errors."""
    try:
        return fn(*args, **kwargs)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"{type(exc).__name__}: {exc}")


# --------------------------------------------------------------------------
# Schemas
# --------------------------------------------------------------------------
class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500, examples=["Which branch performs best?"])


class ChatResponse(BaseModel):
    question: str
    answer: str
    sql: str | None = None
    source: str
    engine: str
    provider: str | None = None
    model: str | None = None
    rows: list[dict] | None = None
    note: str | None = None


# --------------------------------------------------------------------------
# Meta
# --------------------------------------------------------------------------
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["meta"])
def health():
    db_ok = True
    detail = "connected"
    try:
        db.query_rows("SELECT 1 AS ok")
    except Exception as exc:  # noqa: BLE001
        db_ok = False
        detail = str(exc)
    return {
        "status": "healthy" if db_ok else "degraded",
        "database": detail if db_ok else "unavailable",
        "ai_engine": config.llm_provider() or "deterministic",
        "ai_model": config.llm_model(),
    }


# --------------------------------------------------------------------------
# Dashboard / analytics
# --------------------------------------------------------------------------
@app.get(f"{API}/dashboard/kpis", tags=["dashboard"])
def get_kpis(timeframe: str = Query("all", description="Timeframe filter (today, week, month, quarter, all)")):
    return _run(analytics.kpis, timeframe=timeframe)


@app.get(f"{API}/sales/monthly", tags=["sales"])
def get_monthly():
    return _run(analytics.revenue_by_month)


@app.get(f"{API}/sales/daily", tags=["sales"])
def get_daily():
    return _run(analytics.daily_revenue)


@app.get(f"{API}/sales/by-branch", tags=["sales"])
def get_by_branch():
    return _run(analytics.revenue_by_branch)


@app.get(f"{API}/sales/best-day", tags=["sales"])
def get_best_day():
    return _run(analytics.best_day)


@app.get(f"{API}/sales/weekend-vs-weekday", tags=["sales"])
def get_weekend_vs_weekday():
    return _run(analytics.weekend_vs_weekday)


@app.get(f"{API}/sales/month-compare", tags=["sales"])
def get_month_compare():
    return _run(analytics.month_compare)


@app.get(f"{API}/products/top", tags=["products"])
def get_top_products(limit: int = Query(10, ge=1, le=50)):
    return _run(analytics.top_products, limit)


@app.get(f"{API}/products/categories", tags=["products"])
def get_categories():
    return _run(analytics.category_breakdown)


@app.get(f"{API}/anomalies", tags=["anomalies"])
def get_anomalies(threshold: float = Query(0.6, ge=0.1, le=3.0)):
    return _run(analytics.detect_anomalies, threshold)


# --------------------------------------------------------------------------
# AI assistant
# --------------------------------------------------------------------------
@app.post(f"{API}/ai/chat", response_model=ChatResponse, tags=["ai"])
def ai_chat(req: ChatRequest):
    return _run(ai_assistant.answer_question, req.question)
