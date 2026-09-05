"""
Phase 8 - Sales Forecasting Quick Reference Guide
Beginner-friendly guide to using the forecasting system
"""

# ============================================================================
# QUICK START - 3 STEPS
# ============================================================================

QUICK_START = """
PHASE 8 - SALES FORECASTING QUICK START

Step 1: Run the Forecasting System
  Command: python app/forecasting.py
  Output: Model training and evaluation
  Time: ~10 seconds

Step 2: Test the Forecast Tool
  Command: python app/forecast_tool.py
  Output: 5 test cases with predictions
  Time: ~5 seconds

Step 3: Test AI Agent Integration
  Command: python app/agents/forecast_tool.py
  Output: 4 AI agent tests
  Time: ~5 seconds

All tests should PASS [OK]
"""

# ============================================================================
# FILE STRUCTURE
# ============================================================================

FILE_STRUCTURE = """
Phase 8 Files:

1. app/forecasting.py (500+ lines)
   - Main forecasting system
   - Model training
   - Evaluation
   - Runs standalone

2. app/forecast_tool.py (300+ lines)
   - Tool interface
   - Revenue/order forecasting
   - Confidence metrics
   - Easy integration

3. app/agents/forecast_tool.py (200+ lines)
   - AI agent integration
   - Formatted responses
   - 4 forecast actions
   - Ready for Groq LLM

4. app/api/routes/forecast.py (100+ lines)
   - FastAPI endpoints
   - REST integration
   - Query validation
   - Health check

5. PHASE8_FORECASTING_COMPLETE.md
   - Full documentation
   - Architecture details
   - Test results
"""

# ============================================================================
# HOW TO USE - CODE EXAMPLES
# ============================================================================

USAGE_EXAMPLES = """
Example 1: Forecast Revenue for Next 7 Days
═════════════════════════════════════════════

from app.forecast_tool import ForecastTool

# Initialize
tool = ForecastTool()

# Forecast revenue
forecast = tool.forecast_revenue(days=7)

print(f"Total: {forecast['predicted_total']:,.0f} PKR")
print(f"Daily Avg: {forecast['predicted_daily_avg']:,.0f} PKR")
print(f"Confidence: {forecast['confidence_accuracy']}")


Example 2: Forecast Order Volume
════════════════════════════════

forecast = tool.forecast_orders(days=30)

print(f"Total Orders: {forecast['predicted_total_orders']:,}")
print(f"Daily Avg Orders: {forecast['predicted_daily_avg_orders']:,}")


Example 3: Get Model Accuracy
══════════════════════════════

metrics = tool.get_forecast_confidence()

print(f"Model: {metrics['model_type']}")
print(f"Accuracy: {metrics['accuracy_confidence']}")
print(f"MAPE: {metrics['mape_percent']}")


Example 4: AI Agent Integration
════════════════════════════════

from app.agents.forecast_tool import AIAgentForecastTool

agent_tool = AIAgentForecastTool()

# Forecast revenue
result = agent_tool.call("forecast_revenue", {"days": 30})
print(result['summary'])

# Forecast orders
result = agent_tool.call("forecast_orders", {"days": 7})
print(result['summary'])

# Get metrics
result = agent_tool.call("get_metrics", {})
print(result['accuracy_confidence'])


Example 5: API Usage
════════════════════

# Start FastAPI server
# python -m uvicorn app.main:app --reload

# In browser or curl:
http://localhost:8000/api/v1/forecast/revenue?days=7
http://localhost:8000/api/v1/forecast/orders?days=30
http://localhost:8000/api/v1/forecast/confidence
http://localhost:8000/api/v1/forecast/by-period?period=next_month
"""

# ============================================================================
# KEY METRICS EXPLAINED
# ============================================================================

