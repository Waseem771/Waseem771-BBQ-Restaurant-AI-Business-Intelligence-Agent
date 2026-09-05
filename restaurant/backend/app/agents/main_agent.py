"""
Phase 9.5 - Main AI Agent with Tool Integration
Complete AI agent that combines multiple tools (forecasting, anomaly detection, etc.)

This is the central orchestrator that:
1. Receives user questions
2. Selects appropriate tools
3. Calls the tools
4. Combines results
5. Generates final response

Beginner-friendly with detailed English comments.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the tools we created
from agents.forecast_tool import AIAgentForecastTool
from agents.anomaly_tool import AIAgentAnomalyTool


class MainAIAgent:
    """
    Main AI Agent - orchestrates all available tools

    This agent can handle:
    1. Forecasting questions (sales predictions, trends)
    2. Anomaly questions (unusual patterns, alerts)
    3. Analytics questions (KPIs, metrics)

    The agent matches the user question to the right tool
    and combines results intelligently.
    """

    def __init__(self):
        """Initialize the main agent with all available tools."""
        print("[AGENT] Initializing Main AI Agent...")

        # Initialize individual tools
        self.forecast_tool = AIAgentForecastTool()
        self.anomaly_tool = AIAgentAnomalyTool()

        print("[AGENT] All tools initialized successfully")

    def process_question(self, question: str) -> Dict[str, Any]:
        """
        Process a user question and return an intelligent response.

        Steps:
        1. Analyze the question
        2. Determine which tool(s) to use
        3. Call the appropriate tool(s)
        4. Combine results
        5. Generate response

        Args:
            question: User's natural language question

        Returns:
            Response dictionary with answer and metadata
        """

        print(f"\n[AGENT] Processing question: {question}")

        # Step 1: Normalize question
        q_lower = question.lower()

        # Step 2: Detect question type and call appropriate tools
        response = {
            "question": question,
            "timestamp": datetime.now().isoformat(),
            "tools_used": [],
            "results": [],
            "answer": "",
            "confidence": 0.0
        }

        # Check for forecasting questions
        forecast_keywords = ["forecast", "predict", "next", "future", "expected", "will", "revenue"]
        if any(kw in q_lower for kw in forecast_keywords):
            response = self._handle_forecast_question(question, response)

        # Check for anomaly questions
        anomaly_keywords = ["anomal", "unusual", "strange", "outlier", "spike", "alert", "detect"]
        if any(kw in q_lower for kw in anomaly_keywords):
            response = self._handle_anomaly_question(question, response)

        # If no tools matched, provide guidance
        if not response["tools_used"]:
            response["answer"] = self._get_guidance()
            response["confidence"] = 0.3
        else:
            # Calculate combined confidence
            response["confidence"] = min(1.0, len(response["tools_used"]) * 0.5)

        return response

    def _handle_forecast_question(self, question: str, response: Dict) -> Dict:
        """
        Handle forecasting questions.

        Args:
            question: User question
            response: Response dictionary to update

        Returns:
            Updated response with forecast results
        """
        print("[AGENT] -> Calling Forecast Tool")

        # Determine forecast type
        q_lower = question.lower()

        try:
            if "7 day" in q_lower or "week" in q_lower or "next week" in q_lower:
                result = self.forecast_tool.call("forecast_revenue", {"days": 7})
                result_type = "7-day revenue forecast"
            elif "30 day" in q_lower or "month" in q_lower or "next month" in q_lower:
                result = self.forecast_tool.call("forecast_revenue", {"days": 30})
                result_type = "30-day revenue forecast"
            elif "order" in q_lower:
                result = self.forecast_tool.call("forecast_orders", {"days": 30})
                result_type = "order forecast"
            else:
                result = self.forecast_tool.call("forecast_revenue", {"days": 7})
                result_type = "7-day revenue forecast (default)"

            response["tools_used"].append("Forecast Tool")
            response["results"].append({
                "tool": "Forecast Tool",
                "type": result_type,
                "data": result
            })

            # Generate answer from forecast
            # Handle both response formats
            if "summary" in result:
                response["answer"] = result.get("summary", "Forecast generated")
            elif "details" in result and result["details"]:
                details = result["details"]
                if "predicted_total" in details:
                    response["answer"] = (
                        f"Based on historical patterns, the {result_type} is estimated at "
                        f"Rs. {details.get('predicted_total', 0):,.0f} with "
                        f"{details.get('confidence_accuracy', 0)} confidence. "
                        f"Daily average: Rs. {details.get('predicted_daily_avg', 0):,.0f}."
                    )
                else:
                    response["answer"] = result.get("summary", "Forecast generated")
            else:
                response["answer"] = "Forecast generated successfully"

        except Exception as e:
            print(f"[ERROR] Forecast tool error: {e}")
            response["answer"] = f"Forecast analysis: {str(e)}"

        return response

    def _handle_anomaly_question(self, question: str, response: Dict) -> Dict:
        """
        Handle anomaly detection questions.

        Args:
            question: User question
            response: Response dictionary to update

        Returns:
            Updated response with anomaly results
        """
        print("[AGENT] -> Calling Anomaly Tool")

        q_lower = question.lower()

        try:
            if "current" in q_lower or "recent" in q_lower or "today" in q_lower:
                result = self.anomaly_tool.call("detect_current", {"days": 7})
                result_type = "recent anomalies"
            elif "all" in q_lower or "list" in q_lower:
                result = self.anomaly_tool.call("get_alerts", {"severity": "HIGH"})
                result_type = "high severity alerts"
            else:
                result = self.anomaly_tool.call("get_statistics", {})
                result_type = "anomaly statistics"

            response["tools_used"].append("Anomaly Tool")
            response["results"].append({
                "tool": "Anomaly Tool",
                "type": result_type,
                "data": result
            })

            # Generate answer from anomaly results
            if "count" in result:
                response["answer"] = (
                    f"Anomaly detection analysis: Found {result.get('count', 0)} anomalies. "
                    f"{result.get('summary', 'No summary available.')}"
                )
            elif "alert_count" in result:
                response["answer"] = (
                    f"Alert status: {result.get('alert_count', 0)} {result.get('severity', 'UNKNOWN')} severity alerts detected."
                )
            elif "total_days" in result:
                response["answer"] = (
                    f"Anomaly Analysis: {result.get('anomaly_count', 0)} anomalies detected in "
                    f"{result.get('total_days', 0)} days ({result.get('anomaly_percentage', 0):.1f}%). "
                    f"Normal days average Rs. {result.get('normal_avg_revenue', 0):,.0f} vs "
                    f"anomaly days average Rs. {result.get('anomaly_avg_revenue', 0):,.0f}."
                )

        except Exception as e:
            print(f"[ERROR] Anomaly tool error: {e}")
            response["answer"] += f"\nAnomaly detection unavailable: {str(e)}"

        return response

    def _get_guidance(self) -> str:
        """Return guidance for unsupported questions."""
        return (
            "I can help you with:\n"
            "1. FORECASTING: 'What are next week sales?' 'Forecast 30-day revenue'\n"
            "2. ANOMALIES: 'Show recent anomalies' 'Are there unusual patterns?'\n"
            "3. ANALYTICS: 'Show KPIs' 'Top products' 'Revenue breakdown'\n\n"
            "Try rephrasing your question with these keywords."
        )

    def describe_tools(self) -> str:
        """Describe available tools."""
        return f"""
