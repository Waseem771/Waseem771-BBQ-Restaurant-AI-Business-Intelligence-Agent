# 🤖 AI Forecasting Chatbot - Feature Proposal

## Overview

Add an intelligent AI chatbot to the **Forecasting** section that allows users to ask natural language questions about future predictions and get AI-powered insights.

---

## User Experience

### What Users Will See

In the Forecasting section, there will be:

1. **Existing Components** (unchanged)
   - 6-month revenue forecast chart
   - Historical monthly data
   - Best sales day metrics

2. **NEW: AI Forecasting Assistant** (bottom section)
   ```
   ┌─────────────────────────────────┐
   │  🤖 AI Forecasting Assistant    │
   ├─────────────────────────────────┤
   │                                 │
   │  Sample Questions:              │
   │  • What's our revenue trend?    │
   │  • When will we hit target?     │
   │  • Which products will grow?    │
   │  • What's the best time to...?  │
   │                                 │
   │  [User types question here...] │
   │  [Send button]                  │
   │                                 │
   │  💬 Chat History                │
   │  AI: Based on trends...         │
   │  User: When will sales peak?    │
   │  AI: Expected peak on...        │
   │                                 │
   └─────────────────────────────────┘
   ```

### Example Questions Users Can Ask

```
1. "What will our revenue be next month?"
   → AI: "Based on current trend, ~₨2.8M"

2. "Which product will grow the most?"
   → AI: "BBQ Platters showing 15% growth trend"

3. "Should we increase inventory?"
   → AI: "Yes, demand forecast shows +20% in Q4"

4. "When is the best time to launch a promotion?"
   → AI: "Mid-month shows 30% higher engagement"

5. "What risks do we face?"
   → AI: "Seasonal decline in Aug, plan promotions"

6. "Compare forecasts - which branch will perform best?"
   → AI: "Branch A ahead by ₨500K based on patterns"

7. "What's the confidence level of this forecast?"
   → AI: "85% confidence based on 12-month history"

8. "How should we optimize revenue?"
   → AI: "Focus on Sides - high margin, growing demand"
```

---

## Technical Architecture

### Frontend Component Structure

```
Forecasting Component
├── Existing Forecasting Data Section
│   ├── KPI Cards
│   ├── 6-month Forecast Chart
│   └── Historical Monthly Data
│
└── NEW: ForecastingChatbot Component
    ├── Quick Suggestion Buttons
    ├── Chat Input Area
    ├── Chat Message History
    └── Loader for AI Response
```

### Backend API Endpoint

**New endpoint needed:**
```
POST /api/v1/ai/forecast-chat
Content-Type: application/json

{
  "question": "What will our revenue be next month?",
  "context": {
    "forecast_data": [...],
    "historical_data": [...],
    "current_metrics": {...}
  }
}

Response:
{
  "answer": "Based on current trend...",
  "confidence": 0.85,
  "reasoning": "The forecast model shows...",
  "data_used": ["monthly_forecast", "trend_analysis"],
  "recommendations": ["Focus on X", "Monitor Y"]
}
```

---

## Implementation Plan

### Phase 1: Create Chatbot Component (2-3 hours)

**File:** `frontend/src/components/ForecastingChatbot.jsx`

