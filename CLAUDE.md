# BBQ Restaurant AI Business Intelligence Agent

## 1. Project Overview

**Project Name:** BBQ Restaurant AI Business Intelligence Agent

**Project Type:** Production-oriented AI/ML Business Intelligence Platform

**Primary Goal:**

Build an intelligent restaurant analytics platform that combines:

- Python
- FastAPI
- PostgreSQL
- RAG
- LLMs
- AI Agents
- Machine Learning
- Sales Forecasting
- Anomaly Detection
- WebSockets
- Real-time dashboards
- Model versioning
- Authentication
- Docker
- Monitoring

The system should allow restaurant management to understand business performance using natural-language questions while also providing traditional analytics, ML predictions, anomaly detection, and automated business insights.

---

# 2. Core Product Vision

The platform should answer:

> "Ask your BBQ restaurant data anything."

Example questions:

- What were our best-selling products last month?
- Which day generated the highest revenue?
- Why did sales decrease yesterday?
- What are the expected sales for next week?
- Which products are performing poorly?
- Which products should we promote?
- Are there any unusual sales patterns?
- Compare this month with the previous month.
- What are the top-performing branches?
- Which products generate the highest profit?
- What business problems should management investigate?

The AI should not simply generate text.

It should:

1. Understand the user's question.
2. Determine what information is required.
3. Select the appropriate tool.
4. Query structured restaurant data when necessary.
5. Retrieve unstructured business knowledge when necessary.
6. Run ML models when necessary.
7. Analyze the results.
8. Explain the result in natural language.
9. Clearly distinguish facts from predictions and recommendations.

---

# 3. High-Level Architecture

```text
                         ┌───────────────────────┐
                         │    Restaurant Users   │
                         │ Managers / Admins     │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │    Web Dashboard      │
                         │ Analytics + AI Chat    │
                         └───────────┬───────────┘
                                     │
                           REST / WebSocket
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │            FastAPI              │
                    │       Application Backend       │
                    └───────────────┬────────────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
      ┌──────────────┐      ┌───────────────┐     ┌───────────────┐
      │ AI Agent     │      │ RAG Engine    │     │ ML Engine     │
      │              │      │               │     │               │
      │ Reasoning    │      │ Hybrid Search │     │ Forecasting   │
      │ Planning     │      │ Embeddings    │     │ Anomaly       │
      │ Tool Calling │      │ Vector DB     │     │ Detection     │
      └──────┬───────┘      └──────┬────────┘     └──────┬────────┘
             │                     │                     │
             └─────────────────────┼─────────────────────┘
                                   │
                                   ▼
                         ┌───────────────────────┐
                         │      Data Layer       │
                         ├───────────────────────┤
                         │ PostgreSQL            │
                         │ Vector Database       │
                         │ Restaurant Documents  │
                         └───────────────────────┘

                                   │
                                   ▼
                         ┌───────────────────────┐
                         │ Monitoring / Metrics  │
                         │ Model Versions        │
                         │ Logs                  │
                         └───────────────────────┘

                                   │
                                   ▼
                         ┌───────────────────────┐
                         │ Docker / Deployment   │
                         └───────────────────────┘
```

---

# 4. Main System Components

## 4.1 Frontend

The dashboard should provide:

### Dashboard

Display:

- Total Revenue
- Total Orders
- Average Order Value
- Best-Selling Products
- Sales Trends
- Daily Sales
- Weekly Sales
- Monthly Sales
- Forecast
- Anomaly Alerts
- AI-generated insights

### AI Assistant

Natural-language interface:

```text
User:
Why did sales decrease this week?

AI:
Sales decreased by 14.7% compared with the previous
week. The primary contributors were:
1. BBQ Platter sales decreased 22%.
2. Weekend orders decreased 11%.
3. Average order value decreased 6%.

The largest decline occurred on Saturday.
```

### Real-Time Alerts

Display:

- Sales anomaly
- Revenue anomaly
- Order anomaly
- Product anomaly
- Forecast deviation

---

# 5. FastAPI Backend

