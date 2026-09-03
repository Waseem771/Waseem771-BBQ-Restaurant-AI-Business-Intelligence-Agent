# 🚀 START HERE - BBQ Restaurant AI Local Setup

## ⏱️ Time Required: 2 minutes to start running

---

## Step-by-Step Instructions

### **STEP 1: Open Terminal 1** (Backend)

Press `Win + R` and type `powershell`, then press Enter.

Copy and paste this command:
```powershell
cd "E:\BBQ Restaurant AI Business Intelligence Agent\Projects\BBQ Restaurant AI Business Intelligence Agent" ; python -m uvicorn app.main:app --reload --port 8000
```

**Wait for this message:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

✅ **Backend is running!**

---

### **STEP 2: Open Terminal 2** (Frontend)

Press `Win + R` and type `powershell`, then press Enter (another one).

Copy and paste this command:
```powershell
cd "E:\BBQ Restaurant AI Business Intelligence Agent\Projects\BBQ Restaurant AI Business Intelligence Agent\frontend" ; npm run dev
```

**Wait for this message:**
```
VITE v5.x.x  ready in XXX ms
Local:   http://localhost:3000/
```

✅ **Frontend is running!**

---

### **STEP 3: Open Your Browser**

Click this link or type in address bar:

## 🌐 **http://localhost:3000**

---

## ✅ You Should See

```
┌─────────────────────────────────────────────────────┐
│  BBQ Restaurant AI Dashboard                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Total Revenue    Total Orders    Avg Order Value  │
│  Rs. 2,450,000    3,420           Rs. 716          │
│                                                     │
│  [Sales Trend Chart]                               │
│  [Product Performance Chart]                       │
│  [Category Breakdown Pie Chart]                    │
│                                                     │
│  AI Chat Box                                        │
│  [Ask me anything...]                              │
│                                                     │
│  Settings ⚙️  Alerts 🔔                             │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🎯 What to Try First

1. **View Metrics** - See sales data on dashboard
2. **Check Charts** - Explore revenue trends and products
3. **Open Settings** - Click ⚙️ gear icon to customize
4. **Try AI Chat** - Ask: "What are our top products?"
5. **View Alerts** - Check 🔔 bell icon for anomalies

---

## 🔗 Useful Links

| Link | What For |
|------|----------|
| http://localhost:3000 | **Main Dashboard** ⭐ |
| http://localhost:8000/docs | **Test API** (interactive) |
| http://localhost:8000/redoc | **API Documentation** |

---

## 🛑 To Stop Everything

In each terminal, press:
```
Ctrl + C
```

---

## 🔄 If Something Goes Wrong

### Problem: Blank page
- Press `Ctrl + Shift + R` in browser (hard refresh)

### Problem: Port 3000 in use
- Check terminal 2 output for different port (3001, 3002, etc.)

### Problem: Can't connect to backend
- Make sure terminal 1 shows "Application startup complete"
- Try refreshing browser

### Problem: npm/python command not found
- Close terminal and try again
- May need to restart after installing Node.js/Python

---

## 📁 Files Changed/Created

**Fixed:**
- `frontend/package.json` - Removed problematic vite-plugin-visualizer ✅

**Created (for reference):**
- `RUN_LOCALLY_NOW.md` - Detailed guide
- `QUICK_START_LOCAL.md` - Comprehensive instructions
- `SETUP_COMPLETE_SUMMARY.md` - Full summary
- `setup-local-dev.ps1` - Automation script
- `setup-local-dev.bat` - Windows batch script
- `start-servers.bat` - Quick launcher

---

## 🎉 Success Criteria

Check off as you go:

- [ ] Backend terminal shows "Application startup complete"
- [ ] Frontend terminal shows "ready in XXX ms"  
- [ ] Browser loads http://localhost:3000
- [ ] You see the dashboard with metrics
- [ ] No red errors in browser console (F12)
- [ ] Settings panel opens (gear icon)
- [ ] Charts display data
- [ ] AI chat is visible

---

## 💡 Pro Tips

1. **Keep both terminals open** - shows you all the logs
2. **Hard refresh is your friend** - `Ctrl+Shift+R` fixes many issues
3. **Check browser console** - F12 → Console tab shows frontend errors
4. **Check backend terminal** - shows all API requests
5. **Files auto-reload** - make changes and see them instantly

---

## 🆘 Need Help?

1. **Check terminal output** - error messages are usually clear
2. **Google the error** - usually someone solved it before
3. **Restart everything** - fixes 80% of issues
4. **Read TROUBLESHOOTING.md** - detailed solutions for common problems
5. **Check SETUP_COMPLETE_SUMMARY.md** - comprehensive reference

---

## 🚀 What Happens Next

1. You have a fully functional AI Business Intelligence dashboard
2. Backend API at http://localhost:8000 with Swagger docs
3. Real-time analytics and charts
4. AI assistant that understands your restaurant data
5. Sales forecasting and anomaly detection
6. Production-ready code ready to deploy

---

## 📊 Tech Stack

- **Frontend:** React 18, Vite 5, Tailwind CSS, Recharts
- **Backend:** FastAPI, Uvicorn, Python 3.13
- **Database:** SQLite (development), PostgreSQL (production ready)
- **Real-time:** WebSockets
- **ML:** Scikit-learn, XGBoost

---

## ⏱️ Timeline

```
Now           Start servers
│             Terminal 1: Backend
│             Terminal 2: Frontend
│
2 min later   Browser loads dashboard
│
5 min later   You're exploring features
│
∞            Building amazing features!
```

---

## 🎓 Next Steps (After Running)

1. Explore the dashboard interface
2. Test the AI chat with questions
3. Check API docs at http://localhost:8000/docs
4. Make a code change and see hot reload
5. Read `CLAUDE.md` to understand architecture
6. Check `app/main.py` to understand backend
7. Check `frontend/src/App.jsx` to understand frontend

---

## ✨ Key Features Ready

✅ Sales Dashboard with KPIs  
✅ Interactive Charts & Graphs  
✅ AI Chat Assistant  
✅ Real-time Alerts  
✅ Settings & Customization  
✅ Dark/Light Theme  
✅ Anomaly Detection  
✅ Sales Forecasting  
✅ Product Analytics  
✅ WebSocket Support  

---

## 🎯 Your Mission (If You Accept It)

1. ✅ Start backend (Terminal 1)
2. ✅ Start frontend (Terminal 2)
3. ✅ Visit http://localhost:3000
4. ✅ Explore the dashboard
5. ✅ Ask AI a question
6. ✅ Check the settings
7. ✅ View the API docs
8. ✅ Make a change and see it reload

---

**Everything is ready!**

**Go forth and build amazing things! 🚀**

---

**Questions?** Check the other markdown files we created.

**Ready?** Open those two terminals and let's go!

---

*Generated: 2026-09-01*  
*Status: Ready to Run ✅*  
*All Systems: Go ✅*