```javascript
import React, { useState, useRef, useEffect } from 'react';
import { Send, MessageSquare, Loader } from 'lucide-react';

export default function ForecastingChatbot({ forecastData, historicalData }) {
  const [messages, setMessages] = useState([
    { 
      role: 'assistant', 
      text: "👋 Hi! I'm your Forecasting Assistant. Ask me anything about future predictions, trends, and recommendations!" 
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const bottomRef = useRef(null);

  // Quick suggestion questions
  const QUICK_QUESTIONS = [
    "What's our revenue forecast for next month?",
    "Which product will grow the most?",
    "When should we launch a promotion?",
    "What are the risks in this forecast?",
  ];

  // Auto-scroll to bottom
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Send message to AI backend
  async function sendMessage(question) {
    try {
      const userQuestion = (question || input).trim();
      if (!userQuestion) return;

      setInput('');
      setError(null);
      setMessages(prev => [...prev, { role: 'user', text: userQuestion }]);
      setLoading(true);

      // Call backend AI endpoint
      const response = await fetch('http://localhost:8000/api/v1/ai/forecast-chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: userQuestion,
          context: {
            forecast_data: forecastData,
            historical_data: historicalData
          }
        })
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      const data = await response.json();
      setMessages(prev => [...prev, {
        role: 'assistant',
        text: data.answer,
        confidence: data.confidence,
        recommendations: data.recommendations
      }]);
    } catch (err) {
      setError(err.message);
      setMessages(prev => [...prev, {
        role: 'assistant',
        text: '⚠️ Could not process your question. Please try again.'
      }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', marginTop: '2rem' }}>
      <h2 className="section-title">🤖 Forecasting Assistant</h2>

      {/* Quick Suggestions */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
        {QUICK_QUESTIONS.map((q, i) => (
          <button
            key={i}
            onClick={() => sendMessage(q)}
            disabled={loading}
            style={{
              padding: '0.5rem 1rem',
              background: '#FFF5F0',
              border: '1px solid #FDDDD5',
              borderRadius: 20,
              fontSize: '0.8rem',
              color: '#D84C1A',
              cursor: 'pointer',
              opacity: loading ? 0.6 : 1,
            }}
          >
            {q}
          </button>
        ))}
      </div>

      {/* Chat Window */}
      <div style={{
        minHeight: 320,
        maxHeight: 400,
        overflowY: 'auto',
        background: '#F8F6F2',
        borderRadius: 12,
        padding: '1rem',
        border: '1px solid #E8E6E2',
        display: 'flex',
        flexDirection: 'column',
        gap: '0.75rem',
      }}>
        {messages.map((msg, i) => (
          <div key={i} style={{
            display: 'flex',
            justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start'
          }}>
            <div style={{
              maxWidth: '75%',
              padding: '0.75rem 1rem',
              borderRadius: msg.role === 'user' ? '16px 16px 4px 16px' : '16px 16px 16px 4px',
              background: msg.role === 'user' ? '#D84C1A' : '#fff',
              color: msg.role === 'user' ? '#fff' : '#1A1A1A',
              fontSize: '0.875rem',
              lineHeight: 1.5,
              boxShadow: '0 1px 4px rgba(0,0,0,0.08)',
            }}>
              {msg.text}
              {msg.confidence && (
                <p style={{ fontSize: '0.7rem', color: '#8B8B8B', marginTop: 6 }}>
                  Confidence: {(msg.confidence * 100).toFixed(0)}%
                </p>
              )}
              {msg.recommendations && (
                <ul style={{ fontSize: '0.75rem', marginTop: 6, paddingLeft: '1rem' }}>
                  {msg.recommendations.map((rec, j) => (
                    <li key={j}>{rec}</li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div style={{ color: '#8B8B8B', fontSize: '0.85rem' }}>
            🤖 Thinking...
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input Area */}
      <div style={{ display: 'flex', gap: '0.5rem' }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && !loading && sendMessage()}
          placeholder="Ask about forecasts, trends, and recommendations..."
          disabled={loading}
          style={{
            flex: 1,
            padding: '0.75rem 1rem',
            border: '1px solid #E8E6E2',
            borderRadius: 8,
            fontSize: '0.875rem',
            outline: 'none',
          }}
        />
        <button
          onClick={() => sendMessage()}
          disabled={loading || !input.trim()}
          style={{
            padding: '0.75rem 1.5rem',
            background: '#D84C1A',
            color: '#fff',
            border: 'none',
            borderRadius: 8,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: 6,
            opacity: loading || !input.trim() ? 0.6 : 1,
          }}
        >
          <Send size={16} /> Send
        </button>
      </div>

      {error && (
        <div style={{
          padding: '0.75rem 1rem',
          background: '#FFF5F0',
          border: '1px solid #FDDDD5',
          borderRadius: 8,
          color: '#C0392B',
          fontSize: '0.875rem',
        }}>
          ⚠️ {error}
        </div>
      )}
    </div>
  );
}
```