FastAPI is the main backend/API layer.

Responsibilities:

- Authentication
- API routing
- Database access
- AI agent execution
- RAG requests
- ML predictions
- Forecasting
- Anomaly detection
- WebSocket connections
- Model management
- Monitoring
- Validation
- Error handling

Suggested API structure:

```text
/api/v1
```

Suggested endpoints:

```text
/auth
/users

/dashboard
/sales
/products
/orders

/ai/chat
/ai/agent

/rag/search
/rag/documents

/ml/predict
/ml/forecast
/ml/anomalies

/models
/models/versions
/models/activate

/metrics

/ws/dashboard
/ws/alerts
```

---

# 6. PostgreSQL Database

PostgreSQL is the primary structured data store.

Potential tables:

```text
users
roles

restaurants
branches

products
categories

customers

orders
order_items
payments

sales_daily
sales_monthly

inventory

business_rules

model_versions

predictions

anomalies

audit_logs
```

The schema should be normalized where appropriate while keeping analytical queries efficient.

---

# 7. Restaurant Data Model

Example:

```text
Restaurant
    |
    ├── Branch
    |
    ├── Products
    |
    ├── Customers
    |
    └── Orders
            |
            └── Order Items
                    |
                    ├── Product
                    ├── Quantity
                    ├── Unit Price
                    └── Discount
```

Example order:

```json
{
  "order_id": 10001,
  "date": "2026-08-20",
  "branch_id": 1,
  "customer_id": 550,
  "total_amount": 8500,
  "items": [
    {
      "product_id": 12,
      "quantity": 2,
      "unit_price": 2500
    },
    {
      "product_id": 18,
      "quantity": 1,
      "unit_price": 3500
    }
  ]
}
```

---

# 8. AI Agent Architecture

The AI Agent is the central reasoning component.

The agent should use tools instead of guessing.

```text
                    User Question
                          │
                          ▼
                    Intent Analysis
                          │
                          ▼
                    Agent Planner
                          │
            ┌─────────────┼─────────────┐
            │             │             │
            ▼             ▼             ▼
        SQL Tool       RAG Tool       ML Tool
            │             │             │
            ▼             ▼             ▼
       PostgreSQL     Vector DB      ML Models
            │             │             │
            └─────────────┼─────────────┘
                          ▼
                    Result Analysis
                          │
                          ▼
                    LLM Response
```

## Agent Tools

Potential tools:

```text
query_sales_database
query_products
query_orders
query_customers

search_business_knowledge

forecast_sales

detect_anomalies

compare_periods

get_top_products

get_revenue_metrics

get_model_status
```

### Important Rule

The agent must never invent numerical business results.

If the required data is unavailable, it must say so.

---

# 9. RAG Architecture

RAG is used for unstructured restaurant/business knowledge.

Potential documents:

```text
Restaurant policies
Menu documentation
Product descriptions
Pricing rules
Discount policies
Business procedures
Operational manuals
Management documentation
Marketing policies
Staff guidelines
```

Pipeline:

```text
Documents
    ↓
Document Loader
    ↓
Text Cleaning
    ↓
Chunking
    ↓
Metadata
    ↓
Embeddings
    ↓
Vector Database
```

Query pipeline:

```text
User Question
      ↓
Query Processing
      ↓
Hybrid Retrieval
      ├── Dense Vector Search
      └── BM25 Keyword Search
      ↓
Result Fusion / Ranking
      ↓
Relevant Context
      ↓
LLM
      ↓
Answer
```

RAG should include metadata such as:

```text
document_id
document_type
branch_id
category
source
created_at
updated_at
```

---

# 10. Hybrid Search

The project should support:

```text
Dense Search
+
BM25
=
Hybrid Search
```

Dense search is useful for semantic similarity.

BM25 is useful for exact terms, product names, codes, and keywords.

The system should combine both retrieval strategies and rank the results before sending context to the LLM.

---

# 11. Machine Learning Engine

The ML engine handles predictive analytics.

Main components:

```text
Sales Forecasting
Anomaly Detection
Demand Prediction
Product Performance Analysis
```

