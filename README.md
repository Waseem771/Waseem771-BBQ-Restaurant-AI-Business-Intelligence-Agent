# 🍖 BBQ Restaurant AI Business Intelligence Agent

AI-powered Business Intelligence dashboard for BBQ restaurant chain management. Features real-time analytics, anomaly detection, sales forecasting, and an AI chat assistant — all backed by a FastAPI REST API and a React frontend.

---

## 📋 Prerequisites

- **Python 3.10+** — [Download](https://www.python.org/downloads/)
- **Node.js 16+** and **npm 8+** — [Download](https://nodejs.org/)
- **Git** — [Download](https://git-scm.com/)

---

## 🚀 How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/Waseem771/Waseem771-BBQ-Restaurant-AI-Business-Intelligence-Agent.git
cd "BBQ Restaurant AI Business Intelligence Agent/Projects/BBQ Restaurant AI Business Intelligence Agent"
```

### 2. Set Up Environment Variables

Copy the example env file and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` and set your keys:

```env
# Required for AI chat (get free key at https://console.groq.com)
GROQ_API_KEY=your_groq_api_key_here

# Optional fallback (https://console.anthropic.com)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Database (defaults work out of the box)
BBQ_DATA_DIR=./data
BBQ_DB_PATH=./data/bbq.db
```

> **Note:** The dashboard and analytics work without API keys. Only the AI Chat feature requires a valid `GROQ_API_KEY` or `ANTHROPIC_API_KEY`.

### 3. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
pip install fastapi uvicorn python-dotenv pydantic pandas scikit-learn numpy websockets groq
cd ..
```

### 4. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### 5. Start Both Servers

Open **two separate terminals** from the project root:

**Terminal 1 — Backend (FastAPI on port 8000):**

```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

**Terminal 2 — Frontend (React/Vite on port 3000):**

```bash
cd frontend
npm run dev
```

### 6. Open the Dashboard

- 🖥️ **Dashboard:** [http://localhost:3000](http://localhost:3000)
- 📖 **API Docs (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
- ❤️ **Health Check:** [http://localhost:8000/health](http://localhost:8000/health)

> **Login:** Use the **Demo Access** button on the login page to get started immediately.

---

## ⚡ Quick Start (Windows — One Command)

From the project root, run the batch file:

```bash
start-servers.bat
```

This opens two terminal windows (backend + frontend) and opens the dashboard in your browser.

---

## 🏗️ Project Structure

```
├── backend/                   # FastAPI backend
│   ├── app/
│   │   ├── main.py            # FastAPI entry point
│   │   ├── config.py          # Configuration & path resolution
│   │   ├── analytics.py       # Sales analytics & KPI calculations
│   │   ├── ai_assistant.py    # AI-powered Q&A (Groq/Anthropic)
│   │   ├── anomaly_detection.py  # Isolation Forest anomaly detection
│   │   ├── forecast_tool.py   # Revenue & order forecasting
│   │   ├── db.py              # SQLite read-only access layer
│   │   ├── api/routes/        # REST API route handlers
│   │   ├── agents/            # AI agent tools
│   │   └── websocket/         # Real-time WebSocket alerts
│   └── requirements.txt
│
├── frontend/                  # React + Vite frontend
│   ├── src/
│   │   ├── App.jsx            # Root component
│   │   ├── components/
│   │   │   ├── Dashboard.jsx  # Main analytics dashboard
│   │   │   └── LoginPage.jsx  # Authentication UI
│   │   ├── services/api.js    # API client
│   │   └── styles/            # CSS files
│   └── package.json
│
├── data/
│   └── bbq.db                 # SQLite database (pre-built)
│
├── .env                       # Environment variables (not in git)
├── .env.example               # Template for .env
├── start-servers.bat          # Windows quick-start script
└── docker-compose.yml         # Docker deployment
```

---

## 🔌 API Endpoints

| Method | Endpoint                        | Description               |
|--------|---------------------------------|---------------------------|
| GET    | `/health`                       | System health check       |
| GET    | `/api/v1/dashboard/kpis`        | Key Performance Indicators|
| GET    | `/api/v1/sales/monthly`         | Monthly revenue breakdown |
| GET    | `/api/v1/sales/daily`           | Daily revenue data        |
| GET    | `/api/v1/sales/by-branch`       | Revenue per branch        |
| GET    | `/api/v1/sales/best-day`        | Best sales day            |
| GET    | `/api/v1/sales/weekend-vs-weekday` | Weekend vs weekday stats |
| GET    | `/api/v1/sales/month-compare`   | Month-over-month change   |
| GET    | `/api/v1/products/top?limit=10` | Top products by revenue   |
| GET    | `/api/v1/products/categories`   | Category breakdown        |
| GET    | `/api/v1/anomalies?threshold=0.6` | Anomaly detection       |
| POST   | `/api/v1/ai/chat`               | AI assistant Q&A          |

Full interactive docs at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 🧠 AI Features

- **Natural Language Q&A** — Ask questions like *"Which branch performs best?"* or *"What are the top 3 products?"*
- **SQL Generation** — AI translates questions into SQL and returns grounded answers
- **Anomaly Detection** — Isolation Forest detects unusual revenue spikes/drops
- **Sales Forecasting** — Linear trend model with confidence intervals
- **Real-time Alerts** — WebSocket-based anomaly broadcasting

---

## 🐳 Docker Deployment

```bash
docker-compose up --build
```

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| Dashboard shows no data | Make sure the backend is running on port 8000 |
| `sqlite3.OperationalError: unable to open database file` | Check that `data/bbq.db` exists at the project root |
| AI chat says "Could not reach backend" | Verify backend is running: `curl http://localhost:8000/health` |
| Frontend won't start | Run `npm install` in the `frontend/` directory |
| Port already in use | Kill existing processes: `netstat -ano \| findstr :8000` |

---

## 📄 License

MIT
