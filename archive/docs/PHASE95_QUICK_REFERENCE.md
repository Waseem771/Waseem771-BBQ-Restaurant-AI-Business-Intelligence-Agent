# Phase 9.5 - Quick Reference Guide

## Files Overview

### Code Files Created (3 files)

#### 1. app/agents/main_agent.py
**Main AI Agent Orchestrator**
```python
from app.agents.main_agent import MainAIAgent

agent = MainAIAgent()
result = agent.process_question("What will be our revenue next week?")
print(result["answer"])
print(result["tools_used"])  # ['Forecast Tool']
print(result["confidence"])  # 0.5 (50%)
```

**Supported Questions:**
- "What will be our revenue in the next 7 days?"
- "Are there any unusual sales patterns?"
- "Forecast next 30 days and detect anomalies"
- "Show recent anomalies"
- "Get HIGH severity alerts"

#### 2. app/api/routes/anomalies.py
**FastAPI Endpoints**
```python
# Already integrated into app.main:app
# Available at http://localhost:8000/api/v1/anomalies/*
```

**5 Endpoints:**
```
GET /api/v1/anomalies/current?days=7
GET /api/v1/anomalies/statistics
GET /api/v1/anomalies/explain?date=2026-03-23
GET /api/v1/anomalies/alerts?severity=HIGH
GET /api/v1/anomalies/health
```

#### 3. dashboard_anomalies.py
**Streamlit Dashboard**
```bash
streamlit run dashboard_anomalies.py
# Opens at http://localhost:8501
```

**5 Pages:**
1. Overview - KPIs and metrics
2. Anomaly Details - Detailed analysis
3. Statistics - Statistical breakdown
4. Forecasting - Predictions
5. Alerts - Critical alerts

---

## Quick Start

### 1. Start FastAPI Server
```bash
cd "E:\BBQ Restaurant AI Business Intelligence Agent\Projects\BBQ Restaurant AI Business Intelligence Agent"
python -m uvicorn app.main:app --port 8000 --reload
```
Then open: http://localhost:8000/docs

### 2. Test API Endpoints
```bash
# Get anomaly statistics
curl http://localhost:8000/api/v1/anomalies/statistics

# Get recent anomalies
curl http://localhost:8000/api/v1/anomalies/current?days=7

# Explain specific anomaly
curl http://localhost:8000/api/v1/anomalies/explain?date=2026-03-23

# Get HIGH severity alerts
curl http://localhost:8000/api/v1/anomalies/alerts?severity=HIGH

# Health check
curl http://localhost:8000/api/v1/anomalies/health
```

### 3. Use AI Agent
```python
from app.agents.main_agent import MainAIAgent

agent = MainAIAgent()

# Forecast question
result = agent.process_question("What will be our revenue in the next 7 days?")
print(f"Answer: {result['answer']}")
print(f"Tools: {result['tools_used']}")
print(f"Confidence: {result['confidence']:.0%}")

# Anomaly question
result = agent.process_question("Are there any unusual sales patterns?")
print(f"Answer: {result['answer']}")
```

### 4. Run Dashboard
```bash
streamlit run dashboard_anomalies.py
```
Then open: http://localhost:8501

---

## Test Files

### Run All Tests
```bash
# End-to-End Integration Tests (13 tests)
python PHASE95_END_TO_END_TEST.py

# API Endpoint Tests (5 tests)
python PHASE95_API_TEST.py

# AI Agent Tests (4 tests)
python app/agents/main_agent.py
```

### Expected Results
```
PHASE95_END_TO_END_TEST.py
  Total Tests: 13
  Passed: 13
  Failed: 0
  Success Rate: 100%

PHASE95_API_TEST.py
  Total Tests: 5
  Passed: 5
  Failed: 0
  Success Rate: 100%
```

---

## API Response Examples

### GET /api/v1/anomalies/statistics
```json
{
  "total_days": 273,
  "anomaly_count": 14,
  "anomaly_percentage": 5.1,
  "normal_avg_revenue": 138294.0,
  "anomaly_avg_revenue": 150985.0,
  "normal_avg_orders": 71.0,
  "anomaly_avg_orders": 79.0,
  "model_type": "Isolation Forest",
  "features_used": 7
}
```

### GET /api/v1/anomalies/current?days=7
```json
{
  "summary": "In the last 7 days, detected 0 anomalies.",
  "anomalies": [],
  "count": 0,
  "period_days": 7
}
```

