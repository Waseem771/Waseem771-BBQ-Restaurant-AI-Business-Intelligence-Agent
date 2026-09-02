"""FastAPI backend for the BBQ Restaurant AI BI platform (MVP).

Exposes the analytics layer and the AI assistant as a documented REST API.
Business logic lives in :mod:`app.analytics` / :mod:`app.ai_assistant`; these
handlers stay thin (CLAUDE.md sec. 31).

Run:  uvicorn app.main:app --port 8000    (then open http://127.0.0.1:8000/docs)
"""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

from . import analytics, ai_assistant, config, db
from .api.routes import anomalies, websocket, models, auth
from .websocket.monitor import start_realtime_monitor, stop_realtime_monitor


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app startup and shutdown events.

    Startup: Start the real-time monitoring background task.
    Shutdown: Stop the monitoring task gracefully.
    """
    # Startup
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

# Permissive CORS for local development (dashboard / future frontends).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API route routers
app.include_router(anomalies.router)
app.include_router(websocket.router)
app.include_router(models.router)
app.include_router(auth.router)

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
def get_kpis():
    return _run(analytics.kpis)


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
