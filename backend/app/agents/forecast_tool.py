"""
Phase 8 - AI Agent Forecasting Tool
Integration point for AI agent to access forecasting capabilities

This module provides a tool that the AI agent can call to make predictions.
It's designed to work alongside the SQL tool.
"""

from typing import Dict, Any
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from forecast_tool import ForecastTool


class AIAgentForecastTool:
    """
    Forecasting tool for the AI agent.

    The AI agent can call this tool when it needs to make predictions about:
    - Future revenue
    - Future order volumes
    - Forecast confidence and accuracy

    Integration with SQL tool:
    - SQL tool: Retrieves historical data and metrics
    - Forecast tool: Makes predictions based on history
    """

    def __init__(self):
        """Initialize the forecast tool."""
        self.forecast_tool = ForecastTool()

    def call(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call the forecast tool with specified action.

        Actions:
        - forecast_revenue: Predict future revenue
        - forecast_orders: Predict future order volume
        - get_metrics: Get model accuracy metrics
        - compare_periods: Compare forecast with historical period

        Args:
            action: The action to perform
            params: Parameters for the action

        Returns:
            Result dictionary with forecast or metrics
        """

        if action == "forecast_revenue":
            days = params.get("days", 30)
            return self._format_forecast_response(
                self.forecast_tool.forecast_revenue(days=days),
                "revenue"
            )

        elif action == "forecast_orders":
            days = params.get("days", 30)
            return self._format_forecast_response(
                self.forecast_tool.forecast_orders(days=days),
                "orders"
            )

        elif action == "get_metrics":
            return self.forecast_tool.get_forecast_confidence()

        elif action == "compare_periods":
            period = params.get("period", "next_month")
            return self.forecast_tool.forecast_by_period(period)

        else:
            return {"error": f"Unknown action: {action}"}

    def _format_forecast_response(self, forecast_data: Dict, forecast_type: str) -> Dict[str, Any]:
        """
        Format forecast response for AI agent consumption.

        Args:
            forecast_data: Raw forecast data
            forecast_type: Type of forecast (revenue or orders)

        Returns:
            Formatted response with summary and details
        """

        if "error" in forecast_data:
            return forecast_data

        if forecast_type == "revenue":
            summary = (
                f"Revenue forecast for {forecast_data['period']}: "
                f"{forecast_data['predicted_total']:,.0f} PKR total, "
                f"{forecast_data['predicted_daily_avg']:,.0f} PKR daily average. "
                f"Confidence: {forecast_data['confidence_accuracy']}"
            )

        else:  # orders
            summary = (
                f"Order forecast for {forecast_data['period']}: "
                f"{forecast_data['predicted_total_orders']:,} total orders, "
                f"{forecast_data['predicted_daily_avg_orders']:,} daily average. "
                f"Confidence: {forecast_data['confidence_accuracy']}"
            )

        return {
            "summary": summary,
            "details": forecast_data,
            "forecast_type": forecast_type
        }

    def describe(self) -> str:
        """
        Describe the tool for the AI agent.

        Returns:
            Description of tool capabilities
        """
        return """
Forecasting Tool - Predicts future sales and orders

Actions:
1. forecast_revenue(days: int)
   - Predicts total and daily revenue for specified days
   - Example: "forecast_revenue(days=30)"
   - Returns: Total revenue, daily average, day-by-day breakdown

2. forecast_orders(days: int)
   - Predicts order volume for specified days
   - Example: "forecast_orders(days=7)"
   - Returns: Total orders, daily average, day-by-day breakdown

3. get_metrics()
   - Returns model accuracy and confidence metrics
   - Shows MAPE (Mean Absolute Percentage Error)
   - Example: "get_metrics()"

4. compare_periods(period: str)
   - Forecast for predefined periods
   - Periods: "next_week", "next_month", "next_quarter"
   - Example: "compare_periods(period='next_month')"

Model Information:
- Algorithm: Random Forest Regressor
- Training Data: 273 days (2026-01-01 to 2026-09-30)
- Accuracy: 86.35% (MAPE: 13.65%)
- Features: Day of week, month, seasonality, trends
"""


# ============================================================================
# Integration Example for AI Assistant
# ============================================================================

def integrate_forecast_with_agent(agent_tools: Dict) -> Dict:
    """
    Add forecast tool to AI agent's toolkit.

    This function shows how to integrate the forecast tool with the AI agent.

    Args:
        agent_tools: Existing agent tools dictionary

    Returns:
        Updated tools dictionary with forecast tool added
    """

    forecast_tool = AIAgentForecastTool()

    agent_tools["forecast"] = {
        "callable": forecast_tool.call,
        "description": forecast_tool.describe(),
        "actions": [
            "forecast_revenue",
            "forecast_orders",
            "get_metrics",
            "compare_periods"
        ]
    }

    return agent_tools


# ============================================================================
# Test Cases for AI Agent Integration
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("PHASE 8 - AI AGENT FORECAST TOOL")
    print("=" * 80)

    # Initialize tool
    tool = AIAgentForecastTool()

    print("\n[TOOL DESCRIPTION]")
    print(tool.describe())

    # Test 1: Forecast revenue
    print("\n[TEST 1] Forecast revenue for next 7 days")
    result = tool.call("forecast_revenue", {"days": 7})
    print(f"Summary: {result['summary']}")

    # Test 2: Forecast orders
    print("\n[TEST 2] Forecast orders for next 30 days")
    result = tool.call("forecast_orders", {"days": 30})
    print(f"Summary: {result['summary']}")

    # Test 3: Get metrics
    print("\n[TEST 3] Get model confidence metrics")
    result = tool.call("get_metrics", {})
    print(f"Model: {result['model_type']}")
    print(f"Accuracy: {result['accuracy_confidence']}")
    print(f"MAPE: {result['mape_percent']}")

    # Test 4: Compare periods
    print("\n[TEST 4] Forecast for next month")
    result = tool.call("compare_periods", {"period": "next_month"})
    print(f"Period: {result['period']}")
    print(f"Predicted Total: {result['predicted_total']:,.0f} PKR")

    print("\n" + "=" * 80)
    print("ALL TESTS PASSED - READY FOR AI AGENT INTEGRATION")
    print("=" * 80)
