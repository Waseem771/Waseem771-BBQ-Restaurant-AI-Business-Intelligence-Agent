"""
Simple WebSocket test client for testing real-time functionality.
Run this to connect to the WebSocket endpoint and see messages.
"""
import asyncio
import json
import websockets
from datetime import datetime


async def test_dashboard_connection():
    """Test connecting to the /ws/dashboard endpoint."""
    print("=" * 80)
    print("WEBSOCKET CLIENT TEST")
    print("=" * 80)
    print(f"\n📡 Connecting to ws://localhost:8001/ws/dashboard")
    print("   with branch_id=1 and user_id=test_user\n")

    uri = "ws://localhost:8001/ws/dashboard?branch_id=1&user_id=test_user"

    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected successfully!\n")

            # Receive connection acknowledgment
            print("Waiting for messages...\n")

            # Set a timeout for receiving messages
            try:
                while True:
                    # Wait for a message with 10 second timeout
                    message = await asyncio.wait_for(
                        websocket.recv(),
                        timeout=10.0
                    )

                    data = json.loads(message)
                    timestamp = datetime.now().strftime("%H:%M:%S")

                    print(f"[{timestamp}] 📨 Message received:")
                    print(f"   Type: {data.get('type', 'unknown')}")
                    print(f"   Data: {json.dumps(data, indent=6)}")
                    print()

            except asyncio.TimeoutError:
                print("⏱️  No messages received for 10 seconds")
                print("   (This is normal if no anomalies/updates are being sent)")

    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"   Make sure the server is running on http://localhost:8001")


async def test_alerts_connection():
    """Test connecting to the /ws/alerts endpoint."""
    print("\n" + "=" * 80)
    print("ALERTS ENDPOINT TEST")
    print("=" * 80)
    print(f"\n📡 Connecting to ws://localhost:8001/ws/alerts")
    print("   with severity=high\n")

    uri = "ws://localhost:8001/ws/alerts?severity=high&user_id=test_user"

    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to alerts endpoint!\n")

            print("Waiting for alert messages...\n")

            try:
                while True:
                    message = await asyncio.wait_for(
                        websocket.recv(),
                        timeout=10.0
                    )

                    data = json.loads(message)
                    timestamp = datetime.now().strftime("%H:%M:%S")

                    print(f"[{timestamp}] 🚨 Alert received:")
                    print(f"   Type: {data.get('type', 'unknown')}")
                    print(f"   Severity: {data.get('severity', 'unknown')}")
                    print(f"   Data: {json.dumps(data, indent=6)}")
                    print()

            except asyncio.TimeoutError:
                print("⏱️  No alert messages received for 10 seconds")

    except Exception as e:
        print(f"❌ Error: {e}")


async def trigger_and_receive():
    """Trigger test messages and receive them in real-time."""
    print("\n" + "=" * 80)
    print("REAL-TIME TEST: TRIGGER MESSAGES AND RECEIVE")
    print("=" * 80)
    print("\nThis test will:")
    print("  1. Connect to WebSocket")
    print("  2. Wait a moment")
    print("  3. Trigger test messages via REST API")
    print("  4. Receive them in real-time\n")

    uri = "ws://localhost:8001/ws/dashboard?branch_id=1&user_id=test_user"

    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected!\n")

            # Receive connection ack
            print("Waiting for connection acknowledgment...")
            ack = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            ack_data = json.loads(ack)
            print(f"✅ Got ACK: {ack_data.get('type')}\n")

            # Now trigger messages from another process
            print("📤 Triggering test messages...")
            print("   (In a real scenario, these would come from the monitoring service)\n")

            # Wait to receive messages
            message_count = 0
            try:
                while message_count < 5:  # Receive up to 5 messages
                    message = await asyncio.wait_for(
                        websocket.recv(),
                        timeout=5.0
                    )

                    data = json.loads(message)
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    message_count += 1

                    print(f"[{timestamp}] 📨 Message {message_count}:")
                    print(f"   Type: {data.get('type')}")

                    if data.get('type') == 'anomaly_detected':
                        print(f"   Metric: {data.get('metric')}")
                        print(f"   Severity: {data.get('severity')}")
                        print(f"   Value: {data.get('value')}")
                    elif data.get('type') == 'kpi_update':
                        kpis = data.get('kpis', {})
                        for k, v in list(kpis.items())[:2]:
                            print(f"   {k}: {v}")
                    print()

            except asyncio.TimeoutError:
                print(f"\n⏱️  Received {message_count} messages, timeout waiting for more")

    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Run all tests."""
    print("\n🧪 WebSocket Testing Suite\n")

    # Ask user what to test
    print("Choose test to run:")
    print("  1. Dashboard endpoint")
    print("  2. Alerts endpoint")
    print("  3. Real-time trigger and receive")
    print("  4. All tests")

    choice = input("\nEnter choice (1-4): ").strip()

    if choice == "1":
        asyncio.run(test_dashboard_connection())
    elif choice == "2":
        asyncio.run(test_alerts_connection())
    elif choice == "3":
        asyncio.run(trigger_and_receive())
    elif choice == "4":
        asyncio.run(test_dashboard_connection())
        asyncio.run(test_alerts_connection())
        asyncio.run(trigger_and_receive())
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
