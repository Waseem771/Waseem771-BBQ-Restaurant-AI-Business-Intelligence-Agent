# 🎯 BBQ Restaurant AI - Run Locally NOW

## ✅ Status: Ready to Run

Your project is fully set up and ready to go. Here's exactly what to do:

---

## 🚀 **Start in 60 Seconds**

### **Open Terminal 1 (Backend)**

```powershell
cd "E:\BBQ Restaurant AI Business Intelligence Agent\Projects\BBQ Restaurant AI Business Intelligence Agent"
python -m uvicorn app.main:app --reload --port 8000
```

**Wait for this message:**
```
INFO:     Application startup complete
INFO:     Uvicorn running on http://127.0.0.1:8000
```

✅ **Backend is ready** → http://localhost:8000

---

### **Open Terminal 2 (Frontend)**

```powershell
cd "E:\BBQ Restaurant AI Business Intelligence Agent\Projects\BBQ Restaurant AI Business Intelligence Agent\frontend"
npm run dev
```

**Wait for this message:**
```
VITE v5.x.x  ready in XXX ms

➜  Local:   http://localhost:3000/
```

✅ **Frontend is ready** → http://localhost:3000

---

### **Open Your Browser**

Visit: **http://localhost:3000**

You'll see:
- 📊 Sales Dashboard with KPIs
- 📈 Revenue and order charts
- 🤖 AI Assistant chat
- ⚙️ Settings panel
- 🔔 Alerts and anomalies

---

## 🔗 **All URLs**

```
Dashboard:        http://localhost:3000
API Docs:         http://localhost:8000/docs
ReDoc Docs:       http://localhost:8000/redoc
Backend Health:   http://localhost:8000/health
```

---

## 📋 **What's Running**

### **Backend (FastAPI)**
- ✅ Python 3.13
- ✅ FastAPI 0.115
- ✅ Uvicorn server
- ✅ PostgreSQL/SQLite database
- ✅ AI Agent with tools
- ✅ Analytics engine
- ✅ WebSocket support

**Files:** `app/main.py`, `app/analytics.py`, `app/ai_assistant.py`, `app/api/`

### **Frontend (React)**
- ✅ React 18.2
- ✅ Vite 5.0
- ✅ Recharts for charts
- ✅ Tailwind CSS
- ✅ Lucide React icons
- ✅ Settings panel
- ✅ Real-time WebSocket

**Files:** `frontend/src/App.jsx`, `frontend/src/components/BBQDashboard.jsx`

---

## 🧪 **Quick Verification**

Before starting, verify dependencies:

```powershell
# Check Node.js
node --version    # Should be v16+ (you have v24.16.0 ✅)

# Check npm
npm --version     # Should be v8+ (you have v11.16.0 ✅)

# Check Python
python --version  # Should be 3.10+ (you have 3.13.11 ✅)

# All ready? ✅ Start the servers!
```

---

## 🎮 **Dashboard Features**

Once running, you can:

1. **View Metrics**
   - Total Revenue
   - Total Orders
   - Average Order Value
   - Top Products

2. **Explore Charts**
   - Sales Trends (line chart)
   - Product Performance (bar chart)
   - Category Breakdown (pie chart)
   - Order Volume (area chart)

3. **Use AI Assistant**
   - Ask questions: "What are top products?"
   - Get insights: "Which day had highest sales?"
   - Get predictions: "What's the forecast?"

4. **Check Alerts**
   - Anomalies detected
   - Revenue dips
   - Unusual patterns

5. **Configure Settings**
   - Change theme (dark/light)
   - Adjust colors
   - Configure alerts
   - Set preferences

---

## ⚡ **Hot Reload (Live Editing)**

### **Frontend Changes**
Edit any file in `frontend/src/` → Browser auto-updates (no refresh needed)

```javascript
// Edit this and see changes instantly:
frontend/src/components/BBQDashboard.jsx
```

### **Backend Changes**
Edit Python files → Server auto-reloads (with `--reload` flag)

```python
# Edit this and server restarts automatically:
app/main.py
app/analytics.py
app/ai_assistant.py
```