METRICS_EXPLAINED = """
Understanding Forecasting Metrics
═══════════════════════════════════

1. MAE (Mean Absolute Error)
   ─────────────────────────
   What: Average absolute difference between predicted and actual
   Formula: Average of |Predicted - Actual|

   Our Result: 15,998 PKR
   Meaning: On average, predictions are off by 15,998 PKR
   Good? YES - Very good for PKR-based forecasting

   Comparison:
   - Daily revenue: ~140,000 PKR
   - Error percentage: 15,998 / 140,000 = 11.4%


2. RMSE (Root Mean Squared Error)
   ────────────────────────────────
   What: Square root of average squared errors
   Formula: sqrt(Average of (Predicted - Actual)²)

   Our Result: 19,753 PKR
   Meaning: Penalizes larger errors more than smaller ones
   Why higher than MAE? Larger errors get squared

   Use: When large errors are costly


3. MAPE (Mean Absolute Percentage Error)
   ──────────────────────────────────────
   What: Average percentage error
   Formula: Average of |Predicted - Actual| / Actual

   Our Result: 13.65%
   Meaning: On average, predictions are 13.65% off
   Good? YES - Less than 15% is generally good

   Best for: Comparing across different scales


4. Accuracy (Confidence)
   ─────────────────────
   Formula: 100% - MAPE%

   Our Result: 86.35%
   Meaning: We're confident 86% of the time
   Interpretation: ~14 out of 100 predictions are significantly off


Model Comparison:
─────────────────
Linear Regression (Baseline):
  MAE:  25,009 PKR  (worse)
  MAPE: 20.12%      (worse)

Random Forest (SELECTED):
  MAE:  15,998 PKR  (better)
  MAPE: 13.65%      (better)

Improvement: 36% better with Random Forest!
"""

# ============================================================================
# FEATURES USED BY MODEL
# ============================================================================

FEATURES_EXPLAINED = """
How the Model Makes Predictions
═════════════════════════════════

The Random Forest model uses 5 features:

1. day_of_week
   Values: 0-6 (Monday=0, Sunday=6)
   Why: Sales vary by day (weekends higher)
   Example: Friday (4) → Higher revenue expected

2. month
   Values: 1-12
   Why: Sales vary seasonally
   Example: Ramadan might have different patterns

3. quarter
   Values: 1-4 (Q1, Q2, Q3, Q4)
   Why: Quarterly business trends
   Example: Q4 might be higher due to holidays

4. is_weekend
   Values: 0 (weekday) or 1 (weekend)
   Why: Weekend vs weekday behavior
   Example: Saturday (1) → Boost in revenue

5. revenue_ma7
   Values: Rolling 7-day average
   Why: Captures recent trend
   Example: If trend is up, forecast is higher


How Predictions Work:
─────────────────────
For each future date:
1. Extract features (day_of_week, month, etc.)
2. Feed to Random Forest model
3. Model combines 100 decision trees
4. Each tree votes on the prediction
5. Average of all votes = Final prediction

Example for 2026-10-05 (Saturday):
  day_of_week = 5 (Saturday)
  month = 10 (October)
  quarter = 4 (Q4)
  is_weekend = 1 (Saturday = weekend)
  revenue_ma7 = 135,000 (recent average)

  Model predicts: 210,000 PKR
  (Weekend boost over 135,000 baseline)
"""

# ============================================================================
# INTEGRATION CHECKLIST
# ============================================================================

INTEGRATION_CHECKLIST = """
Phase 8 Integration Checklist
══════════════════════════════

For AI Agent Integration:
  [ ] Import AIAgentForecastTool
  [ ] Add to agent's tool list
  [ ] Test with sample queries
  [ ] Verify response formatting
  [ ] Add to Groq LLM agent

For Dashboard Integration:
  [ ] Import forecast functions
  [ ] Create forecasting tab
  [ ] Add charts for predictions
  [ ] Display confidence scores
  [ ] Add period selector

For API Integration:
  [ ] Import forecast router
  [ ] Add to main.py routes
  [ ] Test endpoints
  [ ] Document endpoints
  [ ] Add to OpenAPI docs

For Database Integration:
  [ ] Store predictions (optional)
  [ ] Create predictions table
  [ ] Log forecasts made
  [ ] Track accuracy over time
  [ ] Enable model retraining
"""