Potential algorithms:

### Forecasting

Depending on dataset size and characteristics:

- Baseline moving average
- Linear regression
- Random Forest
- Gradient boosting
- XGBoost
- Time-series models

Start simple and improve only when justified by data.

### Anomaly Detection

Initial approach:

```text
Isolation Forest
```

Possible future approach:

```text
Autoencoder
```

---

# 12. Sales Forecasting

Pipeline:

```text
Historical Sales
       ↓
Data Cleaning
       ↓
Feature Engineering
       ↓
Train / Validation Split
       ↓
Model Training
       ↓
Evaluation
       ↓
Model Versioning
       ↓
Forecast
       ↓
Dashboard
```

Potential features:

```text
date
day_of_week
month
week_of_year
holiday
promotion
branch
product
quantity
revenue
average_order_value
```

Metrics may include:

```text
MAE
RMSE
MAPE
R²
```

Do not select a model based only on training accuracy.

---

# 13. Anomaly Detection

The system should detect unusual behavior such as:

```text
Sudden revenue decrease
Sudden revenue increase
Unusual order volume
Product sales spike
Product sales collapse
Unexpected branch behavior
Forecast deviation
```

Example:

```text
Normal Revenue:
150,000 - 180,000

Actual Revenue:
72,000

Status:
🚨 Anomaly detected
```

Anomaly records should contain:

```text
anomaly_id
metric
value
expected_value
severity
timestamp
branch_id
description
model_version
```

---

# 14. Real-Time Architecture

FastAPI WebSockets should support real-time dashboard updates.

```text
Restaurant Data
      ↓
Data Processing
      ↓
ML / Analytics
      ↓
Anomaly Detection
      ↓
Event
      ↓
WebSocket
      ↓
Dashboard
```

Example:

```text
🚨 New anomaly detected

Revenue:
Expected: Rs. 165,000
Actual:   Rs. 92,000

Deviation: -44.2%
Severity: HIGH
```

---

# 15. Model Versioning

The system must support multiple ML model versions.

Example:

```text
models/
    sales_forecast/
        v1/
        v2/
        v3/

    anomaly_detector/
        v1/
        v2/
```

Model registry information:

```text
model_id
model_name
version
algorithm
metrics
training_date
dataset_version
status
created_by
```

Example:

```text
Sales Forecast Model

v1
MAE = 14,200

v2
MAE = 10,800

v3
MAE = 8,950

Active:
v3
```

---

# 16. Model Rollback

The API should allow administrators to change the active model.

Example:

```text
POST /models/activate
```

If v3 starts producing poor predictions:

```text
v3
 ↓
Problem detected
 ↓
Rollback
 ↓
v2 becomes active
```

The system should record this action in audit logs.

---

# 17. A/B Model Testing

Future capability:

```text
Traffic
   │
   ├── 90% → Model v3
   │
   └── 10% → Model v4
```

Compare:

```text
Accuracy
Latency
Error
Business performance
```

Then promote the better model.

---

# 18. Authentication and Authorization

The platform should support role-based access.

Suggested roles:

```text
Admin
Manager
Analyst
Viewer
```

Example permissions:

```text
Admin
 ├── Manage users
 ├── Manage models
 ├── Manage documents
 └── System configuration

Manager
 ├── View dashboard
 ├── Ask AI
 ├── View forecasts
 └── View anomalies

Analyst
 ├── View analytics
 ├── Run analysis
 └── View ML results

Viewer
 └── Read-only dashboard
```

---

# 19. Monitoring

The production system should monitor:

```text
API latency
API errors
Database performance
LLM latency
LLM token usage
RAG retrieval quality
ML prediction latency
Model accuracy
Anomaly volume
WebSocket connections
CPU
RAM
Docker health
```

FastAPI should expose:

```text
/metrics
/health
```

Example health response:

```json
{
  "status": "healthy",
  "database": "connected",
  "ai_service": "available",
  "ml_service": "available"
}
```

---

# 20. Logging

Use structured logging.

Log:

