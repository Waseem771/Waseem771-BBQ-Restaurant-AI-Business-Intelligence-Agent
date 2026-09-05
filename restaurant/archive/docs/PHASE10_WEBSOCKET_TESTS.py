"""Tests for Phase 10 WebSocket real-time layer.

Tests cover:
- Connection management
- Message schemas
- Event dispatching
- Real-time monitoring
- Integration with anomaly detection
"""
import asyncio
import json
from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.websocket.manager import ConnectionManager
from app.websocket.dispatcher import EventDispatcher, init_dispatcher
from app.websocket.schemas import (
    AlertSeverity,
    AnomalyAlert,
    ConnectionAckMessage,
    KPIUpdateMessage,
    MessageType,
)


# ============================================================================
# UNIT TESTS: Connection Manager
# ============================================================================


@pytest.mark.asyncio
async def test_connection_manager_connect_disconnect():
    """Test basic connection and disconnection."""
    from unittest.mock import AsyncMock

    manager = ConnectionManager()
    mock_ws = AsyncMock()

    # Connect
    await manager.connect("client_1", mock_ws, {"user_id": "user123"})
    assert manager.get_active_count() == 1
    assert "client_1" in manager.get_client_ids()

    # Disconnect
    manager.disconnect("client_1")
    assert manager.get_active_count() == 0
    assert "client_1" not in manager.get_client_ids()


@pytest.mark.asyncio
async def test_connection_manager_send_message():
    """Test sending message to specific client."""
    from unittest.mock import AsyncMock

    manager = ConnectionManager()
    mock_ws = AsyncMock()

    await manager.connect("client_1", mock_ws)

    # Send message
    message = {"type": "test", "value": 123}
    result = await manager.send_message("client_1", message)

    assert result is True
    mock_ws.send_json.assert_called_once_with(message)


@pytest.mark.asyncio
async def test_connection_manager_broadcast():
    """Test broadcasting to all clients."""
    from unittest.mock import AsyncMock

    manager = ConnectionManager()
    mock_ws1 = AsyncMock()
    mock_ws2 = AsyncMock()

    await manager.connect("client_1", mock_ws1)
    await manager.connect("client_2", mock_ws2)

    # Broadcast
    message = {"type": "broadcast", "data": "test"}
    await manager.broadcast(message)

    mock_ws1.send_json.assert_called_once_with(message)
    mock_ws2.send_json.assert_called_once_with(message)


@pytest.mark.asyncio
async def test_connection_manager_filtered_broadcast():
    """Test broadcasting to filtered clients."""
    from unittest.mock import AsyncMock

    manager = ConnectionManager()
    mock_ws1 = AsyncMock()
    mock_ws2 = AsyncMock()

    await manager.connect("client_1", mock_ws1, {"branch_id": 1})
    await manager.connect("client_2", mock_ws2, {"branch_id": 2})

    # Broadcast only to branch 1
    message = {"type": "branch_alert"}

    def filter_fn(client_id: str, metadata: dict) -> bool:
        return metadata.get("branch_id") == 1

    await manager.broadcast_filtered(message, filter_fn)

    mock_ws1.send_json.assert_called_once_with(message)
    mock_ws2.send_json.assert_not_called()


# ============================================================================
# UNIT TESTS: Message Schemas
# ============================================================================


def test_anomaly_alert_schema():
    """Test AnomalyAlert schema validation."""
    alert = AnomalyAlert(
        anomaly_id="anom_123",
        metric="revenue",
        value=50000,
        expected_value=150000,
        deviation_percent=66.67,
        severity=AlertSeverity.HIGH,
        description="Revenue dropped significantly",
    )

    assert alert.type == MessageType.ANOMALY_DETECTED
    assert alert.metric == "revenue"
    assert alert.severity == AlertSeverity.HIGH
    assert isinstance(alert.timestamp, datetime)

    # Can serialize to dict
    data = alert.model_dump()
    assert data["metric"] == "revenue"
    assert data["severity"] == "high"


def test_kpi_update_schema():
    """Test KPIUpdateMessage schema."""
    message = KPIUpdateMessage(
        kpis={
            "total_revenue": 2450000,
            "total_orders": 1250,
            "average_order_value": 1960,
        }
    )

    assert message.type == MessageType.KPI_UPDATE
    assert message.kpis["total_revenue"] == 2450000
    assert message.interval == "hourly"


def test_connection_ack_schema():
    """Test ConnectionAckMessage schema."""
    message = ConnectionAckMessage(client_id="client_123")

    assert message.type == MessageType.CONNECTION_ACK
    assert message.client_id == "client_123"
    assert "metrics" in message.features
    assert "anomalies" in message.features


# ============================================================================
# UNIT TESTS: Event Dispatcher
# ============================================================================


@pytest.mark.asyncio
async def test_event_dispatcher_broadcast_anomaly():
    """Test broadcasting anomaly via dispatcher."""
    from unittest.mock import AsyncMock

    manager = ConnectionManager()
    mock_ws = AsyncMock()
    await manager.connect("client_1", mock_ws)

    dispatcher = EventDispatcher(manager)

    # Broadcast anomaly
    await dispatcher.broadcast_anomaly(
        anomaly_id="anom_123",
        metric="revenue",
        value=50000,
        expected_value=150000,
        severity=AlertSeverity.HIGH,
        description="Revenue dropped",
    )

    # Verify message was sent
    mock_ws.send_json.assert_called_once()
    call_args = mock_ws.send_json.call_args
    message_data = call_args[0][0]
    assert message_data["type"] == "anomaly_detected"
    assert message_data["metric"] == "revenue"


