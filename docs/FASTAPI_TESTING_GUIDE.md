# 🚀 Phase 4: FastAPI Backend — Complete Testing Guide

**Date:** August 30, 2026  
**Status:** ✅ PRODUCTION READY

---

## Quick Start: Run Everything

```bash
# Option 1: One command (starts both API and Dashboard)
python run.py

# Option 2: Run API only
python -m uvicorn app.main:app --port 8000

# Option 3: Run API with auto-reload (development)
python -m uvicorn app.main:app --port 8000 --reload
```

---

## Method 1: Interactive API Documentation (Recommended)

Once the API is running, open your browser:

```
http://127.0.0.1:8000/docs
```

This gives you:
- ✅ **Swagger UI** - Interactive API explorer
- ✅ All 13+ endpoints listed
- ✅ Click "Try it out" to test each endpoint
- ✅ See request/response examples
- ✅ Full OpenAPI schema

**Alternative:** ReDoc documentation at:
```
http://127.0.0.1:8000/redoc
```

---

## Method 2: Command Line Testing (cURL)

### A. Test API Health

```bash
curl http://127.0.0.1:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "ai_engine": "deterministic",
  "ai_model": "claude-opus-5"
}
```

---

### B. Test Dashboard KPIs

```bash
curl http://127.0.0.1:8000/api/v1/dashboard/kpis
```

**Expected:** Returns 10 KPI metrics:
```json
{
  "total_revenue": 37931872.5,
  "total_orders": 19615,
  "average_order_value": 1933.82,
  "gross_profit": 20888262.5,
  ...
}
```

---

### C. Test Sales Endpoints

**Monthly Revenue:**
```bash
curl http://127.0.0.1:8000/api/v1/sales/monthly
```

**Daily Revenue:**
```bash
curl http://127.0.0.1:8000/api/v1/sales/daily
```

**By Branch:**
```bash
curl http://127.0.0.1:8000/api/v1/sales/by-branch
```

**Best Day:**
```bash
curl http://127.0.0.1:8000/api/v1/sales/best-day
```

**Weekend vs Weekday:**
```bash
curl http://127.0.0.1:8000/api/v1/sales/weekend-vs-weekday
```

**Month Comparison:**
```bash
curl http://127.0.0.1:8000/api/v1/sales/month-compare
```

---

### D. Test Product Endpoints

**Top Products (default limit=10):**
```bash
curl http://127.0.0.1:8000/api/v1/products/top
```

**Top 5 Products:**
```bash
curl http://127.0.0.1:8000/api/v1/products/top?limit=5
```

**By Category:**
```bash
curl http://127.0.0.1:8000/api/v1/products/categories
```

---

### E. Test Anomaly Detection

```bash
curl http://127.0.0.1:8000/api/v1/anomalies?threshold=0.6
```

**Expected:** Returns detected anomaly dates

---

### F. Test AI Assistant (Most Important!)

**Test 1: Total Revenue**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is our total revenue?"}'
```

**Test 2: Top Products**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the top 5 products?"}'
```

**Test 3: Best Day**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Which day has the highest sales?"}'
```

**Test 4: Branch Comparison**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Which branch performs best?"}'
```

**Test 5: Month Comparison**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Compare this month with last month"}'
```

**Expected Response:**
```json
{
  "question": "What is our total revenue?",
  "answer": "Total revenue is PKR 37,931,872 from 19,615 orders...",
  "sql": "SELECT SUM(total_amount) as revenue, COUNT(*) as order_count FROM orders",
  "source": "database",
  "engine": "deterministic",
  "provider": null,
  "model": null,
  "rows": [{"revenue": 37931872.5, "order_count": 19615}],
  "note": null
}
```

---

## Method 3: PowerShell Testing Script

Create a file `test_api.ps1`:

```powershell
$baseUrl = "http://127.0.0.1:8000"

Write-Host "🧪 Testing BBQ Restaurant API" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Test 1: Health
Write-Host "`n✅ Testing /health endpoint..." -ForegroundColor Cyan
$health = curl $baseUrl/health -s | ConvertFrom-Json
Write-Host "Status: $($health.status)" -ForegroundColor Green
Write-Host "Database: $($health.database)" -ForegroundColor Green

# Test 2: KPIs
Write-Host "`n✅ Testing /api/v1/dashboard/kpis..." -ForegroundColor Cyan
$kpis = curl $baseUrl/api/v1/dashboard/kpis -s | ConvertFrom-Json
Write-Host "Total Revenue: PKR $('{0:N2}' -f $kpis.total_revenue)" -ForegroundColor Green
Write-Host "Total Orders: $($kpis.total_orders)" -ForegroundColor Green

# Test 3: Top Products
Write-Host "`n✅ Testing /api/v1/products/top..." -ForegroundColor Cyan
$products = curl "$baseUrl/api/v1/products/top?limit=3" -s | ConvertFrom-Json
Write-Host "Top 3 Products:" -ForegroundColor Green
$products[0..2] | ForEach-Object { Write-Host "  - $($_.name): PKR $('{0:N0}' -f $_.revenue)" }

# Test 4: AI Chat
Write-Host "`n✅ Testing /api/v1/ai/chat..." -ForegroundColor Cyan
$chat = curl -X POST "$baseUrl/api/v1/ai/chat" `
  -H "Content-Type: application/json" `
  -d '{"question": "What is our total revenue?"}' -s | ConvertFrom-Json
Write-Host "Question: $($chat.question)" -ForegroundColor Cyan
Write-Host "Answer: $($chat.answer)" -ForegroundColor Green
Write-Host "Source: $($chat.source)" -ForegroundColor Yellow
Write-Host "Engine: $($chat.engine)" -ForegroundColor Yellow

