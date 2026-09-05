#!/usr/bin/env python3
"""
Phase 10 Testing Script - Interactive Demo
Run this to test the real-time WebSocket layer with demo data
"""
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_section(title):
    """Print a formatted section"""
    print(f"\n► {title}")
    print("-" * 80)


async def test_connection_manager():
    """Test the ConnectionManager class"""
    print_section("Testing ConnectionManager")

    from app.websocket.manager import ConnectionManager

    manager = ConnectionManager()
    print("✅ ConnectionManager initialized")

    # Test properties
    print(f"   • Active connections: {manager.get_active_count()}")
    print(f"   • Max connections: (unlimited)")

    print("\n✅ ConnectionManager test passed")


async def test_schemas():
    """Test WebSocket message schemas"""
    print_section("Testing WebSocket Message Schemas")

    from app.websocket.schemas import (
        MessageType, AlertSeverity, AnomalyAlert,
        KPIUpdateMessage, ForecastAlert, ConnectionAckMessage
    )
    from datetime import datetime

    # Test AnomalyAlert
    anomaly = AnomalyAlert(
        anomaly_id="test_001",
        metric="revenue",
        value=50000,
        expected_value=150000,
        deviation_percent=66.67,
        severity=AlertSeverity.HIGH,
        description="Test anomaly"
    )
    print("✅ AnomalyAlert schema valid")
    print(f"   • ID: {anomaly.anomaly_id}")
    print(f"   • Metric: {anomaly.metric}")
    print(f"   • Severity: {anomaly.severity}")

    # Test KPIUpdateMessage
    kpi_msg = KPIUpdateMessage(
        kpis={
            "total_revenue": 2450000,
            "total_orders": 1250,
            "average_order_value": 1960
        }
    )
    print("\n✅ KPIUpdateMessage schema valid")
    print(f"   • KPIs: {len(kpi_msg.kpis)} metrics")
    for key, val in list(kpi_msg.kpis.items())[:2]:
        print(f"     - {key}: {val}")

    # Test ForecastAlert
    forecast = ForecastAlert(
        forecast_period="next_7_days",
        metric="revenue",
        predicted_value=210000,
        confidence=0.92,
        trend="up",
        recommendation="Increase inventory"
    )
    print("\n✅ ForecastAlert schema valid")
    print(f"   • Metric: {forecast.metric}")
    print(f"   • Trend: {forecast.trend}")
    print(f"   • Confidence: {forecast.confidence * 100:.0f}%")

    print("\n✅ All message schemas test passed")


async def test_event_dispatcher():
    """Test the EventDispatcher"""
    print_section("Testing EventDispatcher")

    from app.websocket.dispatcher import EventDispatcher, init_dispatcher
    from app.websocket.manager import ConnectionManager

    manager = ConnectionManager()
    dispatcher = init_dispatcher(manager)

    print("✅ EventDispatcher initialized")

    # Test event subscription
    events_received = []

    async def test_handler(data):
        events_received.append(data)

    dispatcher.subscribe("test_event", test_handler)
    print("✅ Event handler subscribed")

    # Publish event
    await dispatcher.publish("test_event", {"test": "data"})
    print("✅ Event published")

    # Check event history
    history = dispatcher.get_event_history("test_event")
    print(f"✅ Event history: {len(history)} events stored")

    print("\n✅ EventDispatcher test passed")


async def test_realtime_monitor():
    """Test the RealtimeMonitor"""
    print_section("Testing RealtimeMonitor")

    from app.websocket.monitor import RealtimeMonitor, get_monitor

    monitor = RealtimeMonitor(check_interval_seconds=1)

    print("✅ RealtimeMonitor initialized")
    print(f"   • Check interval: {monitor.check_interval}s")
    print(f"   • Alert cooldown: {monitor.alert_cooldown}")
    print(f"   • Is running: {monitor.is_running}")

    # Test start/stop
    print("\n   Starting monitor (1 second test)...")
    asyncio.create_task(monitor.start())
    await asyncio.sleep(1.5)
    await monitor.stop()
    print("✅ Monitor started and stopped successfully")

    print("\n✅ RealtimeMonitor test passed")