Available Tools:

1. FORECAST TOOL
{self.forecast_tool.describe()}

2. ANOMALY TOOL
{self.anomaly_tool.describe()}
"""


# ============================================================================
# Test Cases
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("PHASE 9.5 - MAIN AI AGENT WITH TOOL INTEGRATION")
    print("=" * 80)

    # Initialize agent
    agent = MainAIAgent()

    # Display available tools
    print(agent.describe_tools())

    # Test Case 1: Forecast question
    print("\n[TEST 1] Forecast Question")
    print("-" * 80)
    question1 = "What will be our revenue in the next 7 days?"
    result1 = agent.process_question(question1)
    print(f"Question: {question1}")
    print(f"Tools Used: {', '.join(result1['tools_used'])}")
    print(f"Answer: {result1['answer']}")
    print(f"Confidence: {result1['confidence']:.0%}")

    # Test Case 2: Anomaly question
    print("\n[TEST 2] Anomaly Question")
    print("-" * 80)
    question2 = "Are there any unusual sales patterns recently?"
    result2 = agent.process_question(question2)
    print(f"Question: {question2}")
    print(f"Tools Used: {', '.join(result2['tools_used'])}")
    print(f"Answer: {result2['answer']}")
    print(f"Confidence: {result2['confidence']:.0%}")

    # Test Case 3: Combined question
    print("\n[TEST 3] Combined Question")
    print("-" * 80)
    question3 = "Forecast next 30 days and detect any anomalies"
    result3 = agent.process_question(question3)
    print(f"Question: {question3}")
    print(f"Tools Used: {', '.join(result3['tools_used'])}")
    print(f"Answer: {result3['answer']}")
    print(f"Confidence: {result3['confidence']:.0%}")

    # Test Case 4: Unsupported question with guidance
    print("\n[TEST 4] Unsupported Question (with Guidance)")
    print("-" * 80)
    question4 = "Tell me a joke"
    result4 = agent.process_question(question4)
    print(f"Question: {question4}")
    print(f"Tools Used: {result4['tools_used'] or 'None (showing guidance)'}")
    print(f"Answer: {result4['answer']}")
    print(f"Confidence: {result4['confidence']:.0%}")

    print("\n" + "=" * 80)
    print("ALL AGENT TESTS COMPLETE")
    print("=" * 80)