### Phase 2: Update Forecasting Component (30 min)

Add the chatbot to `Forecasting()` function in Dashboard.jsx:

```javascript
// At bottom of Forecasting() return, add:
<ForecastingChatbot 
  forecastData={forecastData} 
  historicalData={monthly}
/>
```

### Phase 3: Create Backend Endpoint (1-2 hours)

**File:** `backend/app/api/routes/ai.py`

```python
@router.post("/forecast-chat")
async def forecast_chat(request: ForecastChatRequest):
    """
    AI-powered forecasting chatbot
    Answers questions about future predictions
    """
    try:
        # Extract context
        forecast_data = request.context.get('forecast_data', [])
        historical_data = request.context.get('historical_data', [])
        
        # Prepare context for LLM
        context = prepare_forecast_context(
            forecast_data, 
            historical_data
        )
        
        # Call AI agent with forecasting tools
        answer = await forecast_agent.run(
            question=request.question,
            context=context,
            tools=[
                predict_revenue,
                analyze_trends,
                identify_risks,
                recommend_actions
            ]
        )
        
        return {
            "answer": answer['response'],
            "confidence": answer.get('confidence', 0.8),
            "reasoning": answer.get('reasoning', ''),
            "recommendations": answer.get('recommendations', []),
            "data_used": answer.get('data_used', [])
        }
    except Exception as e:
        return {"error": str(e)}
```

---

## Backend AI Agent Tools

The forecasting agent should have these tools:

### Tool 1: `predict_revenue(period, confidence_level)`
```
Predicts revenue for a specified period
Returns: Expected revenue, confidence interval, key factors
```

### Tool 2: `analyze_trends(metric, time_range)`
```
Analyzes trends in any metric
Returns: Trend direction, growth rate, seasonality patterns
```

### Tool 3: `identify_risks(forecast_data)`
```
Identifies potential risks in forecasts
Returns: Risk factors, probability, impact assessment
```

### Tool 4: `recommend_actions(analysis)`
```
Generates business recommendations based on analysis
Returns: Action items, priority, expected impact
```

### Tool 5: `compare_forecasts(metric1, metric2)`
```
Compares forecasts between products/branches
Returns: Comparison analysis, winner, reasoning
```

---

## Features to Implement

### Phase 1: MVP (Week 1)
- [x] Basic chat UI
- [x] Send/receive messages
- [x] Quick suggestion buttons
- [x] Error handling
- [ ] Backend `forecast-chat` endpoint
- [ ] AI agent integration

### Phase 2: Enhanced (Week 2)
- [ ] Confidence scores display
- [ ] Recommendations section
- [ ] Export analysis to PDF
- [ ] Save chat history
- [ ] Multi-language support

### Phase 3: Advanced (Week 3)
- [ ] Real-time forecast updates
- [ ] Trend visualization in chat
- [ ] Integration with alerts system
- [ ] Predictive follow-up questions
- [ ] User preference learning

---

## Example Interactions

### Example 1: Revenue Forecast
```
User: "What will our revenue be next quarter?"

AI: "Based on historical data and current trends:

Q4 Forecast:
• October: ₨2.8M (confidence: 92%)
• November: ₨3.1M (confidence: 89%)
• December: ₨3.5M (confidence: 75%, seasonal boost)

Key factors:
✓ 8% monthly growth trend
✓ Holiday season impact
⚠ Inventory risks in Nov

Recommendations:
1. Increase inventory 25% for Nov-Dec
2. Plan Q4 promotions now
3. Monitor competitor activity"

Confidence: 88%
```

### Example 2: Product Growth Analysis
```
User: "Which products will grow the most?"

AI: "Growth Analysis:

🏆 Top Growing Products:
1. BBQ Platters: +22% projected growth
   - Current: ₨850K/month
   - Forecast: ₨1.04M/month
   - Reason: Increasing demand on weekends

2. Premium Sides: +18% growth
   - Pairing well with platters
   - Higher margin opportunity

3. Beverages: +12% growth
   - Seasonal summer demand
   - Weather-dependent

⚠ Declining Products:
- Budget Meals: -8% (customer switching to premium)

Recommendations:
✓ Promote BBQ Platters
✓ Bundle sides with platters
✓ Refresh budget meals menu"

Confidence: 82%
```