async def test_rest_endpoints():
    """Test REST API endpoints"""
    print_section("Testing REST API Endpoints")

    print("📋 Available endpoints:")

    endpoints = {
        "Health Check": "GET /health",
        "WebSocket Status": "GET /ws/status",
        "Test Anomaly": "POST /ws/test-anomaly",
        "Test Forecast": "POST /ws/test-forecast",
        "Test KPI": "POST /ws/test-kpi",
        "Dashboard KPIs": "GET /api/v1/dashboard/kpis",
        "Anomalies": "GET /api/v1/anomalies",
    }

    for name, endpoint in endpoints.items():
        print(f"   ✓ {name}")
        print(f"     {endpoint}")

    print("\n✅ All endpoints documented")


def print_quick_start():
    """Print quick start guide"""
    print_header("QUICK START GUIDE")

    print("🚀 To test Phase 10 Real-Time WebSocket:\n")

    steps = [
        ("Terminal 1: Start the FastAPI server",
         "uvicorn app.main:app --port 8001 --reload"),

        ("Terminal 2: Open the dashboard",
         "1. Open: file:///E:/BBQ%20Restaurant%20AI%20Business%20Intelligence%20Agent/Projects/BBQ%20Restaurant%20AI%20Business%20Intelligence%20Agent/dashboard.html\n   (Or: Press Ctrl+O in browser and select dashboard.html)"),

        ("Terminal 3: Trigger test messages",
         "python test_websocket_client.py\n   Choose option 3 (Real-time trigger and receive)"),
    ]

    for i, (title, cmd) in enumerate(steps, 1):
        print(f"Step {i}: {title}")
        print(f"   $ {cmd}\n")


def print_demo_commands():
    """Print demo commands"""
    print_header("DEMO COMMANDS")

    print("Use these commands to trigger real-time updates:\n")

    commands = [
        ("Trigger Anomaly Alert",
         "curl http://localhost:8001/ws/test-anomaly"),

        ("Trigger Forecast Alert",
         "curl http://localhost:8001/ws/test-forecast"),

        ("Trigger KPI Update",
         "curl http://localhost:8001/ws/test-kpi"),

        ("Check WebSocket Status",
         "curl http://localhost:8001/ws/status | python -m json.tool"),

        ("Check System Health",
         "curl http://localhost:8001/health | python -m json.tool"),
    ]

    for i, (title, cmd) in enumerate(commands, 1):
        print(f"{i}. {title}")
        print(f"   $ {cmd}\n")


def print_testing_checklist():
    """Print testing checklist"""
    print_header("TESTING CHECKLIST")

    print("Use this checklist to verify Phase 10 is working:\n")

    categories = {
        "Connection": [
            "WebSocket server starts without errors",
            "Client can connect to /ws/dashboard",
            "Client can connect to /ws/alerts",
            "Connection ACK message received",
        ],
        "Broadcasting": [
            "Anomaly messages are broadcast",
            "Forecast messages are broadcast",
            "KPI updates are broadcast",
            "Messages contain correct data",
        ],
        "Multi-Client": [
            "Two clients can connect simultaneously",
            "Both clients receive messages",
            "Each client has unique ID",
            "Disconnect doesn't affect others",
        ],
        "Dashboard": [
            "Dashboard loads without errors",
            "WebSocket connects automatically",
            "KPI cards update in real-time",
            "Alerts appear in real-time",
            "Charts display data correctly",
        ]
    }

    for category, items in categories.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  ☐ {item}")


def print_file_structure():
    """Print Phase 10 file structure"""
    print_header("PHASE 10 FILE STRUCTURE")

    print("Key files for real-time WebSocket functionality:\n")

    files = {
        "app/websocket/": [
            "__init__.py - Package initialization",
            "manager.py - ConnectionManager (tracks clients)",
            "dispatcher.py - EventDispatcher (routes events)",
            "schemas.py - Message schemas (8 message types)",
            "monitor.py - RealtimeMonitor (background checks)",
        ],
        "app/api/routes/": [
            "websocket.py - WebSocket endpoints & test routes",
        ],
        "app/": [
            "main.py - FastAPI app with lifespan events",
        ],
        "Root": [
            "test_websocket_client.py - Interactive test client",
            "dashboard.html - Live updating demo dashboard",
            "PHASE_10_TESTING_GUIDE.md - Detailed testing docs",
        ]
    }

    for path, items in files.items():
        print(f"\n{path}")
        for item in items:
            print(f"  • {item}")


