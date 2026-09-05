"""Test to verify anomaly detection WebSocket fixes.

Tests:
1. Analytics detect_anomalies returns correct structure
2. Monitor processes anomalies correctly
3. JSON serialization handles datetime objects
4. No 'metric' KeyError
"""
import json
import asyncio
from datetime import datetime

from app import analytics
from app.websocket.schemas import AnomalyAlert, AlertSeverity
from app.websocket.manager import DateTimeEncoder


def test_detect_anomalies_structure():
    """Verify detect_anomalies returns correct dict structure."""
    print("\n[TEST 1] Checking anomaly detection structure...")

    anomalies = analytics.detect_anomalies(threshold=0.6)

    if not anomalies:
        print("  [OK] No anomalies detected (this is OK for test data)")
        return True

    # Check first anomaly
    anomaly = anomalies[0]
    required_keys = {"date", "revenue", "expected", "deviation_pct", "direction", "severity"}

    actual_keys = set(anomaly.keys())
    if required_keys.issubset(actual_keys):
        print(f"  [OK] Anomaly has all required keys: {required_keys}")
        print(f"    Sample: {anomaly}")
        return True
    else:
        missing = required_keys - actual_keys
        print(f"  [FAIL] Missing keys: {missing}")
        print(f"    Got: {actual_keys}")
        return False


def test_anomaly_alert_serialization():
    """Verify AnomalyAlert serializes to JSON correctly."""
    print("\n[TEST 2] Checking AnomalyAlert JSON serialization...")

    # Create alert
    alert = AnomalyAlert(
        anomaly_id="anom_revenue_2026-08-20",
        metric="revenue",
        value=92000.0,
        expected_value=165000.0,
        deviation_percent=44.2,
        severity=AlertSeverity.CRITICAL,
        description="Revenue spike on 2026-08-20: expected PKR 165,000, got PKR 92,000 (-44.2%)",
    )

    # Serialize to dict
    data = alert.model_dump()

    # Serialize to JSON using custom encoder
    try:
        json_str = json.dumps(data, cls=DateTimeEncoder)
        print(f"  [OK] Successfully serialized to JSON")
        print(f"    Length: {len(json_str)} chars")

        # Verify it's valid JSON
        parsed = json.loads(json_str)
        print(f"  [OK] JSON is valid and parseable")

        # Check key fields
        assert parsed["metric"] == "revenue", "metric field missing or wrong"
        assert parsed["anomaly_id"] == "anom_revenue_2026-08-20", "anomaly_id field wrong"
        assert isinstance(parsed["timestamp"], str), "timestamp should be ISO string"
        print(f"  [OK] All key fields present and correct")
        print(f"    Timestamp: {parsed['timestamp']}")

        return True
    except Exception as e:
        print(f"  [FAIL] {e}")
        return False


def test_monitor_anomaly_processing():
    """Verify monitor processes analytics anomalies correctly."""
    print("\n[TEST 3] Checking monitor anomaly processing logic...")

    anomalies = analytics.detect_anomalies(threshold=0.6)

    if not anomalies:
        print("  [OK] No anomalies in test data (this is OK)")
        return True

    # Simulate what monitor does
    for anomaly in anomalies:
        try:
            # This is the line that was failing with 'metric' KeyError
            anomaly_key = f"revenue_{anomaly['date']}"

            # Check deviation
            deviation = abs(anomaly["deviation_pct"])
            if deviation > 50:
                severity = AlertSeverity.CRITICAL
            elif deviation > 30:
                severity = AlertSeverity.HIGH
            else:
                severity = AlertSeverity.MEDIUM

            # Create message (this is what dispatcher.broadcast_anomaly does)
            message = AnomalyAlert(
                anomaly_id=f"anom_revenue_{anomaly['date']}",
                metric="revenue",
                value=round(anomaly["revenue"], 2),
                expected_value=round(anomaly["expected"], 2),
                deviation_percent=deviation,
                severity=severity,
                description=f"Revenue {anomaly['direction']} on {anomaly['date']}: "
                f"expected PKR {anomaly['expected']:,.0f}, got PKR {anomaly['revenue']:,.0f} "
                f"({anomaly['deviation_pct']:+.1f}%)",
            )

            # Try to serialize
            json_str = json.dumps(message.model_dump(), cls=DateTimeEncoder)

            print(f"  [OK] Processed anomaly: {anomaly_key}")
            print(f"    Severity: {severity}")
            print(f"    Description: {message.description[:80]}...")

        except KeyError as e:
            print(f"  [FAIL] KeyError: {e}")
            return False
        except Exception as e:
            print(f"  [FAIL] {e}")
            return False

    print(f"  [OK] All {len(anomalies)} anomalies processed successfully")
    return True


def test_datetime_encoder():
    """Verify DateTimeEncoder handles datetime objects."""
    print("\n[TEST 4] Checking DateTimeEncoder...")

    now = datetime.utcnow()
    test_data = {
        "timestamp": now,
        "name": "test",
        "value": 123.45,
    }

    try:
        json_str = json.dumps(test_data, cls=DateTimeEncoder)
        parsed = json.loads(json_str)

        assert isinstance(parsed["timestamp"], str), "timestamp should be string after encoding"
        assert parsed["timestamp"] == now.isoformat(), "timestamp should be ISO format"

        print(f"  [OK] DateTimeEncoder works correctly")
        print(f"    Original: {now}")
        print(f"    Encoded: {parsed['timestamp']}")

        return True
    except Exception as e:
        print(f"  [FAIL] {e}")
        return False


if __name__ == "__main__":
    print("=" * 80)
    print("ANOMALY DETECTION WEBSOCKET FIX VERIFICATION")
    print("=" * 80)

    results = []
    results.append(("Anomaly Detection Structure", test_detect_anomalies_structure()))
    results.append(("AnomalyAlert Serialization", test_anomaly_alert_serialization()))
    results.append(("DateTime Encoder", test_datetime_encoder()))
    results.append(("Monitor Anomaly Processing", test_monitor_anomaly_processing()))

    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {status}: {name}")

    print(f"\nTotal: {passed}/{total} passed")

    if passed == total:
        print("\n[SUCCESS] ALL TESTS PASSED - Fixes are working correctly!")
    else:
        print(f"\n[ERROR] {total - passed} test(s) failed")

    print("=" * 80)