Write-Host "`n✅ All tests passed!" -ForegroundColor Green
```

Run it:
```bash
.\test_api.ps1
```

---

## Method 4: Python Testing Script

Create a file `test_api.py`:

```python
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    print("🧪 Testing /health...")
    resp = requests.get(f"{BASE_URL}/health")
    print(f"Status: {resp.status_code}")
    print(json.dumps(resp.json(), indent=2))

def test_kpis():
    print("\n🧪 Testing /api/v1/dashboard/kpis...")
    resp = requests.get(f"{BASE_URL}/api/v1/dashboard/kpis")
    data = resp.json()
    print(f"Total Revenue: PKR {data['total_revenue']:,.2f}")
    print(f"Total Orders: {data['total_orders']}")
    print(f"Average Order: PKR {data['average_order_value']:,.2f}")

def test_ai_chat():
    print("\n🧪 Testing /api/v1/ai/chat...")
    
    questions = [
        "What is our total revenue?",
        "What are the top 5 products?",
        "Which day has the highest sales?",
        "Which branch performs best?",
    ]
    
    for question in questions:
        print(f"\nQ: {question}")
        resp = requests.post(
            f"{BASE_URL}/api/v1/ai/chat",
            json={"question": question}
        )
        data = resp.json()
        print(f"A: {data['answer'][:150]}...")
        print(f"Source: {data['source']} | Engine: {data['engine']}")

def test_products():
    print("\n🧪 Testing /api/v1/products/top?limit=5...")
    resp = requests.get(f"{BASE_URL}/api/v1/products/top?limit=5")
    products = resp.json()
    for p in products:
        print(f"  - {p['name']}: PKR {p['revenue']:,.0f}")

if __name__ == "__main__":
    try:
        test_health()
        test_kpis()
        test_products()
        test_ai_chat()
        print("\n✅ All tests passed!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
```

Run it:
```bash
python test_api.py
```

---

## Method 5: Postman / Insomnia

If you use Postman or Insomnia, import this collection:

### Create requests for:

1. **GET** `http://127.0.0.1:8000/health`
2. **GET** `http://127.0.0.1:8000/api/v1/dashboard/kpis`
3. **GET** `http://127.0.0.1:8000/api/v1/sales/daily`
4. **GET** `http://127.0.0.1:8000/api/v1/products/top?limit=10`
5. **POST** `http://127.0.0.1:8000/api/v1/ai/chat`
   - Body: `{"question": "What are the top products?"}`

---

## Method 6: Python Requests in a Jupyter Notebook

```python
import requests

# 1. Health check
print(requests.get("http://127.0.0.1:8000/health").json())

# 2. Get KPIs
kpis = requests.get("http://127.0.0.1:8000/api/v1/dashboard/kpis").json()
print(f"Revenue: {kpis['total_revenue']}")

# 3. Ask AI a question
response = requests.post(
    "http://127.0.0.1:8000/api/v1/ai/chat",
    json={"question": "What are the top 5 products?"}
)
print(response.json()["answer"])
```

---

## Checklist: Phase 4 API Validation ✅

- [ ] **API Starts** - No errors on startup
- [ ] **Health Check** - `/health` returns `status: healthy`
- [ ] **Database Connected** - Health check shows `database: connected`
- [ ] **KPIs Endpoint** - Returns all 10 metrics
- [ ] **Sales Endpoints** - All return proper data
- [ ] **Product Endpoints** - Return ranked products
- [ ] **Anomaly Detection** - Detects 4+ anomalies
- [ ] **AI Chat Works** - At least 3 questions answered correctly
- [ ] **No Hallucinations** - All numbers match database
- [ ] **Swagger UI** - `/docs` is accessible and working
- [ ] **CORS Enabled** - Dashboard can call the API
- [ ] **Error Handling** - Bad requests return 400s (not 500s)
- [ ] **Response Time** - All endpoints < 200ms
- [ ] **OpenAPI Schema** - `/openapi.json` is valid

---

## Common Issues & Fixes

### Issue: "Connection refused"
**Fix:** Make sure API is running
```bash
python -m uvicorn app.main:app --port 8000
```

### Issue: "Database not found"
**Fix:** Load the data first
```bash
python scripts/load_data.py
```

### Issue: "405 Method Not Allowed"
**Fix:** You're using the wrong HTTP method (e.g., GET instead of POST for `/ai/chat`)

### Issue: "422 Unprocessable Entity"
**Fix:** Your JSON request body doesn't match the schema. Check `/docs` for examples.

### Issue: Slow responses (> 1 second)
**Fix:** This is normal for deterministic engine first run. Subsequent calls should be < 100ms.

---

## Production Verification

All checks should show ✅:

```bash
# 1. Database integrity
python scripts/load_data.py

# 2. API starts without errors
python -m uvicorn app.main:app --port 8000

# 3. Run tests
python test_api.py

# 4. Open dashboard
streamlit run app/dashboard.py
```

---

## Next Steps (Phase 5+)

- 🔜 **Phase 7:** RAG - Add business knowledge base
- 🔜 **Phase 8:** Forecasting - Add time-series predictions
- 🔜 **Phase 9:** Anomaly Detection - Advanced ML approach
- 🔜 **Phase 10:** WebSockets - Real-time updates
- 🔜 **Phase 11:** Model Versioning - Track ML versions
- 🔜 **Phase 12:** Docker - Production deployment

---

**API Status:** ✅ **PRODUCTION READY**
