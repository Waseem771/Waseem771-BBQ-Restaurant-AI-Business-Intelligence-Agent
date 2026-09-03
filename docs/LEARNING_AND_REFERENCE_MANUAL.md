# 📚 Complete Learning & Reference Manual

**BBQ Restaurant AI Business Intelligence Platform**  
**Comprehensive Guide for Understanding, Maintaining & Extending the System**  
**Date: 2026-08-31**

---

## 🎓 Learning Path for Beginners

### Module 1: Understanding the Project (1-2 hours)

**1.1 What is this project?**
```
A complete AI-powered analytics platform for BBQ restaurants that:
- Analyzes sales and business data in real-time
- Answers natural language questions (e.g., "Why did sales drop?")
- Predicts future sales trends
- Detects unusual business patterns
- Provides actionable insights
- Scales to enterprise deployments
```

**1.2 Key Components**
```
FRONTEND (React)
    ↓
BACKEND (FastAPI)
    ↓
DATABASE (SQLite)
    ↓
ML ENGINE (Forecasting & Anomalies)
    ↓
AI AGENT (Claude LLM with RAG)
```

**1.3 Business Value**
```
For Restaurant Managers:
✓ Real-time visibility into performance
✓ Early warnings of problems
✓ Data-driven decision making
✓ Forecast planning

For IT/DevOps:
✓ Scalable architecture
✓ Easy maintenance
✓ Production-ready code
✓ Complete documentation
```

---

### Module 2: Architecture Overview (2-3 hours)

**2.1 System Architecture**

```
┌─────────────────────────────────────────────────────┐
│                   USER INTERACTION                  │
│  (Web Browser, Mobile, Desktop Application)         │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP/WebSocket
                       ▼
┌─────────────────────────────────────────────────────┐
│              FRONTEND LAYER (React)                 │
│                                                     │
│  • BBQDashboard Component (470 lines)              │
│  • Real-time KPI Cards                            │
│  • Charts (Recharts)                              │
│  • AI Chat Panel                                  │
│  • Navigation & Settings                          │
└──────────────────────┬──────────────────────────────┘
                       │ REST API + WebSocket
                       ▼
┌─────────────────────────────────────────────────────┐
│              FASTAPI BACKEND LAYER                 │
│                                                     │
│  Routes:                                           │
│  • /api/v1/dashboard (KPIs)                       │
│  • /api/v1/sales (Analytics)                      │
│  • /api/v1/ai/chat (AI Assistant)                 │
│  • /api/v1/models (Version Management)            │
│  • /api/v1/anomalies (Detection)                  │
│  • /api/v1/ml/forecast (Predictions)              │
│  • /ws (WebSocket)                                │
└──────────────────────┬──────────────────────────────┘
                       │ SQL
                       ▼
┌─────────────────────────────────────────────────────┐
│               BUSINESS LOGIC LAYER                  │
│                                                     │
│  Services:                                         │
│  • SalesAnalyticsService                          │
│  • AnomalyDetectionService                        │
│  • ForecastingService                             │
│  • ChatService                                    │
│  • ModelRegistryService                           │
└──────────────────────┬──────────────────────────────┘
                       │ Data Access
                       ▼
┌─────────────────────────────────────────────────────┐
│              DATA & STORAGE LAYER                   │
│                                                     │
│  SQLite Database:                                 │
│  • orders (8,000+ records)                        │
│  • sales_daily (273 days)                         │
│  • products (50+ types)                           │
│  • anomalies (detected events)                    │
│  • model_versions (versioning)                    │
└─────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│         MACHINE LEARNING & AI LAYER                │
│                                                     │
│  • XGBoost Forecasting (86.35% accuracy)          │
│  • Isolation Forest Anomaly Detection              │
│  • Claude LLM Integration (AI Assistant)          │
│  • RAG System (Hybrid Search)                      │
│  • Model Registry (Versioning & Rollback)         │
└─────────────────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│         MONITORING & LOGGING LAYER                 │
│                                                     │
│  • Structured Logging                             │
│  • Health Checks                                  │
│  • Performance Metrics                            │
│  • Error Tracking                                 │
└─────────────────────────────────────────────────────┘
```

**2.2 Data Flow Example: "What is our revenue today?"**

