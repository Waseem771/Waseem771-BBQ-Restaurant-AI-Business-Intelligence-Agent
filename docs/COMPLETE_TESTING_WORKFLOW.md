# Phase 10 Complete Testing Workflow

**Step-by-Step Guide to Test Real-Time WebSocket Dashboard**

---

## 📋 Prerequisites Checklist

Before you start, verify you have:

```bash
# Check Python version
python --version
# Should be 3.9 or higher

# Check PostgreSQL is running
psql -U postgres -c "SELECT 1"
# Should return: 1

# Check dependencies are installed
pip show fastapi uvicorn websockets pydantic
# Should show all packages installed
```

If any are missing:
```bash
pip install -r requirements.txt
pip install websockets pytest pytest-asyncio
```

---

## 🚀 Complete Testing Workflow (30 minutes)

### PHASE A: Server Setup (5 minutes)

#### Step 1: Open Terminal #1 (Server)
```bash
# Navigate to project directory
cd "E:\BBQ Restaurant AI Business Intelligence Agent\Projects\BBQ Restaurant AI Business Intelligence Agent"

# Start the FastAPI server
uvicorn app.main:app --port 8001 --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8001
INFO:     Application startup complete
INFO:     Real-time monitor background task started
```

✅ **Leave this terminal open!** You'll see logs as events happen.

---

### PHASE B: Dashboard Connection (5 minutes)

#### Step 2: Open Browser and Navigate to Dashboard

**Option 1: Direct File Path**
```
Press Ctrl+L in browser address bar
Paste: file:///E:/BBQ%20Restaurant%20AI%20Business%20Intelligence%20Agent/Projects/BBQ%20Restaurant%20AI%20Business%20Intelligence%20Agent/dashboard.html
Press Enter
```

**Option 2: Using File Manager**
```
Navigate to: E:\BBQ Restaurant AI Business Intelligence Agent\Projects\BBQ Restaurant AI Business Intelligence Agent\
Find: dashboard.html
Double-click to open in default browser
```

**Expected Result - You Should See:**

```
┌─────────────────────────────────────────────────────────────┐
│  🍖 BBQ Restaurant AI Dashboard     🟢 Live Connection     │
│  Real-time business intelligence                            │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────┬──────────────────────┐
│ 💰 TOTAL REVENUE     │ 📊 TOTAL ORDERS      │
│ ₨ 2,450,000         │ 1,250                │
│ +0%                 │ +0%                  │
└──────────────────────┴──────────────────────┘

┌──────────────────────┬──────────────────────┐
│ 🍽️ AVG ORDER VALUE   │ ⭐ BEST PRODUCT      │
│ ₨ 1,960             │ BBQ Platter          │
│ +0%                 │ Top seller           │
└──────────────────────┴──────────────────────┘

📈 Revenue Trend Chart        📦 Top Products Chart
[Chart Display Area]          [Chart Display Area]

🚨 Real-Time Alerts
Waiting for alerts...

📋 Message Log
[14:30:45] 🔌 WebSocket client initialized...
[14:30:46] Connecting to WebSocket...
[14:30:46] ✅ Connected to WebSocket
[14:30:46] 📨 Message: connection_ack
```

✅ **Dashboard should show "🟢 Live Connection"**

---

#### Step 3: Verify WebSocket Connection

**Using Browser DevTools:**

1. Press `F12` to open Developer Tools
2. Click **Network** tab
3. Filter by **WS** (WebSockets)
4. You should see: `ws://localhost:8001/ws/dashboard`
5. Click it
6. Click **Messages** tab

**You should see at least one message:**
```json
{
  "type": "connection_ack",
  "client_id": "abc-123-def...",
  "server_version": "1.0.0",
  "features": ["metrics", "anomalies", "forecasts", "alerts", "system_status"]
}
```

✅ **WebSocket is connected!**

---

### PHASE C: Test Real-Time Broadcasting (10 minutes)

#### Step 4: Trigger Test Messages (Terminal #2)

