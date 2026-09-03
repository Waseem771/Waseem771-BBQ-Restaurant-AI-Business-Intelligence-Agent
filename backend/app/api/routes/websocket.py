"""WebSocket routes for real-time dashboard and alert streaming.

Handles client connections, subscriptions, and integration with
anomaly detection and forecasting engines.
"""
from __future__ import annotations

import logging
import uuid
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query

from ...websocket.manager import ConnectionManager
from ...websocket.dispatcher import EventDispatcher, init_dispatcher, get_dispatcher
from ...websocket.schemas import ConnectionAckMessage, MessageType

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ws", tags=["websocket"])

# Initialize connection manager and dispatcher
connection_manager = ConnectionManager()
event_dispatcher = init_dispatcher(connection_manager)


@router.websocket("/dashboard")
async def websocket_dashboard(
    websocket: WebSocket,
    branch_id: int | None = Query(None),
    user_id: str | None = Query(None),
):
    """WebSocket endpoint for real-time dashboard updates.

    Clients connect here to receive:
    - KPI updates
    - Anomaly alerts
    - Forecast notifications
    - System status

    Query Parameters:
        branch_id: Optional branch filter (for multi-branch support)
        user_id: Optional user identifier for tracking

    Example client connection:
        ws = new WebSocket("ws://localhost:8000/ws/dashboard?branch_id=1&user_id=user123")
        ws.onmessage = (event) => console.log(JSON.parse(event.data))
    """
    client_id = str(uuid.uuid4())
    metadata = {
        "branch_id": branch_id,
        "user_id": user_id,
        "endpoint": "dashboard",
    }

    try:
        # Accept connection and store metadata
        await connection_manager.connect(client_id, websocket, metadata)

        # Send connection acknowledgment
        ack_message = ConnectionAckMessage(
            client_id=client_id,
            server_version="1.0.0",
            features=[
                "metrics",
                "anomalies",
                "forecasts",
                "alerts",
                "system_status",
            ],
        )
        await connection_manager.send_message(client_id, ack_message.model_dump())
        logger.info(f"Client {client_id} connected to dashboard (branch={branch_id})")

        # Keep connection alive and handle incoming messages
        while True:
            # Receive any message from client (for future client->server commands)
            data = await websocket.receive_json()
            logger.debug(f"Received from {client_id}: {data}")

            # Handle client commands if needed (e.g., subscription changes)
            message_type = data.get("type")
            if message_type == "subscribe":
                # Client can subscribe to specific event types
                event_types = data.get("event_types", [])
                logger.info(f"Client {client_id} subscribed to: {event_types}")
            elif message_type == "unsubscribe":
                event_types = data.get("event_types", [])
                logger.info(f"Client {client_id} unsubscribed from: {event_types}")

    except WebSocketDisconnect:
        connection_manager.disconnect(client_id)
        logger.info(f"Client {client_id} disconnected")
    except Exception as exc:
        logger.error(f"WebSocket error for {client_id}: {exc}")
        connection_manager.disconnect(client_id)


@router.websocket("/alerts")
async def websocket_alerts(
    websocket: WebSocket,
    severity: str | None = Query(None),
    user_id: str | None = Query(None),
):
    """WebSocket endpoint for real-time alerts only.

    Clients connect here to receive only alert notifications:
    - Anomaly alerts
    - Forecast alerts
    - Critical system alerts

    Query Parameters:
        severity: Optional filter (low, medium, high, critical)
        user_id: Optional user identifier

    Example:
        ws = new WebSocket("ws://localhost:8000/ws/alerts?severity=high")
    """
    client_id = str(uuid.uuid4())
    metadata = {
        "severity_filter": severity,
        "user_id": user_id,
        "endpoint": "alerts",
    }

    try:
        await connection_manager.connect(client_id, websocket, metadata)

        ack_message = ConnectionAckMessage(
            client_id=client_id,
            features=["anomalies", "forecasts", "critical_alerts"],
        )
        await connection_manager.send_message(client_id, ack_message.model_dump())
        logger.info(f"Client {client_id} connected to alerts (severity={severity})")

        while True:
            data = await websocket.receive_json()
            logger.debug(f"Alert client {client_id} sent: {data}")

    except WebSocketDisconnect:
        connection_manager.disconnect(client_id)
        logger.info(f"Alert client {client_id} disconnected")
    except Exception as exc:
        logger.error(f"Alert WebSocket error for {client_id}: {exc}")
        connection_manager.disconnect(client_id)


@router.get("/status", tags=["websocket"])
async def websocket_status():
    """Get current WebSocket connection status.

    Returns:
        - active_connections: Number of connected clients
        - client_ids: List of client identifiers
        - event_history: Recent events by type
    """
    dispatcher = get_dispatcher()
    return {
        "active_connections": connection_manager.get_active_count(),
        "client_ids": connection_manager.get_client_ids(),
        "event_types": list(dispatcher.event_history.keys()),
        "recent_events": {
            event_type: dispatcher.get_event_history(event_type, limit=5)
            for event_type in dispatcher.event_history.keys()
        },
    }


@router.post("/test-anomaly", tags=["websocket"])
async def test_anomaly(
    metric: str = "revenue",
    value: float = 50000,
    expected_value: float = 150000,
):
    """Test endpoint: Broadcast a test anomaly alert to all clients.

    Use for testing real-time anomaly notifications in development.

    Args:
        metric: Metric name
        value: Actual value
        expected_value: Expected value
    """
    dispatcher = get_dispatcher()
    await dispatcher.broadcast_anomaly(
        anomaly_id="test_anomaly_123",
        metric=metric,
        value=value,
        expected_value=expected_value,
        severity="high",
        description=f"Test anomaly: {metric} dropped from {expected_value} to {value}",
    )
    return {"status": "anomaly_broadcasted", "clients": connection_manager.get_active_count()}


@router.post("/test-forecast", tags=["websocket"])
async def test_forecast(
    metric: str = "revenue",
    predicted_value: float = 180000,
    trend: str = "up",
):
    """Test endpoint: Broadcast a test forecast alert to all clients.

    Use for testing real-time forecast notifications in development.

    Args:
        metric: What is being forecasted
        predicted_value: Predicted value
        trend: Direction (up, down, stable)
    """
    dispatcher = get_dispatcher()
    await dispatcher.broadcast_forecast(
        forecast_period="next_7_days",
        metric=metric,
        predicted_value=predicted_value,
        confidence=0.92,
        trend=trend,
        recommendation=f"Sales are forecasted to trend {trend}. Consider adjusting inventory.",
    )
    return {"status": "forecast_broadcasted", "clients": connection_manager.get_active_count()}


@router.post("/test-kpi", tags=["websocket"])
async def test_kpi():
    """Test endpoint: Broadcast test KPI update to all clients."""
    dispatcher = get_dispatcher()
    await dispatcher.broadcast_kpi_update(
        kpis={
            "total_revenue": 2450000,
            "total_orders": 1250,
            "average_order_value": 1960,
            "best_selling_product": "BBQ Platter",
        }
    )
    return {"status": "kpi_broadcasted", "clients": connection_manager.get_active_count()}
