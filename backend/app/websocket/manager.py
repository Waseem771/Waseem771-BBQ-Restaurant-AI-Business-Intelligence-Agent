"""Connection manager for WebSocket clients.

Tracks active connections, routes messages, and handles disconnections.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Callable

from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)


class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles datetime objects."""

    def default(self, obj):
        """Convert datetime to ISO format string."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class ConnectionManager:
    """Manages WebSocket connections and message routing.

    Responsibilities:
    - Track active connections by client ID
    - Broadcast messages to specific clients or all clients
    - Handle connection/disconnection lifecycle
    - Error recovery on network failures
    """

    def __init__(self):
        """Initialize connection manager with empty connection pool."""
        self.active_connections: dict[str, WebSocket] = {}
        self.connection_metadata: dict[str, dict] = {}

    async def connect(self, client_id: str, websocket: WebSocket, metadata: dict | None = None):
        """Accept WebSocket connection and store metadata.

        Args:
            client_id: Unique identifier for the client
            websocket: FastAPI WebSocket connection
            metadata: Optional client metadata (user_id, branch_id, etc.)
        """
        await websocket.accept()
        self.active_connections[client_id] = websocket
        self.connection_metadata[client_id] = metadata or {}
        logger.info(f"Client connected: {client_id} (total: {len(self.active_connections)})")

    def disconnect(self, client_id: str):
        """Remove disconnected client from pool.

        Args:
            client_id: Client identifier
        """
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            del self.connection_metadata[client_id]
            logger.info(f"Client disconnected: {client_id} (total: {len(self.active_connections)})")

    async def send_message(self, client_id: str, message: dict):
        """Send message to specific client.

        Args:
            client_id: Target client identifier
            message: Message dict to send (will be JSON encoded)

        Returns:
            True if sent successfully, False if client disconnected
        """
        if client_id not in self.active_connections:
            return False

        try:
            ws = self.active_connections[client_id]
            # Use custom encoder to handle datetime objects
            json_str = json.dumps(message, cls=DateTimeEncoder)
            await ws.send_text(json_str)
            return True
        except Exception as exc:
            logger.warning(f"Failed to send message to {client_id}: {exc}")
            self.disconnect(client_id)
            return False

    async def broadcast(self, message: dict, exclude_client: str | None = None):
        """Send message to all connected clients.

        Args:
            message: Message dict to broadcast
            exclude_client: Optional client ID to exclude
        """
        disconnected = []
        # Use custom encoder to handle datetime objects
        json_str = json.dumps(message, cls=DateTimeEncoder)

        for client_id, ws in list(self.active_connections.items()):
            if exclude_client and client_id == exclude_client:
                continue

            try:
                await ws.send_text(json_str)
            except Exception as exc:
                logger.warning(f"Failed to broadcast to {client_id}: {exc}")
                disconnected.append(client_id)

        # Clean up disconnected clients
        for client_id in disconnected:
            self.disconnect(client_id)

    async def broadcast_filtered(
        self,
        message: dict,
        filter_fn: Callable[[str, dict], bool],
    ):
        """Broadcast to clients matching a filter function.

        Useful for sending branch-specific or role-specific messages.

        Args:
            message: Message dict to send
            filter_fn: Function(client_id, metadata) -> bool
        """
        disconnected = []
        # Use custom encoder to handle datetime objects
        json_str = json.dumps(message, cls=DateTimeEncoder)

        for client_id, metadata in list(self.connection_metadata.items()):
            if not filter_fn(client_id, metadata):
                continue

            try:
                ws = self.active_connections[client_id]
                await ws.send_text(json_str)
            except Exception as exc:
                logger.warning(f"Failed to send filtered message to {client_id}: {exc}")
                disconnected.append(client_id)

        for client_id in disconnected:
            self.disconnect(client_id)

    def get_active_count(self) -> int:
        """Return number of active connections."""
        return len(self.active_connections)

    def get_client_ids(self) -> list[str]:
        """Return list of all connected client IDs."""
        return list(self.active_connections.keys())

    def get_metadata(self, client_id: str) -> dict | None:
        """Get metadata for a specific client."""
        return self.connection_metadata.get(client_id)


# Global connection manager instance
manager = ConnectionManager()