### GET /api/v1/anomalies/explain?date=2026-03-23
```json
{
  "date": "2026-03-23",
  "severity": "HIGH",
  "revenue": 378868.0,
  "orders": 199,
  "anomaly_score": -0.7172,
  "explanation": "Revenue 115% above 7-day average; High volatility (72.0%)",
  "avg_order_value": 1904.36,
  "orders_per_customer": 1.88
}
```

### GET /api/v1/anomalies/alerts?severity=HIGH
```json
{
  "severity": "HIGH",
  "alert_count": 14,
  "alerts": [
    {
      "date": "2026-03-23",
      "revenue": 378868.0,
      "orders": 199,
      "severity": "HIGH",
      "explanation": "Revenue 115% above 7-day average; High volatility (72.0%)"
    },
    ...
  ]
}
```

---

## Integration Points

### 1. AI Agent Integration
```python
# Automatically routes questions to appropriate tools
Agent -> Forecast Tool (for predictions)
      -> Anomaly Tool (for pattern detection)
      -> Combined (for multi-tool queries)
```

### 2. FastAPI Integration
```python
# Routes registered in app.main:app
app.include_router(anomalies.router)
# 5 endpoints automatically available
```

### 3. Dashboard Integration
```python
# Direct tool calls from dashboard
from app.agents.anomaly_tool import AIAgentAnomalyTool
from app.agents.forecast_tool import AIAgentForecastTool

anomaly_tool = AIAgentAnomalyTool()
forecast_tool = AIAgentForecastTool()

# Call tools directly
stats = anomaly_tool.call("get_statistics", {})
forecast = forecast_tool.call("forecast_revenue", {"days": 7})
```

---

## System Architecture

```
┌─────────────────┐
│  User Interface │
└────────┬────────┘
         │
    ┌────┴────────────────────────┐
    │                             │
    ▼                             ▼
┌─────────────┐          ┌──────────────────┐
│ FastAPI     │          │ Streamlit        │
│ REST API    │          │ Dashboard        │
└────┬────────┘          └────────┬─────────┘
     │                            │
     │    ┌───────────────────────┘
     │    │
     ▼    ▼
┌──────────────────────────┐
│  Main AI Agent           │
│  (app/agents/main_agent) │
└───────┬──────────────────┘
        │
    ┌───┴───────────────────┐
    │                       │
    ▼                       ▼
┌──────────────┐   ┌───────────────┐
│ Forecast     │   │ Anomaly       │
│ Tool         │   │ Tool          │
└──────────────┘   └───────────────┘
```

---

## Key Metrics

| Metric | Value |
|--------|-------|
| Response Time | < 1 second |
| Memory Usage | ~50 MB |
| Test Pass Rate | 100% (13/13) |
| API Endpoints | 5 |
| Dashboard Pages | 5 |
| AI Agent Tools | 2 |
| Anomalies Detected | 14 (5.1%) |
| Data Points | 273 days |

---

## Troubleshooting

### Issue: FastAPI won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Use different port
python -m uvicorn app.main:app --port 8001
```

### Issue: Dashboard won't load
```bash
# Make sure streamlit is installed
pip install streamlit

# Run with explicit host
streamlit run dashboard_anomalies.py --server.address=localhost
```

### Issue: Tools not initializing
```bash
# Check database connection
python -c "from app.db import query_rows; print(query_rows('SELECT 1'))"

# Check imports
python -c "from app.agents.main_agent import MainAIAgent; print('OK')"
```

---

## Next Steps

### Phase 10 - Real-Time Features
- WebSocket implementation
- Real-time alerts
- Live dashboard updates

### Production Deployment
- Docker containerization
- Environment configuration
- Monitoring setup

---

## Contact & Support

**Project:** BBQ Restaurant AI Business Intelligence Agent
**Phase:** 9.5 - Integration
**Status:** ✅ COMPLETE

**Key Files:**
- Main Agent: `app/agents/main_agent.py`
- API Routes: `app/api/routes/anomalies.py`
- Dashboard: `dashboard_anomalies.py`
- Tests: `PHASE95_END_TO_END_TEST.py`

**Documentation:**
- `PHASE95_INTEGRATION_COMPLETE.md` - Full summary
- `PHASE9_SUMMARY.md` - Phase 9 overview
- `PHASE8_SUMMARY.md` - Phase 8 overview

---

**Last Updated:** 2026-08-30  
**Version:** 1.0  
**Status:** Production Ready
