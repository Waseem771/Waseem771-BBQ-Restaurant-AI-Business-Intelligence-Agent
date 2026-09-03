# BBQ Restaurant AI Business Intelligence Agent — Complete Project Plan

**Owner:** Waseem Hassan
**Type:** Production-grade AI BI system (not a prototype)
**Approach:** Sequential build — each phase fully understood and completed before the next begins

---

## Phase 0 — Foundation *(Done)*

| | |
|---|---|
| **Goal** | Define scope, architecture, and success criteria before writing code |
| **Output** | `CLAUDE.md` living spec |
| **Status** | ✅ Complete |

---

## Phase 1 — Dataset Creation *(Done)*

| | |
|---|---|
| **Goal** | Realistic synthetic BBQ restaurant data to build and test everything against |
| **Deliverables** | `branches.csv` (3), `products.csv` (14 items/4 categories), `customers.csv` (600), `orders.csv` (~19,600), `order_items.csv` (~40,000) |
| **Realism baked in** | Weekend spikes, ~1.5% monthly growth, 4 injected anomalies (Mar 23 & Jul 14 spikes, May 5 & Aug 18 drops) |
| **Status** | ✅ Complete — integrity verified (no nulls/orphans/negative totals) |

---

## Phase 2 — Exploratory Data Analysis *(Next)*

| | |
|---|---|
| **Goal** | Verify the data behaves as designed; build intuition before it goes into a database |
| **What we'll build** | A single well-commented Python analysis script (reusable later) |
| **Covers** | Join integrity checks, revenue trends (daily/weekly/monthly), anomaly-date verification, product/category performance, branch comparison, basic customer behavior (repeat vs one-time, order frequency) |
| **Tools** | pandas, numpy, matplotlib/seaborn |
| **Exit criteria** | You can explain, in your own words, what the data shows and why — and we've confirmed the injected anomalies and seasonality are visible |

---

## Phase 3 — PostgreSQL Schema Design & Data Loading

| | |
|---|---|
| **Goal** | Move from flat CSVs to a normalized, production-style relational database |
| **What we'll build** | ERD, normalized schema (branches, products, customers, orders, order_items with proper FKs/constraints/indexes), a Python loader script, basic seed/migration setup |
| **Key decisions** | Primary/foreign keys, indexing strategy for the queries the AI agent will later generate, handling of computed columns (totals, margins) |
| **Tools** | PostgreSQL, SQLAlchemy or raw psycopg2, Alembic (migrations) |
| **Exit criteria** | Data loads cleanly, referential integrity enforced by the DB itself (not just by your generator script), you can write and explain basic joins |

---

## Phase 4 — FastAPI Backend

| | |
|---|---|
| **Goal** | Expose the database through a clean, documented REST API |
| **What we'll build** | Project structure (routers, models, schemas, services), CRUD + analytics endpoints (revenue by branch/date, top products, customer stats), Pydantic validation, error handling, auto-generated OpenAPI docs |
| **Key decisions** | Layered architecture (routes → services → repository/DB layer) so later phases (AI agent, dashboard) plug in cleanly |
| **Tools** | FastAPI, Pydantic, SQLAlchemy, Uvicorn |
| **Exit criteria** | You can hit endpoints via `/docs` and get correct, validated JSON back |

---

## Phase 5 — Dashboard (Frontend/Visualization Layer)

| | |
|---|---|
| **Goal** | A real-time-capable visual layer for the business data |
| **What we'll build** | Charts/KPIs for revenue, branch comparison, product performance, anomaly flags — wired to the FastAPI endpoints |
| **Tools** | Streamlit (fastest path given your existing skillset) or a lightweight React frontend if you want the practice — we'll decide together when we get there |
| **Exit criteria** | Non-technical stakeholder could open the dashboard and understand restaurant performance at a glance |

---

## Phase 6 — SQL-Powered AI Assistant (MVP Milestone) 🎯