```text
timestamp
request_id
user_id
endpoint
latency
status
error
model_version
agent_tool
```

Never log:

```text
API keys
passwords
private credentials
sensitive user information
```

---

# 21. Docker Architecture

The production environment should be containerized.

Potential services:

```text
docker-compose.yml

services:

  api:
    FastAPI

  frontend:
    Dashboard

  postgres:
    PostgreSQL

  vector_db:
    Vector database

  worker:
    Background ML/data processing

  redis:
    Optional caching / queue

  nginx:
    Reverse proxy
```

Architecture:

```text
Internet
   ↓
Nginx
   ↓
Frontend
   ↓
FastAPI
   ├── PostgreSQL
   ├── Vector DB
   ├── Redis
   ├── ML Engine
   └── LLM Provider
```

---

# 22. Suggested Project Structure

```text
bbq-ai-business-intelligence/
│
├── CLAUDE.md
├── README.md
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── dashboard.py
│   │   │   ├── sales.py
│   │   │   ├── products.py
│   │   │   ├── orders.py
│   │   │   ├── ai.py
│   │   │   ├── rag.py
│   │   │   ├── ml.py
│   │   │   ├── models.py
│   │   │   └── metrics.py
│   │   │
│   │   └── websocket.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── logging.py
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── restaurant.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── sales.py
│   │   ├── anomaly.py
│   │   └── model_version.py
│   │
│   ├── schemas/
│   │
│   ├── services/
│   │   ├── sales_service.py
│   │   ├── product_service.py
│   │   ├── analytics_service.py
│   │   └── notification_service.py
│   │
│   ├── agents/
│   │   ├── agent.py
│   │   ├── planner.py
│   │   └── tools/
│   │       ├── sql_tool.py
│   │       ├── rag_tool.py
│   │       ├── forecast_tool.py
│   │       └── anomaly_tool.py
│   │
│   ├── rag/
│   │   ├── loader.py
│   │   ├── chunker.py
│   │   ├── embeddings.py
│   │   ├── retriever.py
│   │   └── hybrid_search.py
│   │
│   ├── ml/
│   │   ├── forecasting/
│   │   ├── anomaly_detection/
│   │   ├── training/
│   │   ├── evaluation/
│   │   └── registry/
│   │
│   └── utils/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
│
├── documents/
│   ├── menu/
│   ├── policies/
│   └── business/
│
├── models/
│
├── notebooks/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── frontend/
│
└── scripts/
    ├── seed_database.py
    ├── ingest_documents.py
    └── train_models.py
```

---

# 23. Data Pipeline

```text
Restaurant CSV / Existing Data
              ↓
        Data Validation
              ↓
        Data Cleaning
              ↓
      Feature Engineering
              ↓
          PostgreSQL
              ↓
       ┌──────┴───────┐
       ↓              ↓
   Analytics          ML
       ↓              ↓
   Dashboard       Predictions
```

The original BBQ restaurant dataset should be treated as the initial development dataset.

The architecture should remain flexible enough to support future real restaurant data.

---

# 24. AI Response Rules

The AI assistant must follow these principles:

### Rule 1 — Never hallucinate numbers

If the database says:

```text
Revenue = Rs. 850,000
```

the AI must not report:

```text
Revenue = Rs. 900,000
```

### Rule 2 — Explain data sources

For analytical answers, indicate whether the answer came from:

```text
Database
RAG
ML model
Combination
```

### Rule 3 — Separate facts from predictions

Example:

```text
Historical fact:
Revenue was Rs. 850,000 last month.

Prediction:
Next month's estimated revenue is Rs. 910,000.

Recommendation:
Consider promoting the top three products.
```

### Rule 4 — Ask for clarification when required

If the user says:

> "Show sales."

The system should clarify:

```text
Which period would you like?

Today
This week
This month
Custom period
```

---

# 25. Agent Safety

The AI agent must not:

- Delete production data without explicit authorization.
- Modify financial records without authorization.
- Expose credentials.
- Invent database results.
- Execute arbitrary SQL.
- Execute arbitrary shell commands.
- Modify ML models without proper permissions.
- Bypass authentication.
- Expose confidential restaurant information.