```
1. User Types in Chat:
   "What is our revenue today?"

2. Frontend Sends Request:
   POST /api/v1/ai/chat
   { "message": "What is our revenue today?", "session_id": "xyz" }

3. Backend AI Agent Processes:
   ✓ Parse intent: Query for daily revenue
   ✓ Select tool: Use SQL query tool
   ✓ Execute: SELECT SUM(total_amount) FROM orders WHERE date = TODAY()
   ✓ Get result: 150,000 PKR

4. Backend AI Responds:
   "Your revenue today is 150,000 PKR, 
    which is 12% higher than yesterday."

5. Frontend Displays:
   ✓ Shows response in chat panel
   ✓ Updates KPI card
   ✓ Updates revenue chart

6. Logging:
   timestamp | user_id | query | latency | status
   -------- | ------- | ----- | ------- | ------
```

---

### Module 3: File Structure Explained (2 hours)

**3.1 Backend Structure**

```
app/
├── main.py
│   └── Entry point, route registration, startup/shutdown
│
├── api/routes/
│   ├── dashboard.py → KPI endpoints
│   ├── sales.py → Sales analytics endpoints
│   ├── products.py → Product endpoints
│   ├── ai.py → AI chat endpoints
│   ├── anomalies.py → Anomaly detection endpoints
│   ├── forecast.py → Forecasting endpoints
│   ├── models.py → Model management endpoints (Phase 11)
│   └── websocket.py → Real-time WebSocket endpoints
│
├── core/
│   ├── config.py → Configuration management
│   ├── security.py → Authentication & authorization
│   ├── database.py → Database connection
│   └── logging.py → Logging configuration
│
├── models/
│   ├── user.py → User database model
│   ├── order.py → Order database model
│   ├── sales.py → Sales database model
│   ├── anomaly.py → Anomaly database model
│   └── model_version.py → ML model version model
│
├── schemas/
│   ├── chat_schema.py → Chat request/response validation
│   ├── dashboard_schema.py → Dashboard data validation
│   └── ...
│
├── services/
│   ├── sales_service.py → Sales analytics logic
│   ├── chat_service.py → Chat processing logic
│   ├── notification_service.py → Real-time notifications
│   └── ...
│
├── agents/
│   ├── agent.py → Main AI agent
│   ├── planner.py → Agent planning logic
│   └── tools/
│       ├── sql_tool.py → Database query tool
│       ├── rag_tool.py → Knowledge retrieval
│       ├── forecast_tool.py → Forecasting tool
│       └── anomaly_tool.py → Anomaly detection
│
├── rag/
│   ├── loader.py → Document loading
│   ├── chunker.py → Text chunking
│   ├── embeddings.py → Vector embeddings
│   ├── retriever.py → Hybrid search
│   └── hybrid_search.py → Dense + BM25 search
│
├── ml/
│   ├── models.py → Database schema (Phase 11)
│   ├── registry.py → Model registry (Phase 11)
│   ├── loader.py → Model loading & caching (Phase 11)
│   ├── forecasting/ → Forecasting models
│   ├── anomaly_detection/ → Anomaly models
│   └── evaluation/ → Model evaluation
│
└── utils/
    ├── helpers.py → Utility functions
    ├── validators.py → Data validation
    └── converters.py → Data conversion
```

**3.2 Frontend Structure**

```
frontend/
├── src/
│   ├── components/
│   │   └── BBQDashboard.jsx (470 lines)
│   │       • State management
│   │       • KPI cards rendering
│   │       • Charts display
│   │       • Chat panel
│   │       • Sidebar navigation
│   │
│   ├── services/
│   │   └── api.js (200 lines)
│   │       • APIService class
│   │       • WebSocketService class
│   │       • HTTP requests
│   │       • Real-time connections
│   │
│   ├── App.jsx
│   │   └── Root component wrapper
│   │
│   ├── main.jsx
│   │   └── React DOM rendering
│   │
│   ├── App.css (280 lines)
│   │   └── Component-specific styles
│   │
│   └── index.css (130 lines)
│       └── Global styles & animations
│
├── public/
│   └── Static assets
│
├── vite.config.js
│   └── Build tool configuration
│
├── tailwind.config.js
│   └── Tailwind CSS customization
│
├── package.json
│   └── Dependencies & scripts
│
├── Dockerfile
│   └── Container configuration
│
└── README.md
    └── Frontend documentation
```

**3.3 Configuration Files**

```
Project Root:
├── docker-compose.yml → Multi-container orchestration
├── Dockerfile → Backend containerization
├── nginx.conf → Reverse proxy configuration
├── .env.example → Environment template
├── .env.production → Production configuration
├── requirements.txt → Python dependencies
├── pytest.ini → Test configuration
└── CLAUDE.md → Project instructions
```

