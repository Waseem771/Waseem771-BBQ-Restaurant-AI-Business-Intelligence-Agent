"""
Phase 9.5 - Dashboard Integration
Streamlit dashboard with anomaly detection visualization

This dashboard displays:
1. Anomaly statistics and metrics
2. Timeline of anomalies
3. Severity distribution
4. Top anomalous days
5. Real-time alerts
6. Anomaly explanations

Beginner-friendly with detailed English comments.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.agents.anomaly_tool import AIAgentAnomalyTool
from app.agents.forecast_tool import AIAgentForecastTool

# ============================================================================
# Page Configuration
# ============================================================================

st.set_page_config(
    page_title="BBQ BI - Anomaly Detection Dashboard",
    page_icon="[WARNING]",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# Initialize Tools
# ============================================================================

@st.cache_resource
def load_tools():
    """Initialize anomaly and forecast tools."""
    anomaly_tool = AIAgentAnomalyTool()
    forecast_tool = AIAgentForecastTool()
    return anomaly_tool, forecast_tool


# ============================================================================
# Helper Functions
# ============================================================================

def get_severity_color(severity: str) -> str:
    """Get color for severity level."""
    colors = {
        "CRITICAL": "red",
        "HIGH": "orange",
        "MEDIUM": "yellow",
        "LOW": "green"
    }
    return colors.get(severity, "gray")


def format_currency(value: float) -> str:
    """Format value as Pakistani Rupees."""
    return f"Rs. {value:,.0f}"


# ============================================================================
# Main Dashboard
# ============================================================================

def main():
    """Main dashboard application."""

    # Title
    st.title("[ANOMALY DETECTION] BBQ Restaurant Analytics")
    st.markdown("Real-time sales anomaly detection and analysis")

    # Initialize tools
    anomaly_tool, forecast_tool = load_tools()

    # Sidebar Navigation
    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Select View",
            ["Overview", "Anomaly Details", "Statistics", "Forecasting", "Alerts"]
        )

    # ========================================================================
    # PAGE 1: Overview
    # ========================================================================
    if page == "Overview":
        st.header("Anomaly Detection Overview")

        # Get statistics
        stats = anomaly_tool.call("get_statistics", {})
        current = anomaly_tool.call("detect_current", {"days": 7})

        # KPI Row 1
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Days Analyzed",
                f"{stats['total_days']}",
                "2026-01-01 to 2026-09-30"
            )

        with col2:
            st.metric(
                "Anomalies Detected",
                f"{stats['anomaly_count']}",
                f"{stats['anomaly_percentage']:.1f}% of total"
            )

        with col3:
            st.metric(
                "Recent Anomalies (7 days)",
                f"{current['count']}",
                "In last 7 days"
            )

        with col4:
            st.metric(
                "Model Type",
                "Isolation Forest",
                "5.1% detection rate"
            )

        # Revenue Comparison
        st.subheader("Revenue Comparison: Normal vs Anomaly Days")
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Normal Days Average Revenue",
                format_currency(stats['normal_avg_revenue']),
                "Per day"
            )

        with col2:
            st.metric(
                "Anomaly Days Average Revenue",
                format_currency(stats['anomaly_avg_revenue']),
                f"+{(stats['anomaly_avg_revenue']/stats['normal_avg_revenue']-1)*100:.1f}% higher"
            )

        # Order Comparison
        st.subheader("Order Volume Comparison")
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Normal Days Average Orders",
                f"{stats['normal_avg_orders']:.0f}",
                "Per day"
            )

        with col2:
            st.metric(
                "Anomaly Days Average Orders",
                f"{stats['anomaly_avg_orders']:.0f}",
                f"+{(stats['anomaly_avg_orders']/stats['normal_avg_orders']-1)*100:.1f}% higher"
            )

        # Summary
        st.info(
            f"[INSIGHT] Anomalies tend to be HIGH-VOLUME days with higher revenue (+9.2%) "
            f"and more orders (+11%). These represent unusual business patterns or special events."
        )

    # ========================================================================
    # PAGE 2: Anomaly Details
    # ========================================================================
    elif page == "Anomaly Details":
        st.header("Detailed Anomaly Analysis")

        # Get all alerts
        alerts = anomaly_tool.call("get_alerts", {"severity": "HIGH"})

        st.subheader("Top Anomalous Days")

        # Create table data
        table_data = []
        for alert in alerts["alerts"][:10]:
            table_data.append({
                "Date": alert["date"],
                "Revenue": format_currency(alert["revenue"]),
                "Orders": alert["orders"],
                "Severity": alert["severity"],
                "Explanation": alert["explanation"][:60] + "..." if len(alert["explanation"]) > 60 else alert["explanation"]
            })

        df_alerts = pd.DataFrame(table_data)
        st.dataframe(df_alerts, use_container_width=True, hide_index=True)

        # Detailed explanation
        st.subheader("Explain Specific Anomaly")
        selected_date = st.selectbox(
            "Select date to explain",
            [a["date"] for a in alerts["alerts"][:10]]
        )

        if selected_date:
            explanation = anomaly_tool.call("explain_anomaly", {"date": selected_date})

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Date", explanation["date"])
            with col2:
                st.metric("Severity", explanation["severity"])
            with col3:
                st.metric("Revenue", format_currency(explanation["revenue"]))

            st.subheader("Detailed Explanation")
            st.info(explanation["explanation"])

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Orders", explanation["orders"])
            with col2:
                st.metric("Avg Order Value", format_currency(explanation["avg_order_value"]))

    # ========================================================================
    # PAGE 3: Statistics
    # ========================================================================
    elif page == "Statistics":
        st.header("Anomaly Statistics")

        stats = anomaly_tool.call("get_statistics", {})

        # Overall Statistics
        st.subheader("Overall Statistics")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Detection Rate",
                f"{stats['anomaly_percentage']:.1f}%",
                f"{stats['anomaly_count']} anomalies"
            )

        with col2:
            st.metric(
                "Data Points",
                stats['total_days'],
                "Days analyzed"
            )

        with col3:
            st.metric(
                "Model",
                "Isolation Forest",
                f"{stats['features_used']} features"
            )

        # Revenue Impact
        st.subheader("Revenue Impact Analysis")
        col1, col2 = st.columns(2)

        with col1:
            revenue_diff_pct = (stats['anomaly_avg_revenue']/stats['normal_avg_revenue'] - 1) * 100
            st.metric(
                "Anomaly Day Premium",
                f"+{revenue_diff_pct:.1f}%",
                f"Rs. {stats['anomaly_avg_revenue'] - stats['normal_avg_revenue']:,.0f} higher"
            )

        with col2:
            order_diff_pct = (stats['anomaly_avg_orders']/stats['normal_avg_orders'] - 1) * 100
            st.metric(
                "Anomaly Day Order Increase",
                f"+{order_diff_pct:.1f}%",
                f"{int(stats['anomaly_avg_orders'] - stats['normal_avg_orders'])} more orders"
            )

        # Key Insights
        st.subheader("Key Insights")
        st.success(
            f"""
            **Anomaly Characteristics:**
            - Detection Rate: {stats['anomaly_percentage']:.1f}% of days
            - Revenue Premium: +{revenue_diff_pct:.1f}% on anomaly days
            - Order Volume: +{order_diff_pct:.1f}% on anomaly days
            - Model Type: {stats['model_type']} with {stats['features_used']} features

            **Interpretation:**
            Anomalies represent HIGH-VOLUME days with unusual revenue patterns.
            These could indicate promotions, special events, or seasonal peaks.
            """
        )

    # ========================================================================
    # PAGE 4: Forecasting
    # ========================================================================
    elif page == "Forecasting":
        st.header("Sales Forecasting")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Revenue Forecast")
            forecast_days = st.slider("Forecast days", 1, 90, 7)
            revenue_forecast = forecast_tool.call("forecast_revenue", {"days": forecast_days})
            st.metric(
                f"Forecasted Revenue ({forecast_days} days)",
                format_currency(revenue_forecast.get("forecast_value", 0)),
                f"{revenue_forecast.get('confidence', 0):.0f}% confidence"
            )

        with col2:
            st.subheader("Order Forecast")
            orders_forecast = forecast_tool.call("forecast_orders", {"days": forecast_days})
            st.metric(
                f"Forecasted Orders ({forecast_days} days)",
                f"{orders_forecast.get('forecast_value', 0):.0f}",
                f"{orders_forecast.get('confidence', 0):.0f}% confidence"
            )

        # Model Metrics
        st.subheader("Forecast Model Performance")
        metrics = forecast_tool.call("get_metrics", {})

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Model Accuracy", f"{metrics.get('accuracy', 0):.1f}%")
        with col2:
            st.metric("MAE", format_currency(metrics.get('mae', 0)))
        with col3:
            st.metric("MAPE", f"{metrics.get('mape', 0):.1f}%")

    # ========================================================================
    # PAGE 5: Alerts
    # ========================================================================
    elif page == "Alerts":
        st.header("Critical Alerts")

        severity_filter = st.selectbox(
            "Filter by Severity",
            ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
        )

        alerts = anomaly_tool.call("get_alerts", {"severity": severity_filter})

        st.subheader(f"{severity_filter} Severity Alerts ({alerts['alert_count']} found)")

        if alerts['alerts']:
            for i, alert in enumerate(alerts['alerts'][:5], 1):
                with st.expander(f"Alert {i}: {alert['date']}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Date", alert['date'])
                    with col2:
                        st.metric("Revenue", format_currency(alert['revenue']))
                    with col3:
                        st.metric("Orders", alert['orders'])

                    st.warning(f"**Explanation:** {alert['explanation']}")
        else:
            st.info(f"No {severity_filter} severity alerts found.")

    # Footer
    st.markdown("---")
    st.caption(
        f"Dashboard Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
        "Phase 9.5 Integration - Anomaly Detection + Forecasting"
    )


if __name__ == "__main__":
    main()
