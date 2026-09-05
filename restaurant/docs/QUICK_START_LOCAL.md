# 🚀 BBQ Restaurant AI - Quick Start Guide

## ⚡ 5-Minute Setup (Windows)

### Option 1: Automatic Setup (Recommended)

**Step 1:** Open PowerShell or Command Prompt in the project root

**Step 2:** Run the setup script:

```powershell
# PowerShell users:
.\setup-local-dev.ps1

# Command Prompt users:
setup-local-dev.bat
```

That's it! The script will:
- ✅ Verify Node.js and Python
- ✅ Install frontend dependencies
- ✅ Install backend dependencies
- ✅ Show you what to do next

---

### Option 2: Manual Setup (Step by Step)

#### **Step 1: Install Frontend Dependencies**

Open **Command Prompt** or **PowerShell** and run:

```powershell
cd frontend
npm install
```

**Expected output:**
```
added 450 packages in 45s
```

#### **Step 2: Install Backend Dependencies**

Go back to project root:

```powershell
cd ..
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed fastapi uvicorn pandas plotly...
```

---

## 🏃 Running the Application

### **Terminal 1 - Start Backend (FastAPI)**

```powershell
python -m uvicorn app.main:app --reload --port 8000
```

**You should see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

✅ Backend is ready at: **http://localhost:8000**

---

### **Terminal 2 - Start Frontend (React)**

In a **new terminal/PowerShell window**:

```powershell
cd frontend
npm run dev
```

**You should see:**
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:3000/
➜  press h to show help
```

✅ Frontend is ready at: **http://localhost:3000**

---

## 🌐 Open in Browser

**Visit:** http://localhost:3000

You should see the BBQ Restaurant AI Dashboard with:
- 📊 Sales metrics
- 📈 Charts and analytics
- 🤖 AI chat assistant
- ⚙️ Settings panel

---

## 🔗 Useful URLs

| URL | Purpose |
|-----|---------|
| http://localhost:3000 | **Main Dashboard** |
| http://localhost:8000 | **Backend API** |
| http://localhost:8000/docs | **Swagger API Documentation** (interactive) |
| http://localhost:8000/redoc | **ReDoc API Documentation** |

---

## ⚙️ Common Issues & Fixes

### Issue: "npm: command not found"

**Solution:** Node.js is not installed
- Download from: https://nodejs.org/ (LTS version)
- Restart your terminal after installation
- Verify: `node --version` should show v16+

### Issue: Port 3000 already in use

**Solution:** Vite will automatically try port 3001, 3002, etc.
- Check the terminal output for the actual URL
- Or kill the process: `npx kill-port 3000`

### Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:** Backend dependencies not installed
```powershell
python -m pip install -r requirements.txt
```

### Issue: "npm ERR! 404 Not Found"

**Solution:** We've already fixed this by removing problematic packages
- Run: `cd frontend && npm cache clean --force && npm install`

### Issue: React component errors in browser console

**Solution:** Clear cache and rebuild
```powershell
cd frontend
npm cache clean --force
rm -r node_modules
npm install
npm run dev
```

### Issue: "Cannot GET /" when visiting http://localhost:3000

**Solution:** Frontend dev server might not be running
- Check Terminal 2 output
- Make sure you ran `npm run dev` in the frontend folder
- Restart with Ctrl+C and `npm run dev` again

---

## 🛠️ Frontend Development Commands

```powershell
cd frontend

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code for errors
npm run lint

# Format code automatically
npm run format
```

---

## 🔧 Backend Development Commands

```powershell
# Start with auto-reload (best for development)
python -m uvicorn app.main:app --reload --port 8000

# Start without reload (production)
python -m uvicorn app.main:app --port 8000

# Run specific file
python -m uvicorn app.main:app --reload --log-level debug

# Run tests
pytest tests/
```

---

## 📁 Project Structure

```
project-root/
│
├── frontend/                 # React dashboard (Vite)
│   ├── src/
│   │   ├── App.jsx          # Main app component
│   │   ├── components/      # React components
│   │   ├── services/        # API client
│   │   └── context/         # React context
│   ├── package.json         # Dependencies
│   └── vite.config.js       # Vite config
│
├── app/                      # FastAPI backend
│   ├── main.py              # Entry point
│   ├── analytics.py         # Analytics logic
│   ├── ai_assistant.py      # AI agent
│   └── api/                 # Route handlers
│
├── data/                     # Sample data
├── documents/               # Business knowledge
├── requirements.txt         # Python deps
└── setup-local-dev.ps1     # Setup script
```

---

## 🎯 What Happens After Setup

1. **Backend (port 8000):**
   - Starts FastAPI server
   - Connects to database
   - Loads AI models
   - Ready for API requests

2. **Frontend (port 3000):**
   - Compiles React code
   - Starts Vite dev server
   - Opens browser (if configured)
   - Hot-reloads on file changes

3. **Communication:**
   - Frontend calls backend via `/api/v1/*` endpoints
   - WebSocket connection for real-time updates
   - Both logs appear in respective terminals

---

## ✅ Success Checklist

After following the steps above, verify:

- [ ] Backend terminal shows "Application startup complete"
- [ ] Frontend terminal shows "ready in XXX ms"
- [ ] Browser shows dashboard at http://localhost:3000
- [ ] No errors in browser console (F12 → Console)
- [ ] API docs work at http://localhost:8000/docs
- [ ] Dashboard shows data (sales metrics, charts)
- [ ] Settings panel opens (gear icon)

---

## 🚀 Next Steps

1. **Explore the Dashboard**
   - View sales metrics
   - Check charts and trends
   - Test the AI assistant

2. **Test the API**
   - Visit http://localhost:8000/docs
   - Try out endpoints
   - See the data structure

3. **Make Changes**
   - Edit files in `frontend/src/`
   - See changes in real-time (hot reload)
   - Backend auto-reloads too with `--reload`

4. **Deploy Later**
   - See QUICK_START_DEPLOYMENT.md
   - Deploy to Streamlit Cloud (10 min)
   - Deploy to DigitalOcean (30 min)

---

## 💡 Tips & Tricks

### Keyboard Shortcuts

**Frontend (Vite):**
- `Ctrl + Shift + R` - Hard refresh browser
- `F12` - Open browser DevTools

**Both Terminals:**
- `Ctrl + C` - Stop server
- `Ctrl + L` - Clear terminal

### Debugging

**Frontend:**
```javascript
// Add to React component
console.log('Debug info:', variable);
// View in browser console (F12)
```

**Backend:**
```python
# Add to Python code
print(f"Debug: {variable}")
# View in backend terminal
```

### Common Tasks

**Change Dashboard Colors:**
- Edit `frontend/src/context/SettingsContext.jsx`
- Settings are hot-reloaded

**Add New API Endpoint:**
- Create file in `app/api/routes/`
- Import in `app/main.py`
- Restart backend

**Update Database Schema:**
- Edit `app/db.py`
- Restart backend
- May need to recreate database

---

## 📞 Need Help?

1. **Check Logs:** Both terminals show detailed error messages
2. **Browser Console:** F12 → Console tab shows frontend errors
3. **API Docs:** http://localhost:8000/docs has interactive testing
4. **GitHub Issues:** Look for similar problems
5. **Ask in Issues:** Create detailed bug reports

---

## 🎉 You're All Set!

Your local development environment is ready. Start building amazing features! 

**Next:** Visit http://localhost:3000 and explore the dashboard.

Happy coding! 🚀

---

**Questions or issues?** Check `SETUP_LOCAL_DEV.md` for more detailed troubleshooting.