---

### Module 4: Key Technologies Explained (3-4 hours)

**4.1 FastAPI**

```python
# What is FastAPI?
A modern, fast web framework for building APIs with Python

# Key Features:
• Automatic API documentation (/docs)
• Type hints for validation
• Async/await support
• WebSocket support
• Built-in security

# Simple Example:
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/v1/dashboard/kpis")
async def get_kpis():
    """Get dashboard KPIs"""
    return {
        "revenue": 150000,
        "orders": 245,
        "avg_order_value": 612
    }

# Access at: http://localhost:8000/api/v1/dashboard/kpis
# Docs at: http://localhost:8000/docs
```

**4.2 React**

```javascript
// What is React?
A JavaScript library for building user interfaces with components

// Key Concepts:
• Components: Reusable UI building blocks
• State: Component data that changes over time
• Props: Data passed from parent to child
• Hooks: useState, useEffect for logic

// Simple Example:
import React, { useState, useEffect } from 'react';

export function BBQDashboard() {
  const [revenue, setRevenue] = useState(0);
  
  useEffect(() => {
    // Fetch data when component mounts
    fetch('/api/v1/dashboard/kpis')
      .then(res => res.json())
      .then(data => setRevenue(data.revenue));
  }, []);
  
  return (
    <div>
      <h1>Revenue: {revenue} PKR</h1>
    </div>
  );
}
```

**4.3 SQLite**

```sql
-- What is SQLite?
A file-based SQL database, perfect for small to medium apps

-- View database
sqlite3 data/restaurant.db

-- Common commands:
SELECT * FROM orders;
SELECT COUNT(*) as total_orders FROM orders;
SELECT SUM(total_amount) as revenue FROM orders WHERE date = '2026-08-31';
CREATE INDEX idx_orders_date ON orders(date);
```

**4.4 Docker & Docker Compose**

```yaml
# What is Docker?
Containerization platform that packages apps with dependencies

# docker-compose.yml example:
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./data/restaurant.db
    volumes:
      - ./data:/app/data
    
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"

# Commands:
docker-compose up -d        # Start all services
docker-compose ps           # List running services
docker-compose logs api     # View API logs
docker-compose down         # Stop all services
```

**4.5 Recharts**

```javascript
// What is Recharts?
React charting library for beautiful, interactive charts

// Example:
import { LineChart, Line, XAxis, YAxis } from 'recharts';

const data = [
  { date: '2026-08-28', revenue: 145000 },
  { date: '2026-08-29', revenue: 158000 },
  { date: '2026-08-30', revenue: 150000 },
];

export function SalesChart() {
  return (
    <LineChart data={data} width={400} height={300}>
      <XAxis dataKey="date" />
      <YAxis />
      <Line type="monotone" dataKey="revenue" stroke="#ff6b35" />
    </LineChart>
  );
}
```

---

### Module 5: Running the Application (1-2 hours)

**5.1 Development Setup**

```bash
# Terminal 1: Backend
cd "E:\BBQ Restaurant AI Business Intelligence Agent\Projects\BBQ Restaurant AI Business Intelligence Agent"
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm install
npm run dev

# Terminal 3: Optional - Watch logs
docker-compose logs -f
```

**5.2 Accessing the Application**

```
Dashboard:      http://localhost:3000
API Docs:       http://localhost:8000/docs
Health Check:   http://localhost:8000/health
```

**5.3 Testing Key Features**

```bash
# Test 1: Fetch KPIs
curl http://localhost:8000/api/v1/dashboard/kpis

# Test 2: Get top products
curl http://localhost:8000/api/v1/products/top?limit=5

# Test 3: Chat with AI
curl -X POST http://localhost:8000/api/v1/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is our revenue today?"}'

# Test 4: Get anomalies
curl http://localhost:8000/api/v1/anomalies

# Test 5: Get model history
curl http://localhost:8000/api/v1/models/sales_forecast/history
```

---

## 🔧 Common Development Tasks

### Task 1: Add a New API Endpoint

**Step 1:** Create route in `app/api/routes/sales.py`
```python
from fastapi import APIRouter, Query
from app.schemas.dashboard_schema import SalesResponse

router = APIRouter(prefix="/api/v1/sales", tags=["sales"])

@router.get("/by-category")
async def get_sales_by_category(category: str = Query(...)):
    """Get sales breakdown by category"""
    service = SalesService()
    data = service.get_sales_by_category(category)
    return SalesResponse(data=data)
```