---

## 🛑 **Stop Servers**

In each terminal:
```powershell
Ctrl + C
```

---

## 🔄 **Restart Process**

If something breaks:

1. Stop both servers (Ctrl+C)
2. Close both terminals
3. Follow "Start in 60 Seconds" above again

---

## 🆘 **Common Issues**

### **"Port 3000 already in use"**
✅ Vite will try 3001, 3002, etc. Check terminal for actual port.

### **"Cannot connect to backend"**
✅ Make sure backend terminal shows "Application startup complete"

### **"Blank page"**
✅ Press Ctrl+Shift+R (hard refresh) in browser

### **"npm command not found"**
✅ Restart terminal after installing Node.js

---

## 📚 **Project Structure**

```
project/
├── app/                          # Backend (FastAPI)
│   ├── main.py                  # Entry point ⭐
│   ├── analytics.py             # Analytics logic
│   ├── ai_assistant.py          # AI agent
│   ├── anomaly_detection.py     # Anomaly detection
│   ├── forecasting.py           # Sales forecasting
│   ├── api/                     # API routes
│   └── db.py                    # Database
│
├── frontend/                     # Frontend (React)
│   ├── src/
│   │   ├── App.jsx              # Main app ⭐
│   │   ├── components/
│   │   │   └── BBQDashboard.jsx # Dashboard component ⭐
│   │   ├── services/            # API calls
│   │   └── context/             # Settings context
│   ├── package.json             # Dependencies
│   ├── vite.config.js           # Vite config
│   └── index.html               # HTML entry
│
├── data/                         # Sample data
├── documents/                    # Business knowledge
├── requirements.txt             # Python packages
└── setup-local-dev.ps1         # Setup script

⭐ = Key files to check
```

---

## 💾 **Data & Models**

The project uses:
- **Database:** SQLite (or PostgreSQL)
- **Sample Data:** BBQ restaurant sales data
- **ML Models:** Forecasting, anomaly detection
- **Documents:** Business knowledge for RAG

All data is loaded on startup from `data/` and `documents/` folders.

---

## 🎓 **Learning Resources**

### **Understand the Code**
1. Start with `app/main.py` (backend entry)
2. Check `frontend/src/App.jsx` (frontend entry)
3. Read `frontend/src/components/BBQDashboard.jsx` (UI)
4. Explore `app/analytics.py` (business logic)

### **Test the API**
Visit: http://localhost:8000/docs
- Click "Try it out"
- Test endpoints directly

### **Check Logs**
- **Backend:** Terminal 1 shows all requests and errors
- **Frontend:** Press F12 → Console tab in browser

---

## 🚀 **Next Steps After Running**

1. ✅ **Verify dashboard loads** at http://localhost:3000
2. ✅ **Test AI chat** - ask a question
3. ✅ **Check API** - visit http://localhost:8000/docs
4. ✅ **Edit a file** - see hot reload work
5. ✅ **Read code** - understand the architecture

---

## 📞 **Help**

If something doesn't work:

1. **Check error message** in terminal
2. **Google the error** (very helpful!)
3. **Restart both servers** (fixes 80% of issues)
4. **Clear cache:** `npm cache clean --force` in frontend/
5. **Check requirements.txt is installed:** `pip install -r requirements.txt`

---

## ✅ **Success Checklist**

After following the steps:

- [ ] Backend terminal shows "Application startup complete"
- [ ] Frontend terminal shows "ready in XXX ms"
- [ ] Browser loads http://localhost:3000
- [ ] Dashboard shows sales metrics
- [ ] No red errors in browser console (F12)
- [ ] API docs work at http://localhost:8000/docs
- [ ] Settings panel opens (⚙️ button)
- [ ] Charts display properly

---

## 🎉 **You're Done!**

Your **complete production-ready AI Business Intelligence platform** is now running locally!

**Start here:** http://localhost:3000

Enjoy! 🚀

---

**Generated:** 2026-09-01
**Status:** Production Ready ✅
**Phases Complete:** 1-13 ✅
