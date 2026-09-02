# Anomaly Detection WebSocket Fixes

## Problem Summary

Two errors were occurring in the WebSocket real-time monitoring system when anomaly detection was running:

1. **`Anomaly check error: 'metric'`** — KeyError accessing non-existent 'metric' key
2. **`Failed to send message: Object of type datetime is not JSON serializable`** — datetime serialization error

## Root Causes

### Issue 1: Missing 'metric' Key

The `app.websocket.monitor.py` was trying to access anomaly dictionary keys that didn't exist:

```python
# OLD CODE (monitor.py line 81)
anomaly_key = f"{anomaly['metric']}_{anomaly['date']}"  # 'metric' key doesn't exist!
deviation = abs(anomaly["deviation_percent"])  # Should be "deviation_pct"
```

The `analytics.detect_anomalies()` function in `app/analytics.py` returns anomalies with these keys:
- `date` (string)
- `revenue` (float)
- `expected` (float)
- `deviation_pct` (float)  ← NOT "deviation_percent"
- `direction` (string: "spike" or "drop")
- `severity` (string: "HIGH" or "MEDIUM")

It does NOT include a "metric" key, "actual_value", or "expected_value".

### Issue 2: Datetime JSON Serialization

When Pydantic's `BaseMessage` model calls `model_dump()`, it includes a `timestamp: datetime` field. The WebSocket manager was using `ws.send_json(message)` which uses Python's default JSON encoder, which cannot serialize datetime objects.

## Solutions Implemented

### Fix 1: Updated monitor.py to match analytics data structure

**File:** `app/websocket/monitor.py`

Changed the `_check_anomalies()` method to:
- Use correct key names from `analytics.detect_anomalies()`
- Access `anomaly["deviation_pct"]` instead of `anomaly["deviation_percent"]`
- Access `anomaly["revenue"]` and `anomaly["expected"]` instead of non-existent keys
- Use consistent metric naming: always "revenue" since that's what we detect
- Create appropriate anomaly_key using only available fields

```python
# NEW CODE
anomaly_key = f"revenue_{anomaly['date']}"  # Uses available keys
deviation = abs(anomaly["deviation_pct"])  # Correct key name
value=round(anomaly["revenue"], 2),  # Correct key
expected_value=round(anomaly["expected"], 2),  # Correct key
```

### Fix 2: Custom JSON Encoder for datetime objects

**File:** `app/websocket/manager.py`

Added a custom `DateTimeEncoder` class:

```python
class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles datetime objects."""
    def default(self, obj):
        """Convert datetime to ISO format string."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
```

Updated all broadcast methods to use the custom encoder:
- `send_message()` — uses `json.dumps(message, cls=DateTimeEncoder)`
- `broadcast()` — uses `json.dumps(message, cls=DateTimeEncoder)`
- `broadcast_filtered()` — uses `json.dumps(message, cls=DateTimeEncoder)`

**File:** `app/websocket/schemas.py`

Added Pydantic model configuration to ensure proper serialization:

```python
class BaseMessage(BaseModel):
    model_config = ConfigDict(
        ser_json_timedelta="float",
        ser_json_bytes="utf8",
    )
    type: MessageType
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    client_id: str | None = None
```

## Changes Made

### 1. app/websocket/monitor.py
- Fixed anomaly key generation to use `revenue_{date}`
- Changed `anomaly["deviation_percent"]` → `anomaly["deviation_pct"]`
- Changed `anomaly["actual_value"]` → `anomaly["revenue"]`
- Changed `anomaly["expected_value"]` → `anomaly["expected"]`
- Updated description to use `anomaly["direction"]` for "spike" or "drop"

### 2. app/websocket/manager.py
- Added `DateTimeEncoder` class to handle datetime serialization
- Changed `ws.send_json(message)` → `ws.send_text(json.dumps(message, cls=DateTimeEncoder))`
- Updated all three broadcast methods: `send_message()`, `broadcast()`, `broadcast_filtered()`

### 3. app/websocket/schemas.py
- Added `ConfigDict` import from pydantic
- Added `model_config` to `BaseMessage` for proper datetime serialization

## Testing

Created comprehensive test file: `test_anomaly_websocket_fix.py`

Tests verify:
1. ✓ Anomaly detection returns correct dictionary structure
2. ✓ AnomalyAlert models serialize to JSON correctly
3. ✓ DateTimeEncoder handles datetime objects
4. ✓ Monitor anomaly processing works without KeyError

**Test Results:**
```
Total: 4/4 passed
[SUCCESS] ALL TESTS PASSED - Fixes are working correctly!
```

## Verification

Run the test to verify all fixes:
```bash
python test_anomaly_websocket_fix.py
```

Expected output:
- All 4 tests should pass
- No KeyError for 'metric'
- No datetime serialization errors
- Anomalies should be processed and serializable to JSON

## Impact

These fixes enable:
- Real-time anomaly detection alerts via WebSocket
- Proper JSON serialization of all messages
- Correct data flow from analytics → monitor → dispatcher → clients
- Dashboard receives properly formatted anomaly alerts

## Related Files

- `app/websocket/monitor.py` — Real-time monitoring service
- `app/websocket/manager.py` — WebSocket connection management
- `app/websocket/schemas.py` — Message schemas
- `app/websocket/dispatcher.py` — Event routing
- `app/analytics.py` — Analytics queries (data source)