**Step 2:** Register route in `app/main.py`
```python
from app.api.routes import sales

app.include_router(sales.router)
```

**Step 3:** Test endpoint
```bash
curl http://localhost:8000/api/v1/sales/by-category?category=BBQ%20Platters
```

### Task 2: Create a New Frontend Component

**Step 1:** Create component file `frontend/src/components/SalesByCategory.jsx`
```javascript
import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis } from 'recharts';
import { APIService } from '../services/api';

export function SalesByCategory() {
  const [data, setData] = useState([]);
  
  useEffect(() => {
    APIService.get('/sales/by-category?category=BBQ')
      .then(res => setData(res.data))
      .catch(err => console.error(err));
  }, []);
  
  return (
    <div className="card">
      <h3>Sales by Category</h3>
      <BarChart data={data} width={400} height={300}>
        <XAxis dataKey="name" />
        <YAxis />
        <Bar dataKey="revenue" fill="#ff6b35" />
      </BarChart>
    </div>
  );
}
```

**Step 2:** Import in `BBQDashboard.jsx`
```javascript
import { SalesByCategory } from './SalesByCategory';

// Add to component
<SalesByCategory />
```

### Task 3: Add a Database Table

**Step 1:** Update schema in `app/models/`
```python
# app/models/promotion.py
from sqlalchemy import Column, Integer, String, DateTime

class Promotion(Base):
    __tablename__ = "promotions"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    discount_percent = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
```

**Step 2:** Create migration
```python
# Update database.py
from app.models.promotion import Promotion
Base.metadata.create_all(bind=engine)
```

**Step 3:** Create service
```python
# app/services/promotion_service.py
class PromotionService:
    def get_active_promotions(self):
        query = "SELECT * FROM promotions WHERE start_date <= NOW() AND end_date >= NOW()"
        return execute_query(query)
```

### Task 4: Add Unit Tests

**Step 1:** Create test file `tests/test_sales_service.py`
```python
import pytest
from app.services.sales_service import SalesService

@pytest.fixture
def sales_service():
    return SalesService()

def test_get_daily_revenue(sales_service):
    revenue = sales_service.get_daily_revenue('2026-08-31')
    assert revenue > 0
    assert isinstance(revenue, (int, float))

def test_get_top_products(sales_service):
    products = sales_service.get_top_products(limit=5)
    assert len(products) == 5
    assert 'product_name' in products[0]
    assert 'quantity' in products[0]
```

**Step 2:** Run tests
```bash
pytest tests/test_sales_service.py -v
```

---

## 🚀 Deployment Scenarios

### Scenario 1: Local Docker Deployment

```bash
# 1. Build images
docker-compose build

# 2. Start services
docker-compose up -d

# 3. Verify
docker-compose ps

# 4. Access
# Dashboard: http://localhost:3000
# API: http://localhost:8000/docs

# 5. View logs
docker-compose logs -f api
```

### Scenario 2: Production Deployment to Linux Server

```bash
# 1. SSH into server
ssh user@your-server.com

# 2. Clone repository
git clone <repo-url>
cd bbq-ai-bi-platform

# 3. Configure production environment
nano .env.production
# Set all required variables

# 4. Build images
docker-compose -f docker-compose.yml build

# 5. Start services
docker-compose -f docker-compose.yml up -d

# 6. Setup SSL (optional)
certbot certonly --standalone -d yourdomain.com

# 7. Verify deployment
curl https://yourdomain.com/health
```

### Scenario 3: Cloud Deployment (AWS, Azure, GCP)

**Option A: Heroku**
```bash
# 1. Install Heroku CLI
brew install heroku

# 2. Login
heroku login

# 3. Create app
heroku create bbq-ai-bi

# 4. Set environment variables
heroku config:set DATABASE_URL=your-db-url
heroku config:set LLM_API_KEY=your-key

# 5. Deploy
git push heroku main
```

**Option B: AWS (ECS)**
```bash
# 1. Build and push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin 123456.dkr.ecr.us-east-1.amazonaws.com
docker build -t bbq-api .
docker tag bbq-api:latest 123456.dkr.ecr.us-east-1.amazonaws.com/bbq-api:latest
docker push 123456.dkr.ecr.us-east-1.amazonaws.com/bbq-api:latest

# 2. Create ECS task definition
# 3. Create ECS service
# 4. Setup load balancer
```

---

## 🐛 Debugging Guide

### Debug Scenario 1: API Returns 500 Error

