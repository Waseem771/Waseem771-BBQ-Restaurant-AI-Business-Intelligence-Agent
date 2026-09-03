"""Message schemas for WebSocket communication.

Defines the structure of all real-time messages flowing between
server and dashboard clients.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class MessageType(str, Enum):
    """Types of WebSocket messages."""

    # Dashboard metrics
    METRICS_UPDATE = "metrics_update"
    KPI_UPDATE = "kpi_update"

    # Alerts
    ANOMALY_DETECTED = "anomaly_detected"
    FORECAST_ALERT = "forecast_alert"
    ALERT_RESOLVED = "alert_resolved"

    # Status
    SYSTEM_STATUS = "system_status"
    CONNECTION_ACK = "connection_ack"

    # Real-time data
    SALES_UPDATE = "sales_update"
    ORDER_UPDATE = "order_update"
    INVENTORY_UPDATE = "inventory_update"


class AlertSeverity(str, Enum):
    """Alert severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class BaseMessage(BaseModel):
    """Base schema for all WebSocket messages.

    Every message includes:
    - type: Message category
    - timestamp: When the message was generated
    - client_id: Target client (optional, for routing)
    """

    model_config = ConfigDict(
        ser_json_timedelta="float",
        ser_json_bytes="utf8",
    )

    type: MessageType
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    client_id: str | None = None


class MetricsUpdateMessage(BaseMessage):
    """Real-time metrics update for dashboard.

    Sent when KPIs or analytics change.
    """

    type: MessageType = MessageType.METRICS_UPDATE
    metric_name: str = Field(..., description="Name of metric (e.g., 'total_revenue')")
    value: float | int
    previous_value: float | int | None = None
    change_percent: float | None = None
    branch_id: int | None = None


class KPIUpdateMessage(BaseMessage):
    """Key Performance Indicator batch update.

    Sent periodically or on significant changes.
    """

    type: MessageType = MessageType.KPI_UPDATE
    kpis: dict[str, Any] = Field(
        ...,
        description="Dict of KPI name -> value (total_revenue, avg_order_value, etc.)",
    )
    interval: str = Field(default="hourly", description="Update interval (hourly, daily, etc.)")


class AnomalyAlert(BaseMessage):
    """Alert for detected anomaly.

    Triggered when anomaly detection identifies unusual behavior.
    """

    type: MessageType = MessageType.ANOMALY_DETECTED
    anomaly_id: str
    metric: str = Field(..., description="What metric has an anomaly (revenue, orders, etc.)")
    value: float
    expected_value: float
    deviation_percent: float = Field(..., description="Deviation from expected as percentage")
    severity: AlertSeverity
    branch_id: int | None = None
    description: str = Field(..., description="Human-readable anomaly description")
    model_version: str | None = None


class ForecastAlert(BaseMessage):
    """Alert for forecast-based insights.

    Notifies about predicted sales changes, trends, or issues.
    """

    type: MessageType = MessageType.FORECAST_ALERT
    forecast_period: str = Field(..., description="e.g., 'next_7_days', 'next_month'")
    metric: str = Field(..., description="What is being forecasted")
    predicted_value: float
    confidence: float = Field(..., description="Confidence 0.0-1.0")
    trend: str = Field(..., description="up, down, stable")
    recommendation: str | None = None
    branch_id: int | None = None


class AlertResolvedMessage(BaseMessage):
    """Notification that an alert has been resolved.

    Sent when anomaly is no longer detected or condition clears.
    """

    type: MessageType = MessageType.ALERT_RESOLVED
    alert_id: str
    reason: str = Field(..., description="Why alert was resolved")
    resolved_at: datetime = Field(default_factory=datetime.utcnow)


class SystemStatusMessage(BaseMessage):
    """System health and status update.

    Sent on connection and periodically during operation.
    """

    type: MessageType = MessageType.SYSTEM_STATUS
    status: str = Field(..., description="healthy, degraded, unhealthy")
    database: str = Field(..., description="connected, unavailable")
    ai_engine: str | None = None
    ml_engine: str | None = None
    active_connections: int | None = None
    message: str | None = None


class ConnectionAckMessage(BaseMessage):
    """Acknowledgment of connection establishment.

    Sent when client first connects successfully.
    """

    type: MessageType = MessageType.CONNECTION_ACK
    client_id: str
    server_version: str = "1.0.0"
    features: list[str] = Field(
        default_factory=lambda: [
            "metrics",
            "anomalies",
            "forecasts",
            "alerts",
        ]
    )


class SalesUpdateMessage(BaseMessage):
    """Real-time sales update.

    Could be sent on new orders or at regular intervals.
    """

    type: MessageType = MessageType.SALES_UPDATE
    branch_id: int | None = None
    current_sales: float
    today_sales: float
    today_target: float | None = None
    target_progress_percent: float | None = None
    order_count: int | None = None


# Union type for all possible messages
WebSocketMessage = (
    MetricsUpdateMessage
    | KPIUpdateMessage
    | AnomalyAlert
    | ForecastAlert
    | AlertResolvedMessage
    | SystemStatusMessage
    | ConnectionAckMessage
    | SalesUpdateMessage
)
