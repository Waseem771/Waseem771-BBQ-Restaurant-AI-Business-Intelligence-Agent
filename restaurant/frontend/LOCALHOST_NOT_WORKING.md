# 🔧 Localhost:3000 Not Working - Troubleshooting Guide

## Step 1: Check if Dev Server is Actually Running

Open a terminal and run:
```bash
cd "E:\BBQ Restaurant AI Business Intelligence Agent\Projects\BBQ Restaurant AI Business Intelligence Agent\frontend"
npm run dev
```

**You should see:**
```
VITE v5.0.0  ready in XXX ms

➜  Local:   http://localhost:3000/
➜  press h to show help
```

If you DON'T see this, the dev server isn't running.

---

## Step 2: Check if Port 3000 is Accessible

**Option A: Windows PowerShell**
```powershell
Test-NetConnection -ComputerName localhost -Port 3000
```

**Option B: Browser**
Open these URLs and see which one works:
- http://localhost:3000
- http://127.0.0.1:3000
- http://[::1]:3000

---

## Step 3: Check Console Errors

1. Open browser
2. Press **F12** (opens DevTools)
3. Click **Console** tab
4. Look for **RED** error messages
5. **Screenshot the error and share it**

Common errors:
- `Cannot find module 'react'` → Run `npm install`
- `Unexpected token` → Syntax error in code
- `EADDRINUSE` → Port 3000 already in use

---

## Step 4: Try These Commands

### If you get "npm not found":
```powershell
# Check if Node is installed
node --version    # Should show v16+
npm --version     # Should show 8+

# If not installed, download from nodejs.org
```

### If you get "Port already in use":
```powershell
# Find what's using port 3000
netstat -ano | findstr :3000

# Kill the process (replace PID with the number)
taskkill /PID 12345 /F
```

### If you get "Module not found":
```bash
cd frontend
npm install
npm run dev
```

---

## Step 5: If Server Starts but Page is Blank

1. Press **F12** → **Console**
2. Look for errors
3. **Most likely:** Backend not running

**Fix:**
```bash
# In another terminal, start backend
cd backend
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## Step 6: If Page Shows "Error Loading Overview"

**This is GOOD!** It means:
- ✅ React is working
- ✅ Dashboard component loaded
- ❌ Backend API is not responding

**Fix:**
1. Start backend: `python main.py`
2. Refresh browser: `Ctrl+F5`
3. Should see data now

---

## Step 7: If Page is Still Blank

Try the **Diagnostic Mode:**

The app now has a debug button (🔧) in bottom-right corner.

1. Look for small **🔧** button in bottom-right
2. Click it
3. You should see diagnostic page
4. This tests if React is working

If diagnostic page loads → React is fine, problem is elsewhere
If diagnostic page doesn't load → React isn't working

---

## Quick Fix Checklist

- [ ] Dev server running? (`npm run dev` in terminal)
- [ ] Correct port? (localhost:3000 or check terminal output)
- [ ] Port accessible? (Try http://127.0.0.1:3000)
- [ ] Backend running? (`python main.py` in another terminal)
- [ ] No console errors? (F12 → Console tab)
- [ ] Refreshed browser? (Ctrl+F5 or Cmd+Shift+R)

---

## Common Issues & Solutions

### Issue: "Cannot GET /"
**Problem:** Frontend dev server not running  
**Fix:** `cd frontend && npm run dev`

### Issue: "This site can't be reached"
**Problem:** Dev server crashed or not started  
**Fix:** 
```bash
cd frontend
npm run dev
```

### Issue: Blank page with no errors
**Problem:** React loaded but no data  
**Fix:** 
```bash
cd backend
python main.py
```

### Issue: "Error loading overview"
**Problem:** Backend API not responding  
**Fix:**
```bash
cd backend
python main.py
```

### Issue: "Module not found"
**Problem:** Dependencies not installed  
**Fix:**
```bash
cd frontend
npm install
npm run dev
```

### Issue: Port 3000 in use
**Problem:** Another process using port 3000  
**Options:**
1. Kill the process: `taskkill /PID xxxx /F`
2. Use different port: Vite auto-selects next port
3. Stop the other app

---

## What You Should See

### Success ✅
- Page loads at localhost:3000
- Dashboard visible with data
- KPI cards show numbers
- Charts display
- No red console errors

### In Progress ⏳
- Page loading spinner
- "Loading data…" message

### Error (but OK) ⚠️
- "Error loading overview" message
- "Could not reach backend" message
- Red banner at top
- **This is GOOD** - error handling is working!

### Crash (bad) ❌
- White blank page
- Browser shows error
- Console has red errors
- **Tell me the error message**

---

## Get Me This Information

If it's **still not working**, please provide:

1. **What you see in browser:**
   - Blank page?
   - Error message?
   - Loading spinner?
   - Screenshot?

2. **Console errors (F12):**
   - Any red messages?
   - Screenshot?

3. **Terminal output:**
   - What does `npm run dev` show?
   - Any error messages?
   - Screenshot?

4. **Backend status:**
   - Is `python main.py` running?
   - Does terminal show "Uvicorn running"?

5. **Port status:**
   - Run: `netstat -ano | findstr :3000`
   - Tell me output

---

## I'll Fix It Once I Know The Error

Share:
1. Screenshot of browser (what you see)
2. Screenshot of console (F12 → Console)
3. Screenshot of terminal
4. Exact error messages

Then I can give you the exact fix! 🎯

---

## TL;DR - Quick Start

**Terminal 1:**
```bash
cd backend
python main.py
```

**Terminal 2:**
```bash
cd frontend
npm run dev
```

**Browser:**
```
http://localhost:3000
```

Done! If not working, share the error from F12 console.

---

**Status:** Ready to Debug  
**Next Action:** Share error screenshot