```bash
# 1. Check logs
docker-compose logs api | tail -50

# 2. Check database connection
curl http://localhost:8000/health

# 3. Check endpoint exists
curl http://localhost:8000/docs

# 4. Test endpoint with verbose output
curl -v http://localhost:8000/api/v1/dashboard/kpis

# 5. Add debug logging
# In app/main.py add:
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Debug Scenario 2: Frontend Not Loading Data

```bash
# 1. Open browser DevTools (F12)
# 2. Check Network tab - are API calls succeeding?
# 3. Check Console tab - are there JavaScript errors?
# 4. Check if API_URL is correct
# In frontend/.env.local:
VITE_API_URL=http://localhost:8000/api/v1

# 5. Restart frontend
npm run dev

# 6. Clear cache
# Ctrl+Shift+Delete (Windows/Linux)
# Cmd+Shift+Delete (Mac)
```

### Debug Scenario 3: Database Error

```bash
# 1. Check if database file exists
ls -la data/restaurant.db

# 2. Check permissions
chmod 666 data/restaurant.db

# 3. Backup and recreate
cp data/restaurant.db data/restaurant.db.backup
rm data/restaurant.db
docker-compose restart api

# 4. Verify database
sqlite3 data/restaurant.db "SELECT COUNT(*) FROM orders;"
```

---

## 📈 Performance Tuning

### Metric 1: Slow API Response

```python
# Add timing decorator
import time
from functools import wraps

def timer(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.2f}s")
        return result
    return wrapper

@app.get("/api/v1/dashboard/kpis")
@timer
async def get_kpis():
    # ...
```

### Metric 2: High Memory Usage

```bash
# Check memory
docker stats

# If too high, add limits
# In docker-compose.yml:
services:
  api:
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M
```

### Metric 3: Slow Database Queries

```sql
-- Enable query timing
.timer on

-- Analyze query plan
EXPLAIN QUERY PLAN SELECT * FROM orders WHERE date > '2026-08-01';

-- Add indexes
CREATE INDEX idx_orders_date ON orders(date);
```

---

## 🎯 Troubleshooting Quick Reference

| Problem | Cause | Solution |
|---------|-------|----------|
| Port 8000 in use | Another app on port | `lsof -i :8000` then `kill -9 <PID>` |
| Database locked | Concurrent access | Stop all containers, restart |
| 404 Not Found | Route doesn't exist | Check `app/api/routes/` and `app/main.py` |
| CORS error | Origin not allowed | Check `CORS_ORIGINS` in config |
| WebSocket fails | Proxy not configured | Check `nginx.conf` for WebSocket upgrade |
| Slow response | Missing index | Add database index on commonly queried column |
| Out of memory | Large query | Add LIMIT to queries or paginate results |
| SSL certificate error | Certificate expired | Renew with `certbot renew` |

---

## 📚 Further Reading

### Recommended Resources

1. **FastAPI Documentation**: https://fastapi.tiangolo.com/
2. **React Documentation**: https://react.dev/
3. **Docker Documentation**: https://docs.docker.com/
4. **SQLite Documentation**: https://www.sqlite.org/docs.html
5. **Recharts Documentation**: https://recharts.org/

### Project-Specific Docs

- `CLAUDE.md` - Project specifications
- `PHASE_12_DOCKER_DEPLOYMENT.md` - Deployment
- `FRONTEND_IMPLEMENTATION_COMPLETE.md` - Frontend
- `DEPLOYMENT_AND_NEXT_STEPS.md` - Operations

---

## ✅ Checklist for New Developers

- [ ] Read CLAUDE.md
- [ ] Read this Learning Manual
- [ ] Clone repository
- [ ] Install dependencies (backend + frontend)
- [ ] Run `docker-compose up -d`
- [ ] Access dashboard at http://localhost:3000
- [ ] Test API at http://localhost:8000/docs
- [ ] Run tests: `pytest tests/`
- [ ] Make first code change (add simple endpoint)
- [ ] Run linter: `npm run lint` (frontend)
- [ ] Create pull request with change
- [ ] Get code review
- [ ] Merge and deploy

---

## 🎉 You're Ready!

You now understand the complete BBQ Restaurant AI BI Platform. Start with:

1. **Understanding**: Read modules 1-2
2. **Exploring**: Run the application locally
3. **Building**: Try one of the common development tasks
4. **Deploying**: Follow deployment scenario

**Happy coding! 🚀**

---

*Complete Learning & Reference Manual*  
**Date:** 2026-08-31  
**For:** Beginners to Intermediate Developers  
**Level:** Comprehensive

