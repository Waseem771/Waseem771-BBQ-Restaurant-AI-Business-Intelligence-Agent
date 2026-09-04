"""
Phase 9 - Anomaly Detection Tool for AI Agent
Integration point for AI agent to access anomaly detection

This module provides a tool that the AI agent can call to detect
unusual sales patterns and generate alerts.
"""

import logging
from typing import Dict, Any, List

from ..anomaly_detection import AnomalyDetector, load_sales_data, engineer_anomaly_features

logger = logging.getLogger(__name__)


class AIAgentAnomalyTool:
    """
    Anomaly detection tool for the AI agent.

    The AI agent can call this tool to:
    - Detect current anomalies
    - Get anomaly statistics
    - Explain specific anomalies
    - Get alerts and recommendations
    """

    def __init__(self):
        """Initialize the anomaly detection tool."""
        self.detector = AnomalyDetector(contamination_rate=0.05)
        self.data = None
        self.results = None
        self._initialize()

    def _initialize(self):
        """Initialize anomaly detector with data."""
        try:
            self.data = load_sales_data()
            self.data = engineer_anomaly_features(self.data)
            self.detector.train(self.data)
            self.results, _ = self.detector.detect_anomalies(self.data)
        except Exception as e:
            logger.error(f"Error initializing anomaly detector: {e}")

    def call(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call the anomaly detection tool with specified action.

        Actions:
        - detect_current: Detect anomalies in recent data
        - get_statistics: Get anomaly statistics
        - explain_anomaly: Get explanation for specific anomaly
        - get_alerts: Get critical alerts

        Args:
            action: The action to perform
            params: Parameters for the action

        Returns:
            Result dictionary
        """

        if action == "detect_current":
            days = params.get("days", 7)
            return self._detect_current(days)

        elif action == "get_statistics":
            return self._get_statistics()

        elif action == "explain_anomaly":
            date_str = params.get("date")
            return self._explain_anomaly(date_str)

        elif action == "get_alerts":
            severity = params.get("severity", "HIGH")
            return self._get_alerts(severity)

        else:
            return {"error": f"Unknown action: {action}"}

    def _detect_current(self, days: int) -> Dict[str, Any]:
        """
        Detect anomalies in recent data.

        Args:
            days: Number of recent days to analyze

        Returns:
            Current anomaly detection results
        """
        if self.results is None:
            return {"error": "Anomaly detector not initialized"}

        # Get last N days
        recent = self.results.tail(days).copy()
        anomalies = recent[recent['is_anomaly']]

        summary = f"In the last {days} days, detected {len(anomalies)} anomalies."

        anomaly_list = []
        for idx, row in anomalies.iterrows():
            anomaly_list.append({
                "date": row['date'].strftime("%Y-%m-%d"),
                "severity": row['severity'],
                "revenue": float(row['daily_revenue']),
                "orders": int(row['order_count']),
                "anomaly_score": float(row['anomaly_score'])
            })

        return {
            "summary": summary,
            "anomalies": anomaly_list,
            "count": len(anomalies),
            "period_days": days
        }

    def _get_statistics(self) -> Dict[str, Any]:
        """
        Get anomaly detection statistics.

        Returns:
            Statistics about anomalies
        """
        if self.results is None:
            return {"error": "Anomaly detector not initialized"}

        anomalies = self.results[self.results['is_anomaly']]
        normal = self.results[~self.results['is_anomaly']]

        return {
            "total_days": len(self.results),
            "anomaly_count": len(anomalies),
            "anomaly_percentage": float(len(anomalies) / len(self.results) * 100),
            "normal_avg_revenue": float(normal['daily_revenue'].mean()),
            "anomaly_avg_revenue": float(anomalies['daily_revenue'].mean()),
            "normal_avg_orders": float(normal['order_count'].mean()),
            "anomaly_avg_orders": float(anomalies['order_count'].mean()),
            "model_type": "Isolation Forest",
            "features_used": 7
        }

    def _explain_anomaly(self, date_str: str) -> Dict[str, Any]:
        """
        Get explanation for specific anomaly.

        Args:
            date_str: Date in YYYY-MM-DD format

        Returns:
            Detailed explanation
        """
        if self.results is None:
            return {"error": "Anomaly detector not initialized"}

        try:
            # Find row with matching date
            matching = self.results[self.results['date'].dt.strftime('%Y-%m-%d') == date_str]

            if len(matching) == 0:
                return {"error": f"No data found for date: {date_str}"}

            row = matching.iloc[0]

            if not row['is_anomaly']:
                return {
                    "date": date_str,
                    "status": "NORMAL",
                    "message": "This day was not flagged as anomalous"
                }

            explanation = self.detector.explain_anomaly(row)

            return {
                "date": date_str,
                "severity": row['severity'],
                "revenue": float(row['daily_revenue']),
                "orders": int(row['order_count']),
                "anomaly_score": float(row['anomaly_score']),
                "explanation": explanation,
                "avg_order_value": float(row['avg_order_value']),
                "orders_per_customer": float(row['orders_per_customer'])
            }

        except Exception as e:
            return {"error": f"Error explaining anomaly: {e}"}

    def _get_alerts(self, severity: str = "HIGH") -> Dict[str, Any]:
        """
        Get critical alerts.

        Args:
            severity: Severity level (CRITICAL, HIGH, MEDIUM, LOW)

        Returns:
            List of alerts
        """
        if self.results is None:
            return {"error": "Anomaly detector not initialized"}

        alerts = self.results[
            (self.results['is_anomaly']) &
            (self.results['severity'] == severity)
        ].sort_values('anomaly_score')

        alert_list = []
        for idx, row in alerts.iterrows():
            alert_list.append({
                "date": row['date'].strftime("%Y-%m-%d"),
                "revenue": float(row['daily_revenue']),
                "orders": int(row['order_count']),
                "severity": row['severity'],
                "explanation": self.detector.explain_anomaly(row)
            })

        return {
            "severity": severity,
            "alert_count": len(alert_list),
            "alerts": alert_list
        }

    def describe(self) -> str:
        """
        Describe the tool for the AI agent.

        Returns:
            Description of tool capabilities
        """
        return """
Anomaly Detection Tool - Detects unusual sales patterns

Actions:
1. detect_current(days: int)
   - Detects anomalies in recent days
   - Example: "detect_current(days=7)"
   - Returns: List of anomalies with details

2. get_statistics()
   - Returns overall anomaly statistics
   - Shows comparison between normal and anomaly days
   - Example: "get_statistics()"

3. explain_anomaly(date: str)
   - Detailed explanation for specific date
   - Example: "explain_anomaly(date='2026-03-23')"
   - Returns: Reason for anomaly flag

4. get_alerts(severity: str)
   - Get alerts of specific severity
   - Severity: CRITICAL, HIGH, MEDIUM, LOW
   - Example: "get_alerts(severity='HIGH')"

Model Information:
- Algorithm: Isolation Forest
- Detection Rate: 5.1%
- Features: 7 engineered features
"""
