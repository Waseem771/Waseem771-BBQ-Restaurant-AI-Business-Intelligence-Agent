#!/usr/bin/env python
"""
Dashboard & WebSocket System Verification

Verifies that:
1. Backend is running on correct port
2. WebSocket endpoint is accessible
3. Test endpoints work
4. Real-time monitor is operational
5. Dashboard can connect
"""

import asyncio
import json
import sys
from datetime import datetime

try:
    import aiohttp
except ImportError:
    print("ERROR: aiohttp not installed. Run: pip install aiohttp")
    sys.exit(1)


class DashboardVerifier:
    def __init__(self, host="localhost", port=8000):
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.ws_url = f"ws://{host}:{port}/ws/dashboard"
        self.passed = 0
        self.failed = 0

    async def test_backend_running(self):
        """Test if backend is running"""
        print("\n[TEST 1] Checking if backend is running...")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/health", timeout=aiohttp.ClientTimeout(total=5)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        print(f"  [OK] Backend is running")
                        print(f"       Status: {data.get('status')}")
                        print(f"       Database: {data.get('db')}")
                        self.passed += 1
                        return True
                    else:
                        print(f"  [FAIL] Backend returned status {resp.status}")
                        self.failed += 1
                        return False
        except Exception as e:
            print(f"  [FAIL] Cannot connect to backend: {e}")
            print(f"        Make sure to run: python run.py")
            self.failed += 1
            return False

    async def test_websocket_endpoint(self):
        """Test if WebSocket endpoint is accessible"""
        print("\n[TEST 2] Checking WebSocket endpoint...")
        try:
            async with aiohttp.ClientSession() as session:
                # Check if endpoint exists via HTTP
                async with session.get(
                    f"{self.base_url}/ws/status",
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        print(f"  [OK] WebSocket endpoint accessible")
                        print(f"       Active connections: {data.get('active_connections')}")
                        print(f"       Event types: {data.get('event_types')}")
                        self.passed += 1
                        return True
                    else:
                        print(f"  [FAIL] WebSocket status returned {resp.status}")
                        self.failed += 1
                        return False
        except Exception as e:
            print(f"  [FAIL] Cannot access WebSocket endpoint: {e}")
            self.failed += 1
            return False

    async def test_analytics_endpoints(self):
        """Test if analytics endpoints work"""
        print("\n[TEST 3] Checking analytics endpoints...")
        try:
            async with aiohttp.ClientSession() as session:
                # Test KPI endpoint (correct path)
                async with session.get(
                    f"{self.base_url}/api/v1/dashboard/kpis",
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        print(f"  [OK] Analytics endpoints working")
                        print(f"       Total Revenue: Rs {data.get('total_revenue', 0):,.0f}")
                        print(f"       Total Orders: {data.get('total_orders', 0)}")
                        print(f"       Avg Order Value: Rs {data.get('avg_order_value', 0):,.0f}")
                        self.passed += 1
                        return True
                    else:
                        print(f"  [FAIL] Analytics endpoint returned {resp.status}")
                        self.failed += 1
                        return False
        except Exception as e:
            print(f"  [FAIL] Cannot access analytics endpoints: {e}")
            self.failed += 1
            return False

    async def test_anomaly_detection(self):
        """Test if anomaly detection works"""
        print("\n[TEST 4] Checking anomaly detection...")
        try:
            async with aiohttp.ClientSession() as session:
                # Test anomaly endpoint
                async with session.get(
                    f"{self.base_url}/api/v1/anomalies",
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        count = len(data)
                        print(f"  [OK] Anomaly detection working")
                        print(f"       Anomalies detected: {count}")
                        if count > 0:
                            first = data[0]
                            print(f"       Sample: {first.get('date')} - {first.get('severity')}")
                        self.passed += 1
                        return True
                    else:
                        print(f"  [FAIL] Anomaly endpoint returned {resp.status}")
                        self.failed += 1
                        return False
        except Exception as e:
            print(f"  [FAIL] Cannot access anomaly endpoint: {e}")
            self.failed += 1
            return False

    async def test_broadcast_anomaly(self):
        """Test broadcast anomaly endpoint"""
        print("\n[TEST 5] Testing anomaly broadcast endpoint...")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/ws/test-anomaly?metric=revenue&value=50000&expected_value=150000",
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        print(f"  [OK] Anomaly broadcast successful")
                        print(f"       Status: {data.get('status')}")
                        print(f"       Clients receiving: {data.get('clients')}")
                        self.passed += 1
                        return True
                    else:
                        print(f"  [FAIL] Broadcast returned {resp.status}")
                        self.failed += 1
                        return False
        except Exception as e:
            print(f"  [FAIL] Cannot broadcast anomaly: {e}")
            self.failed += 1
            return False

    async def test_broadcast_kpi(self):
        """Test broadcast KPI endpoint"""
        print("\n[TEST 6] Testing KPI broadcast endpoint...")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/ws/test-kpi",
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        print(f"  [OK] KPI broadcast successful")
                        print(f"       Status: {data.get('status')}")
                        print(f"       Clients receiving: {data.get('clients')}")
                        self.passed += 1
                        return True
                    else:
                        print(f"  [FAIL] Broadcast returned {resp.status}")
                        self.failed += 1
                        return False
        except Exception as e:
            print(f"  [FAIL] Cannot broadcast KPI: {e}")
            self.failed += 1
            return False

    async def test_websocket_connection(self):
        """Test actual WebSocket connection"""
        print("\n[TEST 7] Testing WebSocket connection...")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.ws_connect(
                    f"{self.ws_url}?branch_id=1&user_id=test_user",
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as ws:
                    # Wait for connection_ack
                    msg = await ws.receive_json(timeout=2)
                    if msg.get("type") == "connection_ack":
                        print(f"  [OK] WebSocket connection successful")
                        print(f"       Client ID: {msg.get('client_id')[:8]}...")
                        print(f"       Server Version: {msg.get('server_version')}")
                        print(f"       Features: {msg.get('features')}")
                        self.passed += 1
                        return True
                    else:
                        print(f"  [FAIL] Unexpected message type: {msg.get('type')}")
                        self.failed += 1
                        return False
        except Exception as e:
            print(f"  [FAIL] WebSocket connection failed: {e}")
            self.failed += 1
            return False

    async def run_all_tests(self):
        """Run all tests"""
        print("=" * 80)
        print("DASHBOARD & WEBSOCKET SYSTEM VERIFICATION")
        print("=" * 80)
        print(f"Target: {self.base_url}")
        print(f"WebSocket: {self.ws_url}")

        await self.test_backend_running()
        await self.test_websocket_endpoint()
        await self.test_analytics_endpoints()
        await self.test_anomaly_detection()
        await self.test_broadcast_anomaly()
        await self.test_broadcast_kpi()
        await self.test_websocket_connection()

        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print(f"Passed: {self.passed}/7")
        print(f"Failed: {self.failed}/7")

        if self.failed == 0:
            print("\n[SUCCESS] All systems operational!")
            print("\nNext steps:")
            print("1. Open dashboard.html in your browser")
            print("2. Watch the real-time alerts and KPI updates")
            print("3. The dashboard auto-connects to WebSocket")
            return 0
        else:
            print(f"\n[ERROR] {self.failed} test(s) failed")
            print("\nTroubleshooting:")
            print("1. Make sure backend is running: python run.py")
            print("2. Check if port 8000 is available: netstat -ano | findstr :8000")
            print("3. Verify database file exists: data/bbq.db")
            return 1

        print("=" * 80)


async def main():
    verifier = DashboardVerifier(host="localhost", port=8000)
    exit_code = await verifier.run_all_tests()
    sys.exit(exit_code)


if __name__ == "__main__":
    print("\n[STARTING] Verification...")
    print("(This may take a few seconds)\n")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] Verification cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        sys.exit(1)