### Example 3: Risk Assessment
```
User: "What risks should we be aware of?"

AI: "Forecast Risk Analysis:

🚨 High Risk Factors:
1. Weather Dependency (Aug-Sep)
   - Monsoon season impact
   - 15-20% revenue variance
   - Mitigation: Indoor dining promotions

2. Seasonal Decline (July)
   - Historical 12% dip
   - Plan discounts in advance

3. Competitor Activity
   - New branch opening nearby
   - Prepare differentiation strategy

⚠ Medium Risk:
- Supply chain delays (15% probability)
- Staff turnover in summer

✓ Confidence: 85%

Action Items:
1. Prepare contingency budget
2. Increase marketing in July
3. Diversify supplier base"
```

---

## Data Flow

```
User Question
    ↓
Frontend Chat Component
    ↓
POST /api/v1/ai/forecast-chat
    ↓
Backend AI Agent
    ├── Prepare context (forecast + historical data)
    ├── Route to appropriate tools
    ├── Tool 1: Predict Revenue
    ├── Tool 2: Analyze Trends
    ├── Tool 3: Identify Risks
    ├── Tool 4: Recommend Actions
    └── Combine results with LLM
    ↓
AI Response
    ├── Main answer
    ├── Confidence score
    ├── Reasoning
    ├── Recommendations
    └── Data sources used
    ↓
Frontend Display
    ├── Message in chat
    ├── Show confidence
    ├── Display recommendations
    └── Format nicely
```

---

## Suggested Questions to Surface

```javascript
const QUICK_QUESTIONS = [
  "What's our revenue forecast for next month?",
  "Which product will grow the most?",
  "When should we launch a promotion?",
  "What are the risks in this forecast?",
  "Should we increase inventory?",
  "Compare sales between branches",
  "What's the confidence level of forecasts?",
  "Optimize revenue recommendations",
];
```

---

## Integration with Existing Features

### Connects to:
1. **Forecasting Models** - Uses ML predictions
2. **Historical Sales Data** - Analyzes patterns
3. **AI Agent System** - Uses same reasoning engine
4. **Database** - Retrieves context data
5. **Alert System** - Can trigger alerts based on risks

### Similar to:
- **AIChat component** - Same chat UI pattern
- **Overview/Analytics** - Same data sources
- **ML Engine** - Uses prediction models

---

## Timeline & Effort

| Phase | Component | Time | Effort |
|-------|-----------|------|--------|
| 1 | Chat UI | 2h | Easy |
| 1 | Integration | 30m | Easy |
| 1 | Backend endpoint | 2h | Medium |
| 2 | AI agent tools | 3h | Hard |
| 2 | Enhanced features | 2h | Medium |
| 3 | Advanced features | 4h | Hard |
| **Total** | | **13.5h** | |

**Recommendation:** Start with Phase 1 MVP (4.5h) to test concept, then expand based on feedback.

---

## Success Metrics

When feature is complete, measure:
- ✅ User engagement (% using chatbot)
- ✅ Question types (what users ask)
- ✅ AI accuracy (confidence scores)
- ✅ User satisfaction (ratings)
- ✅ Time to insights (minutes saved)
- ✅ Forecast accuracy (model validation)

---

## Next Steps

1. **Approve concept** - Is this what you want?
2. **Build Phase 1** - Create chatbot component (2h)
3. **Build Phase 2** - Create backend endpoint (2h)
4. **Test** - Ask sample questions (30m)
5. **Iterate** - Improve based on feedback (ongoing)

**Ready to start?** Let me know and I'll build it! 🚀

---

**Document Created:** 2026-09-02  
**Status:** Ready for Development  
**Complexity:** Medium  
**User Impact:** High Value Feature
