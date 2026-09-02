"""Real-time event dispatcher for anomalies, forecasts, and metrics.

Bridges analytics/ML engines with WebSocket clients by:
- Subscribing to anomaly detection events
- Publishing forecast notifications
- Aggregating system metrics
- Routing events to appropriate clients
"""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Any, Callable

from .manager import ConnectionManager
from .schemas import (
    AlertSeverity,
    AnomalyAlert,
    ForecastAlert,
    KPIUpdateMessage,
    MessageType,
    MetricsUpdateMessage,
    SystemStatusMessage,
)

logger = logging.getLogger(__name__)


class EventDispatcher:
    """Routes real-time events to WebSocket clients.

    Subscribes to events from:
    - Anomaly detector
    - Forecast engine
    - Analytics pipeline
    - System health monitor

    Transforms events into WebSocket messages and broadcasts to clients.
    """

    def __init__(self, connection_manager: ConnectionManager):
        """Initialize dispatcher with connection manager.

        Args:
            connection_manager: Shared ConnectionManager instance
        """
        self.manager = connection_manager
        self.event_handlers: dict[str, list[Callable]] = {}
        self.event_history: dict[str, list[dict]] = {}
        self.max_history = 100  # Keep last N events per type

    def subscribe(self, event_type: str, handler: Callable):
        """Register a handler for an event type.

        Args:
            event_type: Event category (e.g., 'anomaly', 'forecast')
            handler: Async callable(event_data) -> None
        """
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
        logger.info(f"Subscribed handler to {event_type}")

    async def publish(self, event_type: str, event_data: dict):
        """Publish an event to all subscribed handlers.

        Args:
            event_type: Event category
            event_data: Event payload
        """
        # Store in history
        if event_type not in self.event_history:
            self.event_history[event_type] = []
        self.event_history[event_type].append(
            {
                "timestamp": datetime.utcnow().isoformat(),
                "data": event_data,
            }
        )
        # Trim history
        if len(self.event_history[event_type]) > self.max_history:
            self.event_history[event_type] = self.event_history[event_type][-self.max_history :]

        # Invoke handlers
        handlers = self.event_handlers.get(event_type, [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event_data)
                else:
                    handler(event_data)
            except Exception as exc:
                logger.error(f"Handler error for {event_type}: {exc}")

    async def broadcast_anomaly(
        self,
        anomaly_id: str,
        metric: str,
        value: float,
        expected_value: float,
        severity: AlertSeverity,
        description: str,
        branch_id: int | None = None,
        model_version: str | None = None,
    ):
        """Broadcast anomaly detection alert to all clients.

        Args:
            anomaly_id: Unique anomaly identifier
            metric: Metric with anomaly (e.g., 'revenue')
            value: Actual value
            expected_value: Expected/normal value
            severity: Alert severity level
            description: Human-readable description
            branch_id: Optional branch identifier
            model_version: Version of detection model
        """
        deviation_percent = abs((value - expected_value) / expected_value * 100) if expected_value else 0

        message = AnomalyAlert(
            anomaly_id=anomaly_id,
            metric=metric,
            value=value,
            expected_value=expected_value,
            deviation_percent=deviation_percent,
            severity=severity,
            branch_id=branch_id,
            description=description,
            model_version=model_version,
        )

        await self.manager.broadcast(message.model_dump())
        await self.publish("anomaly", message.model_dump())

    async def broadcast_forecast(
        self,
        forecast_period: str,
        metric: str,
        predicted_value: float,
        confidence: float,
        trend: str,
        recommendation: str | None = None,
        branch_id: int | None = None,
    ):
        """Broadcast forecast-based alert or insight to all clients.

        Args:
            forecast_period: Time period (e.g., 'next_7_days', 'next_month')
            metric: What is being forecasted
            predicted_value: Predicted value
            confidence: Confidence 0.0-1.0
            trend: Direction (up, down, stable)
            recommendation: Optional actionable recommendation
            branch_id: Optional branch identifier
        """
        message = ForecastAlert(
            forecast_period=forecast_period,
            metric=metric,
            predicted_value=predicted_value,
            confidence=confidence,
            trend=trend,
            recommendation=recommendation,
            branch_id=branch_id,
        )

        await self.manager.broadcast(message.model_dump())
        await self.publish("forecast", message.model_dump())

    async def broadcast_kpi_update(
        self,
        kpis: dict[str, Any],
        interval: str = "hourly",
    ):
        """Broadcast KPI batch update to all clients.

        Args:
            kpis: Dict of KPI name -> value
            interval: Update interval description
        """
        message = KPIUpdateMessage(kpis=kpis, interval=interval)

        await self.manager.broadcast(message.model_dump())
        await self.publish("kpi_update", message.model_dump())

    async def broadcast_metric_update(
        self,
        metric_name: str,
        value: float | int,
        previous_value: float | int | None = None,
        branch_id: int | None = None,
    ):
        """Broadcast single metric update to all clients.

        Args:
            metric_name: Name of metric
            value: Current value
            previous_value: Previous value (for delta calculation)
            branch_id: Optional branch identifier
        """
        change_percent = None
        if previous_value is not None and previous_value != 0:
            change_percent = ((value - previous_value) / previous_value) * 100

        message = MetricsUpdateMessage(
            metric_name=metric_name,
            value=value,
            previous_value=previous_value,
            change_percent=change_percent,
            branch_id=branch_id,
        )

        await self.manager.broadcast(message.model_dump())
        await self.publish("metric_update", message.model_dump())

    async def broadcast_system_status(
        self,
        status: str,
        database: str,
        ai_engine: str | None = None,
        ml_engine: str | None = None,
        message_text: str | None = None,
    ):
        """Broadcast system health status to all clients.

        Args:
            status: Overall status (healthy, degraded, unhealthy)
            database: Database status
            ai_engine: AI service status
            ml_engine: ML service status
            message_text: Optional status message
        """
        message = SystemStatusMessage(
            status=status,
            database=database,
            ai_engine=ai_engine,
            ml_engine=ml_engine,
            active_connections=self.manager.get_active_count(),
            message=message_text,
        )

        await self.manager.broadcast(message.model_dump())

    async def broadcast_to_branch(
        self,
        branch_id: int,
        message: dict,
    ):
        """Broadcast message to clients connected for specific branch.

        Args:
            branch_id: Target branch
            message: Message dict to send
        """

        def filter_fn(client_id: str, metadata: dict) -> bool:
            return metadata.get("branch_id") == branch_id or metadata.get("branch_id") is None

        await self.manager.broadcast_filtered(message, filter_fn)

    def get_event_history(self, event_type: str, limit: int = 20) -> list[dict]:
        """Get recent events of a specific type.

        Args:
            event_type: Event category
            limit: Max number of events to return

        Returns:
            List of recent events
        """
        events = self.event_history.get(event_type, [])
        return events[-limit:]


# Global dispatcher instance
dispatcher: EventDispatcher | None = None


def init_dispatcher(manager: ConnectionManager) -> EventDispatcher:
    """Initialize global event dispatcher.

    Args:
        manager: Connection manager instance

    Returns:
        Initialized EventDispatcher
    """
    global dispatcher
    dispatcher = EventDispatcher(manager)
    return dispatcher


def get_dispatcher() -> EventDispatcher:
    """Get global dispatcher instance.

    Raises:
        RuntimeError: If dispatcher not initialized
    """
    if dispatcher is None:
        raise RuntimeError("Event dispatcher not initialized. Call init_dispatcher() first.")
    return dispatcher