**Open a new terminal (Terminal #2):**

```bash
cd "E:\BBQ Restaurant AI Business Intelligence Agent\Projects\BBQ Restaurant AI Business Intelligence Agent"
```

**Test 1: Send Anomaly Alert**
```bash
curl -X POST http://localhost:8001/ws/test-anomaly
```

**Expected Output in Terminal #2:**
```json
{
  "status": "anomaly_broadcasted",
  "clients": 1
}
```

**Expected Output in Browser Dashboard:**
```
🚨 Real-Time Alerts

┌─────────────────────────────────────────────┐
│ 🚨 REVENUE                           14:31  │
│ Revenue dropped 66.67% below expected       │
│ Expected: ₨150,000                         │
│ Actual:   ₨50,000                          │
│ Deviation: 66.67%                  [HIGH]  │
└─────────────────────────────────────────────┘

📋 Message Log
...
[14:31:02] 📨 Message: anomaly_detected
[14:31:02] 🚨 Anomaly Alert: revenue (high)
```

✅ **Alert appears instantly in dashboard!**

---

**Test 2: Send Forecast Alert**

```bash
curl -X POST http://localhost:8001/ws/test-forecast
```

**Expected in Dashboard:**
```
🚨 Real-Time Alerts

┌─────────────────────────────────────────────┐
│ 📈 REVENUE                           14:32  │
│ Trend: UP | Confidence: 92%                 │
│ Predicted: ₨210,000                        │
│ Sales are forecasted to trend up.           │
│ Consider adjusting inventory.               │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ 🚨 REVENUE                           14:31  │
│ Revenue dropped 66.67% below expected       │
│ [HIGH]                                      │
└─────────────────────────────────────────────┘
```

✅ **Two alerts now showing!**

---

**Test 3: Send KPI Update**

```bash
curl -X POST http://localhost:8001/ws/test-kpi
```

**Expected in Dashboard:**
```
💰 TOTAL REVENUE      (Pulses and glows red briefly)
₨ 2,450,000
+0%

📊 TOTAL ORDERS       (Updates)
1,250
+0%

🍽️ AVG ORDER VALUE
₨ 1,960
+0%

⭐ BEST PRODUCT
BBQ Platter

📋 Message Log
[14:32:45] 📨 Message: kpi_update
[14:32:45] 📊 KPI Update received
```

✅ **KPI cards update smoothly!**

---

#### Step 5: Check WebSocket Status

**In Terminal #2, check connections:**

```bash
curl http://localhost:8001/ws/status | python -m json.tool
```

**Expected Output:**
```json
{
  "active_connections": 1,
  "client_ids": [
    "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6"
  ],
  "event_types": [
    "anomaly",
    "forecast",
    "kpi_update"
  ],
  "recent_events": {
    "anomaly": [
      {
        "timestamp": "2026-08-31T14:31:02.123456",
        "data": {
          "type": "anomaly_detected",
          "anomaly_id": "test_anomaly_123",
          "metric": "revenue",
          ...
        }
      }
    ],
    ...
  }
}
```

✅ **Status endpoint working!**

---

### PHASE D: Multi-Client Testing (7 minutes)

#### Step 6: Test Multiple Browsers

**In the same browser:**
1. Open a new tab
2. Navigate to: `file:///E:/BBQ%20Restaurant%20AI%20Business%20Intelligence%20Agent/Projects/BBQ%20Restaurant%20AI%20Business%20Intelligence%20Agent/dashboard.html`
3. You now have 2 browser tabs connected!

**Or in a different browser:**
1. Open Firefox (if you used Chrome)
2. Navigate to the same dashboard.html file
3. Now you have 2 browsers connected!

**Trigger a test message:**

```bash
curl -X POST http://localhost:8001/ws/test-anomaly
```

**Expected Result:**
```
✅ Both browser tabs show the alert
✅ Alert appears at the same time
✅ Same timestamp on both
✅ Both get "🟢 Live Connection"
```

**Check status:**
```bash
curl http://localhost:8001/ws/status | python -m json.tool
```

**Expected:**
```json
{
  "active_connections": 2,
  "client_ids": [
    "client-id-1...",
    "client-id-2..."
  ],
  ...
}
```

✅ **Multi-client support working!**

---

#### Step 7: Test Disconnection Handling

**With 2 browser tabs open:**

1. Close one tab (simulates client disconnect)
2. Check status:
   ```bash
   curl http://localhost:8001/ws/status
   ```
3. Should show 1 connection now
4. Trigger another test message
5. Other tab still receives it ✅

---

### PHASE E: Advanced Testing (3 minutes)

#### Step 8: View DevTools Messages in Real-Time

**In Browser with Dashboard open:**

1. Press `F12`
2. Go to **Network** tab
3. Filter by **WS**
4. Click the WebSocket connection
5. Go to **Messages** tab
6. Back in Terminal #2, run:
   ```bash
   curl -X POST http://localhost:8001/ws/test-anomaly
   ```
7. **Watch the message appear in real-time in DevTools!**

**You'll see:**
```json
← {
    "type": "anomaly_detected",
    "timestamp": "2026-08-31T14:35:10.123456",
    "anomaly_id": "test_anomaly_123",
    "metric": "revenue",
    "value": 50000,
    "expected_value": 150000,
    "deviation_percent": 66.67,
    "severity": "high",
    "description": "Test anomaly: revenue dropped from 150000 to 50000"
  }
```

✅ **You can see exact WebSocket protocol!**

---

#### Step 9: Check Server Logs

**Look at Terminal #1 (Server) logs:**

You should see:
```
INFO:     Client a1b2c3d4 connected to dashboard (branch=1)
DEBUG:    Received from a1b2c3d4: {"type": "subscribe", ...}
DEBUG:    Checked 1 anomalies
INFO:     KPI metrics updated
INFO:     Client a1b2c3d4 disconnected
```

✅ **Server logs show all activity!**

---

## ✅ Complete Testing Checklist

Mark off each as you complete it:

### Connection & Setup
```
☐ Server starts without errors
☐ Dashboard loads in browser
☐ Status shows "🟢 Live Connection"
☐ DevTools shows WS connection
☐ Message log shows connection successful
```

### Anomaly Alerts
```
☐ Anomaly alert appears in < 1 second
☐ Alert shows correct metric (revenue)
☐ Alert shows correct values
☐ Alert shows [HIGH] severity badge
☐ Alert slides in from left
☐ Message log shows anomaly received
☐ Browser DevTools shows JSON message
```

### Forecast Alerts
```
☐ Forecast alert appears instantly
☐ Shows trend (UP/DOWN/STABLE)
☐ Shows confidence percentage
☐ Shows recommendation
☐ Added to alerts list
☐ Message log updated
```

### KPI Updates
```
☐ KPI cards update smoothly
☐ Values pulse/animate
☐ Percentage changes update
☐ Cards glow red briefly
☐ All 4 cards update
☐ Changes persist
```

### Multi-Client
```
☐ Dashboard works in Tab 1
☐ Dashboard works in Tab 2
☐ Both receive same message
☐ Status shows 2 connections
☐ Disconnect Tab 1, Tab 2 still works
☐ Tab 1 reconnects automatically
```

### UI/UX
```
☐ Dark theme displays correctly
☐ All text is readable
☐ Charts display data
☐ Alerts have proper colors
☐ Animations are smooth
☐ No console errors (F12)
☐ Responsive on different sizes
```

### Performance
```
☐ Messages appear instantly (< 100ms)
☐ No lag when multiple updates
☐ Dashboard stays responsive
☐ No memory leaks
☐ CPU usage reasonable
```

---

## 🎯 Success Criteria

**Phase 10 testing is COMPLETE when ALL of these are true:**

✅ WebSocket connects without errors  
✅ All 3 test endpoints work (anomaly, forecast, KPI)  
✅ Messages appear in real-time (< 1 second)  
✅ Dashboard displays all updates correctly  
✅ Multi-client support verified  
✅ Reconnection works automatically  
✅ No errors in browser console  
✅ Server logs show expected activity  
✅ All animations work smoothly  
✅ Status endpoints return correct data  

---

## 📊 Sample Output You Should See

### Terminal #1 (Server) - Expected Logs
```
INFO:     Uvicorn running on http://127.0.0.1:8001
INFO:     Application startup complete
INFO:     Real-time monitor background task started
INFO:     Client a1b2c3d4 connected to dashboard (branch=1)
DEBUG:    Client a1b2c3d4 subscribed to: []
DEBUG:    Checked 1 anomalies
INFO:     KPI metrics updated
INFO:     Client a1b2c3d4 disconnected
```

### Terminal #2 (Tests) - Expected Results
```
$ curl -X POST http://localhost:8001/ws/test-anomaly
{"status":"anomaly_broadcasted","clients":1}

$ curl -X POST http://localhost:8001/ws/test-forecast
{"status":"forecast_broadcasted","clients":1}

$ curl -X POST http://localhost:8001/ws/test-kpi
{"status":"kpi_broadcasted","clients":1}

$ curl http://localhost:8001/ws/status | python -m json.tool
{
  "active_connections": 1,
  "client_ids": [...],
  "event_types": ["anomaly", "forecast", "kpi_update"],
  "recent_events": {...}
}
```

### Browser - Expected Display
```
🟢 Live Connection
💰 ₨2,450,000 +0%
📊 1,250 +0%
🍽️ ₨1,960 +0%
⭐ BBQ Platter

[Charts Display]

🚨 3 Real-Time Alerts
  1. Revenue Anomaly (HIGH)
  2. Revenue Forecast (UP trend)
  3. KPI Update

📋 Message Log (20+ entries)
```

---

## 🐛 Troubleshooting During Testing

### Problem: "Connection refused" when opening dashboard

**Solution:**
```bash
# Verify server is running in Terminal #1
# Check output shows: "Uvicorn running on http://127.0.0.1:8001"
# If not running, start it:
uvicorn app.main:app --port 8001 --reload
```

---

### Problem: "Waiting for messages..." but alerts don't appear

**Solution:**
```bash
# Verify you're triggering correctly:
curl -X POST http://localhost:8001/ws/test-anomaly

# Check /ws/status to see connections:
curl http://localhost:8001/ws/status

# Check server logs for errors in Terminal #1
# Verify no firewall blocking port 8001
```

---

### Problem: Dashboard shows "🔴 Disconnected"

**Solution:**
```bash
# Check server is still running
# Try reconnecting manually (F5 refresh)
# Check server logs for client disconnect message
# Check port 8001 is accessible:
netstat -ano | findstr :8001
```

---

### Problem: Browser DevTools shows no WebSocket

**Solution:**
```bash
# Make sure DevTools is open BEFORE opening dashboard
# Filter by "WS" (not just any protocol)
# Try different browser (Chrome, Firefox, Edge)
# Check Console tab for JavaScript errors
```

---

## 📈 Performance Expectations

| Metric | Expected | Actual |
|--------|----------|--------|
| Connection Time | < 500ms | _____ |
| Message Delivery | < 100ms | _____ |
| Alert Appearance | < 1 sec | _____ |
| KPI Update | < 1 sec | _____ |
| Server Memory | < 100MB | _____ |
| CPU Usage | < 10% idle | _____ |

---

## 🎉 Completion

When you've completed all steps:

1. ✅ All checks pass
2. ✅ All tests complete successfully
3. ✅ Dashboard updates in real-time
4. ✅ Multi-client support verified
5. ✅ No errors in logs or console

**Phase 10 Real-Time WebSocket Layer is COMPLETE!**

---

## 📚 Next Resources

- **QUICK_REFERENCE.md** - Commands cheat sheet
- **DASHBOARD_GUIDE.md** - Dashboard feature details
- **PHASE_10_TESTING_GUIDE.md** - Detailed testing guide
- **test_phase_10.py** - Interactive test suite

---

## 🚀 Ready for Phase 11?

Once Phase 10 testing is complete:

1. All components working ✅
2. Real-time updates verified ✅
3. Multi-client support confirmed ✅
4. Production-ready code ✅

**Next: Phase 11 - Docker & Production Deployment**

```bash
# Phase 11 will include:
# • Dockerfile creation
# • docker-compose.yml setup
# • Environment configuration
# • Production deployment
# • Monitoring & logging
```

---

*Last Updated: 2026-08-31*  
*Workflow: Phase 10 Complete Testing*  
*Status: Ready for Testing ✅*