@pytest.mark.asyncio
async def test_event_dispatcher_broadcast_kpi():
    """Test broadcasting KPI update via dispatcher."""
    from unittest.mock import AsyncMock

    manager = ConnectionManager()
    mock_ws = AsyncMock()
    await manager.connect("client_1", mock_ws)

    dispatcher = EventDispatcher(manager)

    # Broadcast KPI
    await dispatcher.broadcast_kpi_update(
        kpis={
            "total_revenue": 2450000,
            "total_orders": 1250,
        }
    )

    mock_ws.send_json.assert_called_once()
    call_args = mock_ws.send_json.call_args
    message_data = call_args[0][0]
    assert message_data["type"] == "kpi_update"
    assert message_data["kpis"]["total_revenue"] == 2450000


@pytest.mark.asyncio
async def test_event_dispatcher_publish_and_subscribe():
    """Test event publishing and subscription."""
    manager = ConnectionManager()
    dispatcher = EventDispatcher(manager)

    # Track handler calls
    events_received = []

    async def test_handler(event_data):
        events_received.append(event_data)

    # Subscribe to custom event
    dispatcher.subscribe("custom_event", test_handler)

    # Publish event
    await dispatcher.publish("custom_event", {"data": "test"})

    assert len(events_received) == 1
    assert events_received[0]["data"] == "test"


@pytest.mark.asyncio
async def test_event_dispatcher_event_history():
    """Test event history tracking."""
    manager = ConnectionManager()
    dispatcher = EventDispatcher(manager)

    # Publish multiple events
    for i in range(5):
        await dispatcher.publish("test_event", {"id": i})

    # Get history
    history = dispatcher.get_event_history("test_event")
    assert len(history) == 5
    assert history[0]["data"]["id"] == 0
    assert history[4]["data"]["id"] == 4


# ============================================================================
# INTEGRATION TESTS: REST API Endpoints
# ============================================================================


def test_websocket_status_endpoint():
    """Test /ws/status endpoint."""
    client = TestClient(app)
    response = client.get("/ws/status")

    assert response.status_code == 200
    data = response.json()
    assert "active_connections" in data
    assert "event_types" in data
    assert data["active_connections"] >= 0


def test_test_anomaly_endpoint():
    """Test /ws/test-anomaly endpoint."""
    client = TestClient(app)
    response = client.post(
        "/ws/test-anomaly",
        params={
            "metric": "revenue",
            "value": 50000,
            "expected_value": 150000,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "anomaly_broadcasted"
    assert "clients" in data


def test_test_forecast_endpoint():
    """Test /ws/test-forecast endpoint."""
    client = TestClient(app)
    response = client.post(
        "/ws/test-forecast",
        params={
            "metric": "revenue",
            "predicted_value": 180000,
            "trend": "up",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "forecast_broadcasted"


def test_test_kpi_endpoint():
    """Test /ws/test-kpi endpoint."""
    client = TestClient(app)
    response = client.post("/ws/test-kpi")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "kpi_broadcasted"


# ============================================================================
# INTEGRATION TESTS: WebSocket Connections
# ============================================================================


def test_websocket_dashboard_connection():
    """Test WebSocket dashboard endpoint connection."""
    client = TestClient(app)

    with client.websocket_connect("/ws/dashboard?branch_id=1&user_id=user123") as websocket:
        # Receive connection acknowledgment
        data = websocket.receive_json()
        assert data["type"] == "connection_ack"
        assert "client_id" in data
        assert "metrics" in data["features"]


def test_websocket_alerts_connection():
    """Test WebSocket alerts endpoint connection."""
    client = TestClient(app)

    with client.websocket_connect("/ws/alerts?severity=high") as websocket:
        # Receive connection acknowledgment
        data = websocket.receive_json()
        assert data["type"] == "connection_ack"
        assert "anomalies" in data["features"]


def test_websocket_multiple_connections():
    """Test multiple concurrent WebSocket connections."""
    client = TestClient(app)

    with client.websocket_connect("/ws/dashboard?user_id=user1") as ws1:
        with client.websocket_connect("/ws/dashboard?user_id=user2") as ws2:
            # Both should receive connection ack
            data1 = ws1.receive_json(timeout=1.0)
            data2 = ws2.receive_json(timeout=1.0)

            assert data1["type"] == "connection_ack"
            assert data2["type"] == "connection_ack"
            assert data1["client_id"] != data2["client_id"]


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_broadcast_performance():
    """Test broadcast performance with many connections."""
    import time

    manager = ConnectionManager()
    from unittest.mock import AsyncMock

    # Create 100 mock connections
    for i in range(100):
        mock_ws = AsyncMock()
        await manager.connect(f"client_{i}", mock_ws)

    # Broadcast message
    message = {"type": "test", "data": "performance"}
    start = time.time()
    await manager.broadcast(message)
    elapsed = time.time() - start

    # Should complete reasonably fast (< 1 second for 100 clients)
    assert elapsed < 1.0


# ============================================================================
# SUMMARY
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("PHASE 10 - WEBSOCKET REAL-TIME LAYER TESTS")
    print("=" * 80)
    print("\nRun tests with:")
    print("  pytest PHASE10_WEBSOCKET_TESTS.py -v")
    print("  pytest PHASE10_WEBSOCKET_TESTS.py -v --asyncio-mode=auto")
    print("\nTest coverage:")
    print("  - Connection management")
    print("  - Message schemas")
    print("  - Event dispatching")
    print("  - REST endpoints")
    print("  - WebSocket connections")
    print("  - Performance")
