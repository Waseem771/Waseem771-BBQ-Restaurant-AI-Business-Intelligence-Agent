# BBQ Restaurant AI - Local Development Setup Guide

## Overview
This guide will help you set up and run the entire BBQ Restaurant AI Business Intelligence project locally on Windows.

## Prerequisites
- **Node.js** v16+ (check: `node --version`)
- **npm** v8+ (check: `npm --version`)
- **Python** 3.10+ (check: `python --version`)
- **Git** (for version control)

## Quick Start (5 minutes)

### Step 1: Navigate to Project
```powershell
cd "E:\BBQ Restaurant AI Business Intelligence Agent\Projects\BBQ Restaurant AI Business Intelligence Agent"
```

### Step 2: Install Frontend Dependencies
```powershell
cd frontend
npm install
```

### Step 3: Install Backend Dependencies
```powershell
cd ..
python -m pip install -r requirements.txt
```

### Step 4: Start Backend (in Terminal 1)
```powershell
cd "E:\BBQ Restaurant AI Business Intelligence Agent\Projects\BBQ Restaurant AI Business Intelligence Agent"
python -m uvicorn app.main:app --reload --port 8000
```

You should see:
```
Uvicorn running on http://127.0.0.1:8000
```

### Step 5: Start Frontend (in Terminal 2)
```powershell
cd "E:\BBQ Restaurant AI Business Intelligence Agent\Projects\BBQ Restaurant AI Business Intelligence Agent\frontend"
npm run dev
```

You should see:
```
VITE v5.x.x  ready in XXX ms
➜  Local:   http://localhost:3000/
➜  press h to show help
```

### Step 6: Open in Browser
Visit: **http://localhost:3000**

## Troubleshooting

### Issue: `npm ERR! 404 Not Found` during install
**Solution:** We've removed the problematic `vite-plugin-visualizer` dependency. Run:
```powershell
cd frontend
rm package-lock.json
npm install
```

### Issue: Port 3000 already in use
**Solution:** The Vite dev server will automatically use the next available port (3001, 3002, etc.). Check the terminal output for the actual URL.

### Issue: Backend doesn't start
**Solution:** Ensure Python dependencies are installed:
```powershell
python -m pip install fastapi uvicorn pandas plotly requests python-dotenv streamlit
```

### Issue: React/JSX errors
**Solution:** Clear cache and reinstall:
```powershell
cd frontend
npm cache clean --force
rm -r node_modules package-lock.json
npm install
npm run dev
```

### Issue: CORS errors in console
**Solution:** The backend CORS is configured to accept all origins. Make sure:
1. Backend is running on `http://localhost:8000`
2. Frontend is running on `http://localhost:3000` (or the port shown)
3. Check browser console for exact error

## What's Running

| Service | URL | Purpose |
|---------|-----|---------|
| Backend API | http://localhost:8000 | FastAPI + analytics |
| API Docs | http://localhost:8000/docs | Swagger UI |
| Frontend | http://localhost:3000 | React dashboard |
| WebSocket | ws://localhost:8000 | Real-time updates |

## Project Structure

```
├── app/                    # Backend (FastAPI)
│   ├── main.py            # FastAPI entry point
│   ├── analytics.py       # Analytics logic
│   ├── ai_assistant.py    # AI agent
│   └── api/               # API routes
│
├── frontend/              # Frontend (React + Vite)
│   ├── src/
│   │   ├── App.jsx        # Main app component
│   │   ├── components/    # React components
│   │   ├── services/      # API services
│   │   └── context/       # React context
│   ├── package.json       # Dependencies
│   └── vite.config.js     # Vite config
│
├── data/                  # Sample data
├── documents/             # Business knowledge
└── requirements.txt       # Python dependencies
```

## Development Workflow

### Adding Frontend Dependencies
```powershell
cd frontend
npm install <package-name>
```

### Adding Backend Dependencies
```powershell
pip install <package-name>
pip freeze > requirements.txt
```

### Running Tests
```powershell
# Backend tests
pytest tests/

# Frontend tests
cd frontend
npm test
```

### Building for Production
```powershell
# Frontend
cd frontend
npm run build

# Output: frontend/dist/
```

## Next Steps

1. **Access Dashboard:** http://localhost:3000
2. **Test API:** http://localhost:8000/docs (Swagger UI)
3. **Ask Questions:** Use the AI chat on the dashboard
4. **Check Logs:** Both terminals show real-time logs

## Common Commands Reference

### Frontend
```powershell
npm run dev          # Start dev server
npm run build        # Production build
npm run preview      # Preview production build
npm run lint         # Lint code
npm run format       # Format code
```

### Backend
```powershell
python -m uvicorn app.main:app --reload --port 8000
python -m uvicorn app.main:app --port 8000        # Production
```

## Environment Variables

Frontend uses: `.env.local`
Backend uses: `.env`

Example `.env`:
```
APP_ENV=development
DATABASE_URL=sqlite:///./bbq.db
LLM_API_KEY=your_key_here
```

## Performance Tips

1. **Use Dev Server Caching:** Frontend dev server caches automatically
2. **Check Network Tab:** Use browser DevTools to debug API calls
3. **Monitor Terminal Logs:** Backend logs appear in terminal 1
4. **Reload Frontend:** Press Ctrl+R if stuck
5. **Restart Backend:** Ctrl+C and rerun command

## Getting Help

1. Check terminal output for error messages
2. Open browser DevTools (F12) → Console tab
3. Check backend API: http://localhost:8000/docs
4. Read CLAUDE.md for architecture overview

## Success Checklist

- [ ] Node.js and Python installed
- [ ] `npm install` completed in frontend
- [ ] `pip install -r requirements.txt` completed
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Browser shows dashboard at http://localhost:3000
- [ ] No errors in browser console
- [ ] API Swagger UI works at http://localhost:8000/docs

---

**All set!** Your local development environment is ready. Start with Step 4 above to begin running the application.
