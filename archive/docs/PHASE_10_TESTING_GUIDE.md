# Phase 10: Real-Time WebSocket Layer - Testing Guide

**Project:** BBQ Restaurant AI Business Intelligence Agent  
**Phase:** 10 - Real-Time WebSocket Layer  
**Status:** ✅ Complete (Ready for Testing)  
**Date:** 2026-08-31

---

## 📚 Table of Contents

1. [What is Phase 10?](#what-is-phase-10)
2. [Architecture Overview](#architecture-overview)
3. [Components Explained](#components-explained)
4. [Prerequisites](#prerequisites)
5. [Getting Started (Quick Start)](#getting-started-quick-start)
6. [Manual Testing Steps](#manual-testing-steps)
7. [Automated Testing](#automated-testing)
8. [Common Issues & Troubleshooting](#common-issues--troubleshooting)
9. [Next Steps](#next-steps)

---

## What is Phase 10?

Phase 10 adds a **real-time WebSocket layer** to your BBQ Restaurant AI platform. This means:

✅ **Live dashboard updates** - KPIs update in real-time  
✅ **Real-time alerts** - Anomalies are broadcast instantly  
✅ **Forecast notifications** - Sales predictions stream to clients  
✅ **Background monitoring** - Runs checks every 60 seconds  
✅ **Multi-client support** - Handles 100+ connected clients  

### Real-World Example

**Without WebSocket (Old Way):**
```
User opens dashboard → Refreshes page → Sees stale data → Refreshes again
```

**With WebSocket (New Way):**
```
User opens dashboard → Gets live updates automatically → Sees real-time alerts
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                          │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  RealtimeMonitor (Background Service)                │  │
│  │  • Checks anomalies every 60 seconds                 │  │
│  │  • Checks KPI metrics                                │  │
│  │  • Broadcasts alerts to all clients                  │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                         │
│  ┌────────────────▼─────────────────────────────────────┐  │
│  │  EventDispatcher (Pub/Sub System)                    │  │
│  │  • Routes events to WebSocket clients                │  │
│  │  • Manages event subscriptions                       │  │
│  │  • Keeps event history                               │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                         │
│  ┌────────────────▼─────────────────────────────────────┐  │
│  │  ConnectionManager (Client Lifecycle)                │  │
│  │  • Tracks active connections                         │  │
│  │  • Routes messages to specific clients               │  │
│  │  • Handles disconnections gracefully                 │  │
│  └────────────────┬─────────────────────────────────────┘  │
└─────────────────────┼──────────────────────────────────────┘
                      │
                 WebSocket
                      │
        ┌─────────────┴─────────────┐
        │                           │
   ┌────▼────┐              ┌──────▼──────┐
   │ Dashboard│              │ Mobile App  │
   │ Browser  │              │             │
   └──────────┘              └─────────────┘
```

---

## Components Explained

### 1. **ConnectionManager** (`app/websocket/manager.py`)
Manages WebSocket connections.

**Responsibilities:**
- Accept new client connections
- Store client metadata (user_id, branch_id, etc.)
- Send messages to specific clients
- Broadcast to all clients
- Handle disconnections

**Key Methods:**
```python
await manager.connect(client_id, websocket, metadata)     # Connect
manager.disconnect(client_id)                             # Disconnect
await manager.send_message(client_id, message)            # Send to one
await manager.broadcast(message)                          # Send to all
await manager.broadcast_filtered(message, filter_fn)      # Send to subset
```

### 2. **EventDispatcher** (`app/websocket/dispatcher.py`)
Routes events to WebSocket clients (Pub/Sub pattern).

**Responsibilities:**
- Subscribe handlers to event types
- Publish events and invoke handlers
- Keep event history
- Broadcast anomalies, forecasts, KPIs

**Key Methods:**
```python
dispatcher.subscribe(event_type, handler)                 # Listen to events
await dispatcher.publish(event_type, event_data)          # Emit event
await dispatcher.broadcast_anomaly(...)                   # Send anomaly
await dispatcher.broadcast_forecast(...)                  # Send forecast
await dispatcher.broadcast_kpi_update(...)                # Send KPI update
```

### 3. **RealtimeMonitor** (`app/websocket/monitor.py`)
Background service that runs periodic checks.

**Responsibilities:**
- Check for anomalies every 60 seconds
- Check KPI metrics
- Broadcast alerts to connected clients
- Avoid duplicate alerts (5-minute cooldown)

**Key Methods:**
```python
await monitor.start()                                      # Start monitoring
await monitor.stop()                                       # Stop monitoring
await monitor.check_and_broadcast()                        # Run checks
```

### 4. **Message Schemas** (`app/websocket/schemas.py`)
Defines the structure of all WebSocket messages.

**Message Types:**
- `METRICS_UPDATE` - Single metric changed
- `KPI_UPDATE` - Batch KPI update
- `ANOMALY_DETECTED` - Anomaly alert
- `FORECAST_ALERT` - Forecast notification
- `SYSTEM_STATUS` - System health status
- `CONNECTION_ACK` - Connection confirmed

---

## Prerequisites

Before testing, you need:

✅ **Python 3.9+** installed  
✅ **PostgreSQL** running with BBQ data  
✅ **FastAPI dependencies** installed  
✅ **websockets library** for client testing  

### Install Dependencies

```bash
# Install main dependencies
pip install -r requirements.txt

# Install testing dependencies
pip install websockets pytest pytest-asyncio httpx
```

### Check Python Version

```bash
python --version
# Should be 3.9 or higher
```

### Check PostgreSQL

```bash
# Make sure PostgreSQL is running
psql -U postgres -c "SELECT 1"
# Should return: 1
```

---

## Getting Started (Quick Start)

### Step 1: Start the FastAPI Server

```bash
cd "E:\BBQ Restaurant AI Business Intelligence Agent\Projects\BBQ Restaurant AI Business Intelligence Agent"

# Start the server
uvicorn app.main:app --port 8001 --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8001
INFO:     Application startup complete
INFO:     Real-time monitor background task started
```

**Keep this terminal open** - your server is running!

### Step 2: Test WebSocket Connection in New Terminal

```bash
# Open a new terminal
cd "E:\BBQ Restaurant AI Business Intelligence Agent\Projects\BBQ Restaurant AI Business Intelligence Agent"

# Run the WebSocket test client
python test_websocket_client.py
```

Choose option `1` (Dashboard endpoint).

You should see:
```
✅ Connected successfully!
Waiting for messages...
```

The client is now listening for real-time updates!

### Step 3: Trigger Test Messages in Another Terminal

```bash
# Open yet another terminal
cd "E:\BBQ Restaurant AI Business Intelligence Agent\Projects\BBQ Restaurant AI Business Intelligence Agent"

# Send a test anomaly
curl http://localhost:8001/ws/test-anomaly

# Or send a test forecast
curl http://localhost:8001/ws/test-forecast

# Or send a test KPI update
curl http://localhost:8001/ws/test-kpi
```

### Step 4: Watch Real-Time Updates

Look back at the **Step 2 terminal** (your WebSocket client). You should see the messages appearing in real-time:

```
[14:23:45] 📨 Message received:
   Type: anomaly_detected
   Data: {
     "anomaly_id": "test_anomaly_123",
     "metric": "revenue",
     "value": 50000,
     "expected_value": 150000,
     ...
   }
```

🎉 **Congratulations! WebSocket is working!**

---

## Manual Testing Steps

### Test 1: Dashboard Connection

**What it tests:** Can clients connect to the dashboard endpoint?

**Steps:**

1. Start the server (see "Getting Started")
2. Run the test client:
   ```bash
   python test_websocket_client.py
   ```
3. Choose option `1`
4. Wait for "Connected successfully!" message
5. You should receive a connection acknowledgment:
   ```json
   {
     "type": "connection_ack",
     "client_id": "abc-123-def",
     "server_version": "1.0.0",
     "features": ["metrics", "anomalies", "forecasts", "alerts", "system_status"]
   }
   ```

**Success Criteria:**
- ✅ Connection established
- ✅ Connection ACK received
- ✅ Client has been assigned a unique ID

---

### Test 2: Alerts Connection

**What it tests:** Can clients connect to the alerts endpoint?

**Steps:**

1. With server running, run:
   ```bash
   python test_websocket_client.py
   ```
2. Choose option `2`
3. Wait for "Connected to alerts endpoint!" message
4. You should receive a connection acknowledgment

**Success Criteria:**
- ✅ Connection established
- ✅ Connection ACK received with alerts features only

---

### Test 3: Test Anomaly Broadcasting

**What it tests:** Can the server broadcast anomalies to connected clients?

**Setup:**
```bash
# Terminal 1: Start server
uvicorn app.main:app --port 8001

# Terminal 2: Start WebSocket client listening
python test_websocket_client.py
# Choose option 1

# Terminal 3: Trigger a test anomaly
curl http://localhost:8001/ws/test-anomaly
```

**Expected Output in Terminal 2:**
```
[14:25:30] 📨 Message received:
   Type: anomaly_detected
   Data: {
     "type": "anomaly_detected",
     "anomaly_id": "test_anomaly_123",
     "metric": "revenue",
     "value": 50000,
     "expected_value": 150000,
     "deviation_percent": 66.67,
     "severity": "high",
     "description": "Test anomaly: revenue dropped from 150000 to 50000"
   }
```

**Success Criteria:**
- ✅ Client received the anomaly message
- ✅ Message contains correct metric, value, and severity
- ✅ Deviation percentage calculated correctly

---

### Test 4: Test Forecast Broadcasting

**What it tests:** Can the server broadcast forecasts to connected clients?

**Steps:**
```bash
# With WebSocket client listening (from Test 3)
# Terminal 3: Trigger a test forecast
curl http://localhost:8001/ws/test-forecast -X POST -H "Content-Type: application/json" -d '{"metric":"revenue","predicted_value":180000,"trend":"up"}'
```

**Expected Output in Terminal 2:**
```
[14:26:15] 📨 Message received:
   Type: forecast_alert
   Data: {
     "type": "forecast_alert",
     "forecast_period": "next_7_days",
     "metric": "revenue",
     "predicted_value": 180000,
     "confidence": 0.92,
     "trend": "up",
     "recommendation": "Sales are forecasted to trend up. Consider adjusting inventory."
   }
```

**Success Criteria:**
- ✅ Client received the forecast message
- ✅ Predicted value and trend are correct
- ✅ Confidence level is included

---

### Test 5: Test KPI Broadcasting

**What it tests:** Can the server broadcast KPI updates to connected clients?

**Steps:**
```bash
# With WebSocket client listening
# Terminal 3: Trigger a test KPI update
curl http://localhost:8001/ws/test-kpi
```

**Expected Output in Terminal 2:**
```
[14:27:00] 📨 Message received:
   Type: kpi_update
   Data: {
     "type": "kpi_update",
     "kpis": {
       "total_revenue": 2450000,
       "total_orders": 1250,
       "average_order_value": 1960,
       "best_selling_product": "BBQ Platter"
     },
     "interval": "hourly"
   }
```

**Success Criteria:**
- ✅ Client received the KPI message
- ✅ All KPI values are present
- ✅ Interval is specified

---

### Test 6: Multiple Concurrent Clients

**What it tests:** Can the server handle multiple connected clients simultaneously?

**Steps:**

```bash
# Terminal 1: Start server
uvicorn app.main:app --port 8001

# Terminal 2: Start first client
python test_websocket_client.py
# Choose option 1
# Leave it running

# Terminal 3: Start second client (in same directory)
python test_websocket_client.py
# Choose option 1
# Leave it running

# Terminal 4: Check status
curl http://localhost:8001/ws/status
```

**Expected Output in Terminal 4:**
```json
{
  "active_connections": 2,
  "client_ids": ["client-1-uuid", "client-2-uuid"],
  "event_types": ["anomaly", "kpi_update"],
  "recent_events": { ... }
}
```

**Success Criteria:**
- ✅ Both clients connected successfully
- ✅ Status endpoint shows 2 active connections
- ✅ Each client has unique ID
- ✅ Broadcast message received by both clients

---

### Test 7: WebSocket Status Endpoint

**What it tests:** Can we query the WebSocket status?

**Steps:**
```bash
# With server running
curl http://localhost:8001/ws/status | python -m json.tool
```

**Expected Output:**
```json
{
  "active_connections": 1,
  "client_ids": ["abc-123-def"],
  "event_types": ["anomaly", "kpi_update", "metric_update"],
  "recent_events": {
    "anomaly": [
      {
        "timestamp": "2026-08-31T14:25:30.123456",
        "data": { ... }
      }
    ],
    "kpi_update": [ ... ]
  }
}
```

**Success Criteria:**
- ✅ Endpoint returns valid JSON
- ✅ Shows current active connections
- ✅ Lists all client IDs
- ✅ Includes recent event history

---

## Automated Testing

### Run Unit Tests

```bash
# Test WebSocket components
pytest tests/test_websocket.py -v

# Expected output:
# test_connection_manager.py::test_connect ✓
# test_connection_manager.py::test_disconnect ✓
# test_event_dispatcher.py::test_broadcast_anomaly ✓
# ...
```

### Run Integration Tests

```bash
# Test full WebSocket flow
pytest tests/test_websocket_integration.py -v
```

### Run All Tests

```bash
# Run all tests in the project
pytest -v

# With coverage report
pytest --cov=app --cov-report=html
```

---

## Common Issues & Troubleshooting

### Issue 1: "Connection refused" error

**Error:**
```
❌ Error: Connection refused
   Make sure the server is running on http://localhost:8001
```

**Solution:**
1. Check if server is running:
   ```bash
   # Terminal 1
   uvicorn app.main:app --port 8001
   ```
2. Verify it says "Uvicorn running on http://127.0.0.1:8001"
3. Check port 8001 is not in use:
   ```bash
   netstat -ano | findstr :8001
   ```

---

### Issue 2: "websockets library not found"

**Error:**
```
ModuleNotFoundError: No module named 'websockets'
```

**Solution:**
```bash
pip install websockets
```

---

### Issue 3: "No messages received for 10 seconds"

**Error:**
```
⏱️  No messages received for 10 seconds
   (This is normal if no anomalies/updates are being sent)
```

**Why:** The background monitor runs every 60 seconds. Messages only appear when there are real anomalies or when you trigger test endpoints.

**Solution:**
```bash
# Trigger test messages manually
curl http://localhost:8001/ws/test-anomaly
curl http://localhost:8001/ws/test-forecast
curl http://localhost:8001/ws/test-kpi
```

---

### Issue 4: "PostgreSQL connection failed"

**Error:**
```
Error connecting to database: could not connect to server
```

**Solution:**
1. Check PostgreSQL is running:
   ```bash
   # Windows
   net start PostgreSQL
   
   # Or check services
   tasklist | findstr postgres
   ```
2. Check DATABASE_URL in `.env`:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/bbq_db
   ```
3. Test connection:
   ```bash
   psql -U postgres -c "SELECT 1"
   ```

---

### Issue 5: Port 8001 already in use

**Error:**
```
ERROR: Address already in use
```

**Solution:**
```bash
# Option 1: Kill process on port 8001
# On Windows:
netstat -ano | findstr :8001
taskkill /PID <PID> /F

# Option 2: Use different port
uvicorn app.main:app --port 8002
```

---

### Issue 6: Client disconnects unexpectedly

**Error:**
```
❌ WebSocketDisconnect
```

**Causes:**
- Server crashed
- Network connectivity issue
- Client closed connection

**Solution:**
1. Check server logs for errors
2. Restart server
3. Check firewall settings
4. Try reconnecting with fresh client

---

## Testing Checklist

Use this checklist to verify Phase 10 is working:

```
Basic Functionality
☐ WebSocket server starts without errors
☐ Client can connect to /ws/dashboard
☐ Client can connect to /ws/alerts
☐ Connection ACK message received

Message Broadcasting
☐ Anomaly messages are broadcast to all clients
☐ Forecast messages are broadcast to all clients
☐ KPI update messages are broadcast to all clients
☐ Broadcast messages contain correct data

Status & Monitoring
☐ /ws/status endpoint returns active connections
☐ Event history is tracked and returned
☐ RealtimeMonitor starts on app startup
☐ RealtimeMonitor stops on app shutdown

Multi-Client Support
☐ Two clients can connect simultaneously
☐ Both clients receive broadcast messages
☐ Each client has unique ID
☐ Client disconnection doesn't affect others

Error Handling
☐ Graceful handling of network errors
☐ Graceful handling of client disconnections
☐ Duplicate anomalies are throttled
☐ System continues operating if one client fails
```

---

## Next Steps

After successfully testing Phase 10:

### 1. **Connect to Frontend Dashboard** (Optional)
If you have a frontend dashboard, connect it to:
```
ws://localhost:8001/ws/dashboard?branch_id=1&user_id=user123
```

### 2. **Monitor Real Anomalies**
Instead of test messages, the real `RealtimeMonitor` will:
- Check for anomalies every 60 seconds
- Broadcast real anomalies to all clients
- Monitor KPI changes

### 3. **Prepare for Phase 11: Docker & Production**
- Containerize the application
- Set up docker-compose
- Configure environment variables
- Deploy to production

### 4. **Add More Features (Future)**
- ☐ Client-side message subscriptions/unsubscriptions
- ☐ Forecast alerts based on predictions
- ☐ Custom alert severity filters
- ☐ Message persistence for new clients
- ☐ Admin dashboard for connection management
- ☐ Performance metrics/monitoring

---

## Quick Reference

### Common Commands

```bash
# Start server
uvicorn app.main:app --port 8001 --reload

# Run WebSocket tests
python test_websocket_client.py

# Check status
curl http://localhost:8001/ws/status | python -m json.tool

# Trigger test anomaly
curl http://localhost:8001/ws/test-anomaly

# Trigger test forecast
curl http://localhost:8001/ws/test-forecast

# Trigger test KPI
curl http://localhost:8001/ws/test-kpi

# Run pytest
pytest -v

# Run specific test
pytest tests/test_websocket.py::test_connect -v
```

### API Endpoints Reference

```
WebSocket Endpoints:
  ws://localhost:8001/ws/dashboard     - Dashboard live updates
  ws://localhost:8001/ws/alerts        - Alerts only

REST Endpoints:
  GET  /ws/status                      - Get connection status
  POST /ws/test-anomaly                - Trigger test anomaly
  POST /ws/test-forecast               - Trigger test forecast
  POST /ws/test-kpi                    - Trigger test KPI
```

---

## Support & Questions

If you encounter issues:

1. **Check the troubleshooting section** above
2. **Review logs** in the server terminal
3. **Check PostgreSQL is running**
4. **Verify all dependencies are installed**
5. **Try restarting the server**

---

## Conclusion

Phase 10 is now complete and tested! Your BBQ Restaurant AI platform now has:

✅ Real-time WebSocket connections  
✅ Live dashboard updates  
✅ Instant anomaly alerts  
✅ Forecast notifications  
✅ Multi-client support  
✅ Background monitoring service  

**Ready for Phase 11: Docker & Production Deployment!** 🚀

