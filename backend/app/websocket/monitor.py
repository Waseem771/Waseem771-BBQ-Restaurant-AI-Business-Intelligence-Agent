"""Background service for real-time monitoring and alert generation.

Runs periodic checks on anomalies, forecasts, and metrics,
broadcasting alerts to connected WebSocket clients.
"""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta

from .. import analytics
from .dispatcher import get_dispatcher
from .schemas import AlertSeverity

logger = logging.getLogger(__name__)


class RealtimeMonitor:
    """Monitors business metrics and broadcasts real-time alerts.

    Responsibilities:
    - Periodic anomaly detection
    - Sales trend monitoring
    - Forecast-based alerts
    - Metric aggregation
    - Alert batching to avoid spam
    """

    def __init__(self, check_interval_seconds: int = 60):
        """Initialize monitor.

        Args:
            check_interval_seconds: How often to run checks
        """
        self.check_interval = check_interval_seconds
        self.is_running = False
        self.last_anomalies: dict = {}  # Track recent anomalies to avoid duplicates
        self.alert_cooldown = timedelta(minutes=5)  # Don't alert twice in 5 minutes

    async def start(self):
        """Start the monitoring loop."""
        self.is_running = True
        logger.info(f"Real-time monitor started (check interval: {self.check_interval}s)")

        try:
            while self.is_running:
                await asyncio.sleep(self.check_interval)
                await self.check_and_broadcast()
        except Exception as exc:
            logger.error(f"Monitor error: {exc}")
            self.is_running = False

    async def stop(self):
        """Stop the monitoring loop."""
        self.is_running = False
        logger.info("Real-time monitor stopped")

    async def check_and_broadcast(self):
        """Run all checks and broadcast any alerts."""
        try:
            await self._check_anomalies()
            await self._check_metrics()
            # await self._check_forecasts()  # Can be enabled later
        except Exception as exc:
            logger.error(f"Check and broadcast error: {exc}")

    async def _check_anomalies(self):
        """Check for anomalies and broadcast alerts."""
        try:
            dispatcher = get_dispatcher()

            # Run anomaly detection
            anomalies = analytics.detect_anomalies(threshold=0.6)

            if not anomalies:
                return

            # Broadcast each anomaly
            for anomaly in anomalies:
                # Create a unique key for deduplication
                anomaly_key = f"revenue_{anomaly['date']}"

                # Skip if we just alerted on this
                if anomaly_key in self.last_anomalies:
                    last_alert = self.last_anomalies[anomaly_key]
                    if datetime.utcnow() - last_alert < self.alert_cooldown:
                        continue

                # Determine severity based on deviation percentage
                deviation = abs(anomaly["deviation_pct"])
                if deviation > 50:
                    severity = AlertSeverity.CRITICAL
                elif deviation > 30:
                    severity = AlertSeverity.HIGH
                elif deviation > 15:
                    severity = AlertSeverity.MEDIUM
                else:
                    severity = AlertSeverity.LOW

                # Broadcast
                await dispatcher.broadcast_anomaly(
                    anomaly_id=f"anom_revenue_{anomaly['date']}",
                    metric="revenue",
                    value=round(anomaly["revenue"], 2),
                    expected_value=round(anomaly["expected"], 2),
                    severity=severity,
                    description=f"Revenue {anomaly['direction']} on {anomaly['date']}: "
                    f"expected PKR {anomaly['expected']:,.0f}, got PKR {anomaly['revenue']:,.0f} "
                    f"({anomaly['deviation_pct']:+.1f}%)",
                )

                self.last_anomalies[anomaly_key] = datetime.utcnow()

            logger.debug(f"Checked {len(anomalies)} anomalies")

        except Exception as exc:
            logger.error(f"Anomaly check error: {exc}")

    async def _check_metrics(self):
        """Check and broadcast updated KPIs."""
        try:
            dispatcher = get_dispatcher()

            # Get current KPIs
            kpis = analytics.kpis()

            # Broadcast KPI update
            await dispatcher.broadcast_kpi_update(kpis=kpis, interval="real_time")

            logger.debug("KPI metrics updated")

        except Exception as exc:
            logger.error(f"Metrics check error: {exc}")

    async def _check_forecasts(self):
        """Check forecasts and broadcast relevant alerts."""
        try:
            dispatcher = get_dispatcher()

            # This would integrate with forecasting.py
            # For now, placeholder

            logger.debug("Forecast checks completed")

        except Exception as exc:
            logger.error(f"Forecast check error: {exc}")


# Global monitor instance
_monitor: RealtimeMonitor | None = None


def get_monitor() -> RealtimeMonitor:
    """Get or create the global monitor instance."""
    global _monitor
    if _monitor is None:
        _monitor = RealtimeMonitor(check_interval_seconds=60)
    return _monitor


async def start_realtime_monitor():
    """Start the background real-time monitor.

    Call this during app startup (lifespan event).
    """
    monitor = get_monitor()
    # Run in background task
    asyncio.create_task(monitor.start())
    logger.info("Real-time monitor background task started")


async def stop_realtime_monitor():
    """Stop the background real-time monitor.

    Call this during app shutdown (lifespan event).
    """
    monitor = get_monitor()
    await monitor.stop()
    logger.info("Real-time monitor background task stopped")