# ============================================================================
# TROUBLESHOOTING
# ============================================================================

TROUBLESHOOTING = """
Common Issues and Solutions
═════════════════════════════

Issue 1: ModuleNotFoundError
  Error: "No module named 'app'"
  Solution: Run from project root directory
  Command: cd "E:/BBQ Restaurant AI Business Intelligence Agent/Projects/BBQ Restaurant AI Business Intelligence Agent"
  Then: python app/forecasting.py

Issue 2: DatabaseNotFoundError
  Error: "Database not found at..."
  Solution: Ensure data/bbq.db exists
  Check: ls -la data/
  Or: Run data loading script first

Issue 3: ImportError sklearn
  Error: "No module named 'sklearn'"
  Solution: Install scikit-learn
  Command: pip install scikit-learn

Issue 4: Encoding errors (Unicode)
  Error: "UnicodeEncodeError"
  Solution: Already fixed in code
  Use: Plain ASCII characters in print statements

Issue 5: Model not trained
  Error: "Model not trained"
  Solution: ForecastTool trains automatically
  Check: tool.trained == True
  Debug: Check database connection

Issue 6: Prophet not installed
  Warning: "Prophet not installed"
  This is OK - Prophet is optional
  Code defaults to Random Forest
  To install: pip install prophet
"""

# ============================================================================
# NEXT STEPS
# ============================================================================

NEXT_STEPS = """
Phase 8 Complete! What's Next?
═══════════════════════════════

Immediate Tasks (This Week):
  1. Integrate forecast tool with AI agent
  2. Add forecasting endpoints to FastAPI
  3. Test combined queries (SQL + Forecast)
  4. Add forecasting tab to dashboard

Short-term (Next 2 Weeks):
  1. Add confidence intervals to predictions
  2. Implement model retraining pipeline
  3. Add product-level forecasting
  4. Add branch-level forecasting

Medium-term (Phase 9):
  1. Start Anomaly Detection module
  2. Real-time monitoring
  3. Automatic alerts
  4. Pattern explanation

Long-term (Phase 10):
  1. WebSocket real-time updates
  2. Advanced features
  3. A/B model testing
  4. Production deployment

Recommended Priority:
  1. Phase 8.5 - Integration (2 days)
  2. Phase 9 - Anomaly Detection (3 days)
  3. Phase 10 - Real-time (2 days)
  4. Production deployment (1 day)
"""

# ============================================================================
# PRINT ALL GUIDES
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("PHASE 8 - SALES FORECASTING QUICK REFERENCE")
    print("=" * 80)

    print("\n" + "=" * 80)
    print("1. QUICK START")
    print("=" * 80)
    print(QUICK_START)

    print("\n" + "=" * 80)
    print("2. FILE STRUCTURE")
    print("=" * 80)
    print(FILE_STRUCTURE)

    print("\n" + "=" * 80)
    print("3. USAGE EXAMPLES")
    print("=" * 80)
    print(USAGE_EXAMPLES)

    print("\n" + "=" * 80)
    print("4. METRICS EXPLAINED")
    print("=" * 80)
    print(METRICS_EXPLAINED)

    print("\n" + "=" * 80)
    print("5. FEATURES EXPLAINED")
    print("=" * 80)
    print(FEATURES_EXPLAINED)

    print("\n" + "=" * 80)
    print("6. INTEGRATION CHECKLIST")
    print("=" * 80)
    print(INTEGRATION_CHECKLIST)

    print("\n" + "=" * 80)
    print("7. TROUBLESHOOTING")
    print("=" * 80)
    print(TROUBLESHOOTING)

    print("\n" + "=" * 80)
    print("8. NEXT STEPS")
    print("=" * 80)
    print(NEXT_STEPS)

    print("\n" + "=" * 80)
    print("END OF QUICK REFERENCE")
    print("=" * 80)