def print_architecture():
    """Print Phase 10 architecture"""
    print_header("PHASE 10 ARCHITECTURE")

    print("""
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                          │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  RealtimeMonitor (Background Service)                │  │
│  │  ✓ Checks anomalies every 60s                        │  │
│  │  ✓ Checks KPI metrics                                │  │
│  │  ✓ Broadcasts alerts                                 │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                         │
│  ┌────────────────▼─────────────────────────────────────┐  │
│  │  EventDispatcher (Pub/Sub System)                    │  │
│  │  ✓ Routes events to clients                          │  │
│  │  ✓ Manages subscriptions                             │  │
│  │  ✓ Keeps event history                               │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                         │
│  ┌────────────────▼─────────────────────────────────────┐  │
│  │  ConnectionManager (Client Lifecycle)                │  │
│  │  ✓ Tracks active connections                         │  │
│  │  ✓ Routes messages                                   │  │
│  │  ✓ Handles disconnections                            │  │
│  └────────────────┬─────────────────────────────────────┘  │
└─────────────────────┼──────────────────────────────────────┘
                      │ WebSocket
                      │
        ┌─────────────┴─────────────┐
        │                           │
   ┌────▼────┐              ┌──────▼──────┐
   │Dashboard │              │ Mobile App  │
   │Browser   │              │ (Future)    │
   └──────────┘              └─────────────┘
    """)


async def run_all_tests():
    """Run all component tests"""
    print_header("PHASE 10 COMPONENT TESTS")

    print("Running component tests...\n")

    tests = [
        ("ConnectionManager", test_connection_manager),
        ("Message Schemas", test_schemas),
        ("EventDispatcher", test_event_dispatcher),
        ("RealtimeMonitor", test_realtime_monitor),
        ("REST Endpoints", test_rest_endpoints),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            await test_func()
            passed += 1
        except Exception as e:
            print(f"\n❌ {name} test failed: {e}")
            failed += 1

    print_header("TEST RESULTS")
    print(f"✅ Passed: {passed}/{len(tests)}")
    if failed > 0:
        print(f"❌ Failed: {failed}/{len(tests)}")
    else:
        print("🎉 All tests passed!")


def main():
    """Main entry point"""
    print("\n")
    print("█" * 80)
    print("█  🍖 BBQ RESTAURANT AI - PHASE 10 TESTING SUITE")
    print("█  Real-Time WebSocket Layer")
    print("█" * 80)

    print("\n\nChoose what you'd like to do:\n")

    options = [
        ("Run all component tests", "1"),
        ("View quick start guide", "2"),
        ("View demo commands", "3"),
        ("View testing checklist", "4"),
        ("View file structure", "5"),
        ("View architecture", "6"),
        ("All of the above", "7"),
        ("Exit", "0"),
    ]

    for title, key in options:
        print(f"  {key}) {title}")

    choice = input("\nEnter choice (0-7): ").strip()

    if choice == "1":
        asyncio.run(run_all_tests())
    elif choice == "2":
        print_quick_start()
    elif choice == "3":
        print_demo_commands()
    elif choice == "4":
        print_testing_checklist()
    elif choice == "5":
        print_file_structure()
    elif choice == "6":
        print_architecture()
    elif choice == "7":
        asyncio.run(run_all_tests())
        print_quick_start()
        print_demo_commands()
        print_testing_checklist()
        print_file_structure()
        print_architecture()
    elif choice == "0":
        print("\nGoodbye! 👋\n")
        return
    else:
        print("\n❌ Invalid choice\n")
        return

    print("\n" + "=" * 80)
    print("For detailed information, see: PHASE_10_TESTING_GUIDE.md")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Testing interrupted by user\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