| | |
|---|---|
| **Goal** | Natural language → SQL → grounded answer. This is your first real "AI BI agent" milestone |
| **What we'll build** | An agent that takes a question like *"Which branch had the highest revenue in July?"*, generates safe parameterized SQL against your schema, executes it, and returns a grounded natural-language answer |
| **Key decisions** | Schema-aware prompting, SQL validation/sandboxing (never execute unsafe/unvalidated SQL), query result → NL response formatting |
| **Tools** | Anthropic API (or your LLM of choice), a SQL-generation agent pattern, guardrails around execution |
| **Exit criteria** | You can ask real business questions in plain English and get correct, DB-grounded answers |

---

## Phase 7 — RAG (Retrieval-Augmented Generation)

| | |
|---|---|
| **Goal** | Let the agent answer questions that aren't purely structured-data lookups (e.g., menu descriptions, policies, unstructured notes) |
| **What we'll build** | Hybrid dense + BM25 retrieval pipeline, embedding pipeline, vector store, a retrieval tool the agent can call alongside SQL |
| **Tools** | Sentence-Transformers / embeddings API, FAISS (or pgvector, worth discussing given you're already on Postgres), BM25 (rank_bm25 or similar) |
| **Exit criteria** | The agent correctly chooses between "query the database" vs "retrieve from knowledge base" depending on the question, and blends both when needed |

---

## Phase 8 — Sales Forecasting

| | |
|---|---|
| **Goal** | Predictive capability — not just "what happened" but "what's likely next" |
| **What we'll build** | Time-series forecasting model(s) for revenue/order volume, evaluation against holdout data, a forecast tool the agent can call |
| **Tools** | Prophet, statsmodels, or a gradient-boosted approach (XGBoost/LightGBM) with engineered time features — we'll pick based on the EDA results from Phase 2 |
| **Exit criteria** | You can ask "what's projected revenue for next month?" and get a defensible, backtested forecast |

---

## Phase 9 — Anomaly Detection

| | |
|---|---|
| **Goal** | Automatically flag unusual patterns — this is exactly what your 4 injected anomalies in Phase 1 were designed to validate |
| **What we'll build** | Statistical or ML-based anomaly detection (e.g., seasonal decomposition + residual thresholds, or isolation forest), an anomaly-explanation tool for the agent |
| **Tools** | statsmodels (STL decomposition), scikit-learn (IsolationForest) |
| **Exit criteria** | The system correctly flags all 4 injected anomaly dates without excessive false positives |

---

## Phase 10 — WebSockets & Real-Time Layer

| | |
|---|---|
| **Goal** | Push live updates to the dashboard instead of polling |
| **What we'll build** | WebSocket endpoints in FastAPI, live-updating dashboard components, event-driven updates on new orders |
| **Tools** | FastAPI WebSockets, async patterns |
| **Exit criteria** | Dashboard reflects new data without a manual refresh |

---

## Phase 11 — Model Versioning & Rollback

| | |
|---|---|
| **Goal** | Production ML hygiene — never deploy a model you can't roll back |
| **What we'll build** | Model registry pattern, versioned artifacts, rollback mechanism, basic performance tracking across versions |
| **Tools** | MLflow (or a lightweight custom registry if you want full control/learning value) |
| **Exit criteria** | You can deploy a new forecasting/anomaly model and roll it back safely if it underperforms |

---

## Phase 12 — Production Deployment

| | |
|---|---|
| **Goal** | Ship it like a real product |
| **What we'll build** | Dockerized services (API, DB, dashboard), docker-compose for local orchestration, authentication on the API, monitoring/logging, environment-based config, basic CI |
| **Tools** | Docker, Docker Compose, JWT/OAuth for auth, structured logging, (optionally) a monitoring stack |
| **Exit criteria** | The whole system runs from `docker-compose up`, is authenticated, and is observable |

---

## How We'll Work Through Each Phase

1. I explain the concept (beginner → advanced) before we write code
2. We design the approach together and I flag trade-offs
3. I deliver complete, runnable artifacts (scripts/files), not fragments
4. We verify it works against your actual data before moving on
5. We update `CLAUDE.md` to reflect what's been built

## Current Position

📍 **You are here:** Phase 2 (EDA) — waiting on your CSV uploads to begin.

---

*This plan is a living document — phases may be reordered or adjusted (e.g., pgvector vs FAISS, Streamlit vs React) as we learn more from earlier phases, but the sequence reflects your original roadmap.*
