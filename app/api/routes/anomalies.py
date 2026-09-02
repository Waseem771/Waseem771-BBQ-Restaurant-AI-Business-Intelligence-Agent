"""
Phase 9.5 - FastAPI Routes for Anomaly Detection
REST API endpoints for anomaly detection system

Endpoints:
- GET /api/v1/anomalies/current - Recent anomalies
- GET /api/v1/anomalies/statistics - Anomaly statistics
- GET /api/v1/anomalies/explain - Explain specific anomaly
- GET /api/v1/anomalies/alerts - Get critical alerts
- GET /api/v1/anomalies/health - Health check

Beginner-friendly with detailed English comments.
"""

import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel, Field

# Add parent directory to path so we can import from app package
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from app.agents.anomaly_tool import AIAgentAnomalyTool

# Initialize anomaly tool
anomaly_tool = AIAgentAnomalyTool()

# Create router
router = APIRouter(
    prefix="/api/v1/anomalies",
    tags=["anomalies"],
    responses={404: {"description": "Not found"}},
)


# ============================================================================
# Response Models (Pydantic schemas for documentation)
# ============================================================================

class AnomalyItem(BaseModel):
    """Single anomaly record"""
    date: str = Field(..., example="2026-03-23")
    severity: str = Field(..., example="HIGH")
    revenue: float = Field(..., example=378868.0)
    orders: int = Field(..., example=199)
    anomaly_score: float = Field(..., example=-0.7172)


class CurrentAnomaliesResponse(BaseModel):
    """Response for current anomalies endpoint"""
    summary: str
    anomalies: List[AnomalyItem]
    count: int
    period_days: int


class StatisticsResponse(BaseModel):
    """Response for statistics endpoint"""
    total_days: int
    anomaly_count: int
    anomaly_percentage: float
    normal_avg_revenue: float
    anomaly_avg_revenue: float
    normal_avg_orders: float
    anomaly_avg_orders: float
    model_type: str
    features_used: int


class AnomalyExplanation(BaseModel):
    """Response for anomaly explanation"""
    date: str
    severity: str
    revenue: float
    orders: int
    anomaly_score: float
    explanation: str
    avg_order_value: float
    orders_per_customer: float


class AlertItem(BaseModel):
    """Single alert record"""
    date: str
    revenue: float
    orders: int
    severity: str
    explanation: str


class AlertsResponse(BaseModel):
    """Response for alerts endpoint"""
    severity: str
    alert_count: int
    alerts: List[AlertItem]


class HealthResponse(BaseModel):
    """Response for health check"""
    status: str
    message: str
    model_status: str
    data_points: int


# ============================================================================
# Endpoints
# ============================================================================

@router.get(
    "/current",
    response_model=CurrentAnomaliesResponse,
    summary="Get Current Anomalies",
    description="Detect anomalies in recent data (last N days)"
)
def get_current_anomalies(
    days: int = Query(7, ge=1, le=90, description="Number of recent days to analyze")
):
    """
    Get anomalies detected in the recent period.

    Parameters:
    - days: Number of recent days to analyze (1-90)

    Returns:
    - Summary of anomalies
    - List of anomalies with details
    - Count and period

    Example:
    GET /api/v1/anomalies/current?days=7
    """
    try:
        result = anomaly_tool.call("detect_current", {"days": days})
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error detecting anomalies: {str(e)}")


@router.get(
    "/statistics",
    response_model=StatisticsResponse,
    summary="Get Anomaly Statistics",
    description="Get overall anomaly detection statistics"
)
def get_anomaly_statistics():
    """
    Get anomaly detection statistics for the entire dataset.

    Returns:
    - Total days analyzed
    - Anomaly count and percentage
    - Revenue comparison (normal vs anomaly days)
    - Order comparison (normal vs anomaly days)
    - Model information

    Example:
    GET /api/v1/anomalies/statistics
    """
    try:
        result = anomaly_tool.call("get_statistics", {})
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting statistics: {str(e)}")


@router.get(
    "/explain",
    response_model=AnomalyExplanation,
    summary="Explain Specific Anomaly",
    description="Get detailed explanation for why a specific date was flagged as anomalous"
)
def explain_anomaly(
    date: str = Query(..., example="2026-03-23", description="Date in YYYY-MM-DD format")
):
    """
    Get detailed explanation for a specific anomalous date.

    Parameters:
    - date: The date to explain (format: YYYY-MM-DD)

    Returns:
    - Date and severity
    - Revenue and order metrics
    - Detailed explanation
    - Anomaly score

    Example:
    GET /api/v1/anomalies/explain?date=2026-03-23
    """
    try:
        result = anomaly_tool.call("explain_anomaly", {"date": date})
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error explaining anomaly: {str(e)}")


@router.get(
    "/alerts",
    response_model=AlertsResponse,
    summary="Get Critical Alerts",
    description="Get alerts of specified severity level"
)
def get_alerts(
    severity: str = Query(
        "HIGH",
        enum=["CRITICAL", "HIGH", "MEDIUM", "LOW"],
        description="Severity level of alerts"
    )
):
    """
    Get alerts of a specific severity level.

    Parameters:
    - severity: Alert severity (CRITICAL, HIGH, MEDIUM, LOW)

    Returns:
    - Severity level
    - Alert count
    - List of alerts with explanations

    Example:
    GET /api/v1/anomalies/alerts?severity=HIGH
    """
    try:
        result = anomaly_tool.call("get_alerts", {"severity": severity})
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting alerts: {str(e)}")


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check if anomaly detection system is healthy"
)
def health_check():
    """
    Check the health status of the anomaly detection system.

    Returns:
    - System status (healthy/degraded/unhealthy)
    - Message with details
    - Model status
    - Data points processed

    Example:
    GET /api/v1/anomalies/health
    """
    try:
        stats = anomaly_tool.call("get_statistics", {})
        return {
            "status": "healthy",
            "message": "Anomaly detection system is operational",
            "model_status": "ready",
            "data_points": stats.get("total_days", 0)
        }
    except Exception as e:
        return {
            "status": "degraded",
            "message": f"Anomaly detection system error: {str(e)}",
            "model_status": "error",
            "data_points": 0
        }


# Export router for integration into main FastAPI app
__all__ = ["router"]