SQL tools should preferably use controlled queries or read-only database access for analytics.

---

# 26. Performance Principles

Prioritize:

```text
Correctness
Security
Reliability
Observability
Maintainability
Performance
```

Avoid premature optimization.

Use caching where appropriate.

Potential caching targets:

```text
Dashboard metrics
Frequently asked AI questions
RAG retrieval results
Expensive analytics
```

---

# 27. Testing Strategy

Tests should cover:

### Unit Tests

```text
Data processing
Feature engineering
ML functions
RAG functions
Agent tools
Database functions
```

### Integration Tests

```text
FastAPI + PostgreSQL
FastAPI + RAG
FastAPI + ML
Agent + Tools
WebSocket
```

### End-to-End Tests

Example:

```text
User
 ↓
Dashboard
 ↓
AI Question
 ↓
Agent
 ↓
SQL Tool
 ↓
PostgreSQL
 ↓
Result
 ↓
LLM
 ↓
Dashboard
```

---

# 28. Development Roadmap

## Phase 1 — Dataset

- Understand BBQ restaurant dataset.
- Clean data.
- Explore columns.
- Perform EDA.
- Define business metrics.

## Phase 2 — PostgreSQL

- Design schema.
- Create tables.
- Import dataset.
- Create indexes.
- Build analytical queries.

## Phase 3 — FastAPI

- Create application.
- Database connection.
- CRUD APIs.
- Analytics APIs.
- Authentication.

## Phase 4 — Dashboard

Build:

- KPI cards
- Sales charts
- Product analytics
- Revenue trends
- Filters

## Phase 5 — RAG

Implement:

- Document ingestion
- Chunking
- Embeddings
- Vector storage
- Hybrid retrieval
- Context generation

## Phase 6 — AI Agent

Implement:

- Agent
- Planning
- Tool calling
- SQL tool
- RAG tool
- Analytics tools

## Phase 7 — ML

Implement:

- Sales forecasting
- Evaluation
- Model registry
- Prediction API

## Phase 8 — Anomaly Detection

Implement:

- Isolation Forest
- Thresholds
- Anomaly storage
- Alert system

## Phase 9 — Real-Time

Implement:

- WebSockets
- Real-time dashboard
- Real-time anomaly alerts

## Phase 10 — Production

Implement:

- Docker
- Logging
- Monitoring
- Authentication
- Security
- Testing
- Deployment

---

# 29. MVP Definition

The first working MVP should NOT implement everything.

MVP:

```text
BBQ Dataset
     ↓
PostgreSQL
     ↓
FastAPI
     ↓
Dashboard
     ↓
AI Assistant
     ↓
SQL Tool
     ↓
LLM
```

The first AI questions should be:

```text
What is total revenue?

What are the top 10 products?

What is the average order value?

Which day has the highest sales?

Compare this month with last month.
```

After this works reliably, add RAG, forecasting, anomaly detection, WebSockets, and model versioning.

---

# 30. Definition of Done

The project is considered production-ready when:

- [ ] PostgreSQL database is properly designed.
- [ ] Restaurant data is validated.
- [ ] FastAPI APIs are documented.
- [ ] Authentication works.
- [ ] Dashboard works.
- [ ] AI agent can use tools.
- [ ] AI answers are grounded in database results.
- [ ] RAG works with restaurant documents.
- [ ] Hybrid search works.
- [ ] Sales forecasting works.
- [ ] Forecast model is evaluated.
- [ ] Anomaly detection works.
- [ ] Real-time alerts work.
- [ ] Model versions are tracked.
- [ ] Model rollback works.
- [ ] Logging is implemented.
- [ ] Monitoring is implemented.
- [ ] Tests are implemented.
- [ ] Docker deployment works.
- [ ] Secrets are managed through environment variables.
- [ ] Production database access is secured.
- [ ] README contains setup instructions.

---

# 31. Development Principles for Claude Code

When working on this repository:

1. **Understand the existing code before modifying it.**
2. Do not rewrite working components unnecessarily.
3. Make small, incremental changes.
4. Preserve existing functionality.
5. Follow the project architecture defined in this document.
6. Use type hints in Python.
7. Use Pydantic schemas for FastAPI validation.
8. Keep business logic out of route handlers where possible.
9. Keep database access separated from AI logic.
10. Keep AI agent tools modular.
11. Write tests for important functionality.
12. Never hard-code API keys.
13. Use `.env` for secrets.
14. Never commit `.env`.
15. Use meaningful error messages.
16. Add logging for important operations.
17. Prefer readable code over clever code.
18. Do not add dependencies unless necessary.
19. Explain architectural changes before implementing major changes.
20. If requirements are ambiguous, ask before making destructive architectural decisions.

---

# 32. Environment Variables

Use `.env.example`.

Example:

```env
APP_ENV=development

DATABASE_URL=

LLM_API_KEY=

EMBEDDING_API_KEY=

VECTOR_DATABASE_URL=

REDIS_URL=

SECRET_KEY=

JWT_SECRET_KEY=
```

Never place real credentials in source code.

---

# 33. Git Strategy

Recommended branches:

```text
main
develop

feature/fastapi
feature/rag
feature/agent
feature/ml
feature/dashboard
feature/anomaly-detection
feature/websocket
```

Commit examples:

```text
feat: add restaurant sales API

feat: implement hybrid RAG retrieval

feat: add sales forecasting model

feat: add anomaly detection

fix: correct revenue aggregation

test: add sales analytics tests
```

---

# 34. Important Architectural Principle

This project is **not simply an LLM chatbot**.

The architecture should be:

```text
             AI Business Intelligence
                       │
       ┌───────────────┼────────────────┐
       │               │                │
      Data            RAG              ML
       │               │                │
 PostgreSQL       Knowledge Base    Predictions
       │               │                │
       └───────────────┼────────────────┘
                       │
                    AI Agent
                       │
                    FastAPI
                       │
                   Dashboard
```

The LLM is one component of the system.

The **data, tools, retrieval, ML models, APIs, security, monitoring, and business logic are equally important.**

---

# 35. Long-Term Vision

Future versions may include:

```text
Multi-branch restaurant support
Multi-tenant architecture
Inventory prediction
Customer segmentation
Recommendation engine
Marketing optimization
Dynamic pricing recommendations
Staff scheduling prediction
Food waste prediction
Profit optimization
Voice AI assistant
WhatsApp integration
Mobile application
Automated management reports
Email reports
AI-generated executive summaries
Agent-to-agent workflows
```

Potential future architecture:

```text
                    AI Restaurant Platform
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   Data Agent          Analytics Agent      Operations Agent
        │                   │                   │
        ├──────────────┬────┴────┬──────────────┤
        │              │         │              │
     RAG Agent      ML Agent  Forecast Agent  Alert Agent
        │              │         │              │
        └──────────────┴─────────┴──────────────┘
                            │
                       AI Orchestrator
                            │
                         FastAPI
                            │
                    Restaurant Platform
```

---

# 36. Final Project Objective

The final system should demonstrate that an AI Engineer can build a complete production-oriented AI application rather than only calling an LLM API.

The project should demonstrate expertise in:

```text
Python
FastAPI
REST APIs
PostgreSQL
Data Engineering
Machine Learning
Forecasting
Anomaly Detection
RAG
Hybrid Search
LLMs
AI Agents
Tool Calling
WebSockets
Authentication
Model Versioning
Monitoring
Docker
Production Architecture
```

The BBQ restaurant dataset is the initial business domain and development environment.

The architecture should remain modular so that the same platform can later be adapted to other businesses such as:

```text
Retail
E-commerce
Hotels
Restaurants
Education
Healthcare
Finance
Manufacturing
```

**Core philosophy:**

> Build an AI-powered business intelligence system where the AI reasons over real business data, uses tools to obtain evidence, applies ML when prediction is required, retrieves organizational knowledge through RAG, and presents actionable insights through a production-ready API and dashboard.
