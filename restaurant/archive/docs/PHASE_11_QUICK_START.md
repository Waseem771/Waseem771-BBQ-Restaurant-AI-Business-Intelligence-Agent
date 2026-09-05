# 🚀 Phase 11: Quick Start & Integration Checklist

**BBQ Restaurant AI Business Intelligence Agent**  
**Phase 11 — Model Versioning & Rollback**  
**Quick Reference Guide**

---

## ⚡ 5-Minute Quick Start

### What is Phase 11?

Before Phase 11: Deploy new model → breaks → manually recover  
After Phase 11: Deploy new model → monitor → rollback instantly if needed

### The 3 Key Ideas

| Idea | Meaning | Why It Matters |
|------|---------|----------------|
| **Model Versioning** | Keep all model versions (v1, v2, v3...) | You can always go back |
| **Active Model** | Only one version is "live" at a time | Predictable, trackable |
| **Rollback** | Instantly switch to previous version | Crisis recovery in seconds |

### Files You Need to Know

| File | Purpose | Key Methods |
|------|---------|-------------|
| `app/ml/models.py` | Database tables | ModelVersion, ModelAuditLog |
| `app/ml/registry.py` | Core logic | register, activate, rollback |
| `app/ml/loader.py` | Load models | load_model(), get_model_loader() |
| `app/api/routes/models.py` | REST API | 8 endpoints |
| `tests/test_model_registry.py` | Tests | 20+ test cases |

### Quick Commands

```bash
# Register new model version
curl -X POST http://localhost:8001/api/v1/models/sales_forecast/register \
  -H "Content-Type: application/json" \
  -d '{"version":"v2","algorithm":"XGBoost","metrics":{"MAE":12800},...}'

# Activate it
curl -X POST http://localhost:8001/api/v1/models/sales_forecast/v2/activate \
  -d '{"reason":"Better metrics"}'

# Emergency rollback
curl -X POST http://localhost:8001/api/v1/models/sales_forecast/rollback \
  -d '{"target_version":"v1","reason":"v2 broken"}'

# Check what's active
curl http://localhost:8001/api/v1/models/sales_forecast/active

# View all history
curl http://localhost:8001/api/v1/models/sales_forecast/history
```

---

## 📋 Integration Checklist

### Prerequisites (Before Phase 11)
- ✅ Phase 8 (Sales Forecasting) Complete
- ✅ Phase 9 (Anomaly Detection) Complete
- ✅ Phase 10 (Real-Time WebSocket) Complete
- ✅ FastAPI backend running
- ✅ PostgreSQL database configured

### Step 1: Add Phase 11 Code to Your Project

**Copy these files to your project:**

```
✅ app/ml/models.py              → Database schema
✅ app/ml/registry.py            → Core registry logic
✅ app/ml/loader.py              → Model loader
✅ app/api/routes/models.py      → API endpoints
✅ tests/test_model_registry.py  → Tests
```

**Verify file structure:**
```
app/
├── ml/
│   ├── models.py           ← NEW
│   ├── registry.py         ← NEW
│   ├── loader.py           ← NEW
│   ├── forecasting/        ← EXISTING
│   └── ...
├── api/
│   ├── routes/
│   │   ├── models.py       ← NEW
│   │   ├── websocket.py    ← EXISTING
│   │   └── ...
│   └── ...
└── ...
```

### Step 2: Update Database

```python
# In app/core/database.py or your DB init script
from app.ml.models import Base

# Create tables when app starts
def init_db(engine):
    Base.metadata.create_all(engine)

# This creates:
# - model_versions table
# - model_audit_logs table
```

### Step 3: Add Imports to Main FastAPI App

```python
# app/main.py
from fastapi import FastAPI
from app.api.routes import models  # NEW
from app.core.database import init_db

app = FastAPI(title="BBQ Restaurant AI BI")

# Initialize database
init_db(engine)

# Include routers
app.include_router(models.router)  # NEW

# ... rest of your app setup
```

### Step 4: Update Forecasting Service

**File: `app/ml/forecasting/service.py`**

```python
# BEFORE (Phase 8)
import joblib

def get_forecast(...):
    # Loads model directly
    model = joblib.load("/models/sales_forecast/model.pkl")
    return model.predict(...)

# AFTER (Phase 11)
from app.ml.loader import get_model_loader

def get_forecast(...):
    # Loads via registry
    loader = get_model_loader()
    model = loader.load_model("sales_forecast")
    return model.predict(...)
```

### Step 5: Update Anomaly Detection Service

**File: `app/websocket/monitor.py`**

```python
# BEFORE (Phase 9)
import joblib

class RealtimeMonitor:
    def __init__(self):
        self.model = joblib.load("/models/anomaly_detector/model.pkl")

# AFTER (Phase 11)
from app.ml.loader import get_model_loader

class RealtimeMonitor:
    def __init__(self):
        self.loader = get_model_loader()
        self.model = self.loader.load_model("anomaly_detector")
```

### Step 6: Add Model Version to Dashboard

**File: `dashboard.html`** (or Streamlit app)

```html
<!-- Add to dashboard -->
<div class="model-status">
  <h3>🤖 Active Models</h3>
  <div id="model-info">Loading...</div>
</div>

<script>
async function loadModelInfo() {
  try {
    const response = await fetch('/api/v1/models');
    const data = await response.json();
    
    const html = data.models.map(m => `
      <p>
        <strong>${m.model_name}:</strong> 
        ${m.active_version} (${m.algorithm})
      </p>
    `).join('');
    
    document.getElementById('model-info').innerHTML = html;
  } catch (e) {
    console.error('Error loading models:', e);
  }
}

loadModelInfo();
setInterval(loadModelInfo, 30000);  // Refresh every 30 seconds
</script>
```

### Step 7: Run Database Migrations

```bash
# If using Alembic for migrations
alembic revision --autogenerate -m "Add model versioning tables"
alembic upgrade head

# Or manually:
# The tables are created automatically when Base.metadata.create_all(engine) runs
```

### Step 8: Run Tests

```bash
# Install pytest if not already installed
pip install pytest pytest-cov

# Run all model registry tests
pytest tests/test_model_registry.py -v

# Expected output:
# test_register_model_successfully PASSED
# test_activate_model PASSED
# test_rollback_to_previous_version PASSED
# ... (20+ tests total)
# ====== 20 passed in 2.34s ======
```

### Step 9: Verify Integration

```bash
# Start your app
uvicorn app.main:app --port 8001 --reload

# In another terminal, test the API
curl http://localhost:8001/api/v1/models
# Should return: {"models": [], "total": 0}

# Check database tables exist
# Connect to your PostgreSQL database
psql -U postgres -d your_db
\dt
# Should show: model_versions, model_audit_logs
```

### Step 10: Document Your Models

```bash
# Create a models directory structure
mkdir -p models/sales_forecast/v1
mkdir -p models/anomaly_detector/v1

# Save your existing trained models there
cp path/to/your/sales_forecast/model.pkl models/sales_forecast/v1/

# Register them via API
curl -X POST http://localhost:8001/api/v1/models/sales_forecast/register \
  -H "Content-Type: application/json" \
  -d '{
    "version": "v1",
    "algorithm": "XGBoost",
    "metrics": {"MAE": 14200, "RMSE": 18500},
    "file_path": "/models/sales_forecast/v1/model.pkl",
    "training_date": "2026-08-15T09:00:00",
    "training_dataset": "Q3_2026",
    "notes": "Initial production model"
  }'

# Activate it
curl -X POST http://localhost:8001/api/v1/models/sales_forecast/v1/activate \
  -d '{"reason": "Initial production deployment"}'
```

---

## 🔍 Verification Tests

### Test 1: Model Registration

```bash
curl -X POST http://localhost:8001/api/v1/models/test_model/register \
  -H "Content-Type: application/json" \
  -d '{
    "version": "v1",
    "algorithm": "TestAlgo",
    "metrics": {"accuracy": 0.95},
    "file_path": "/tmp/test_model.pkl",
    "training_date": "2026-08-31T10:00:00",
    "training_dataset": "test_data"
  }'

# Expected response:
# {"success": true, "message": "Registered test_model version v1", ...}
```

### Test 2: Model Activation

```bash
curl -X POST http://localhost:8001/api/v1/models/test_model/v1/activate \
  -H "Content-Type: application/json" \
  -d '{"reason": "test activation"}'

# Expected response:
# {"success": true, "message": "Activated test_model version v1", ...}
```

### Test 3: Get Active Model

```bash
curl http://localhost:8001/api/v1/models/test_model/active

# Expected response:
# {"model_name": "test_model", "version": "v1", "status": "active", ...}
```

### Test 4: Rollback

```bash
# First, activate v2
curl -X POST http://localhost:8001/api/v1/models/test_model/register \
  -H "Content-Type: application/json" \
  -d '{"version": "v2", ...}'

curl -X POST http://localhost:8001/api/v1/models/test_model/v2/activate

# Then rollback to v1
curl -X POST http://localhost:8001/api/v1/models/test_model/rollback \
  -H "Content-Type: application/json" \
  -d '{"target_version": "v1", "reason": "test rollback"}'

# Expected: v1 becomes active again
```

### Test 5: History

```bash
curl http://localhost:8001/api/v1/models/test_model/history

# Should show all versions and audit trail
```

---

## 🐛 Troubleshooting

### Issue: "ModelVersion table doesn't exist"

**Solution:**
```python
# Make sure Base.metadata.create_all(engine) is called on startup
# Add to app/main.py:

from app.core.database import engine
from app.ml.models import Base

Base.metadata.create_all(engine)
```

### Issue: "No active model found"

**Solution:**
```bash
# Register and activate a model first
curl -X POST http://localhost:8001/api/v1/models/your_model/register ...
curl -X POST http://localhost:8001/api/v1/models/your_model/v1/activate ...
```

### Issue: "Model file not found"

**Solution:**
```bash
# Make sure the file_path exists
ls -la /models/sales_forecast/v1/model.pkl

# If not, copy your model there
cp your_model.pkl /models/sales_forecast/v1/model.pkl
```

### Issue: Tests fail with "database locked"

**Solution:**
```bash
# Use sqlite in-memory for tests (already configured in test fixtures)
# Or clean up any existing test databases:
rm -f test.db
pytest tests/test_model_registry.py -v
```

---

## 📊 Phase 11 Completion Checklist

### Code Implementation
- [ ] `app/ml/models.py` created
- [ ] `app/ml/registry.py` created
- [ ] `app/ml/loader.py` created
- [ ] `app/api/routes/models.py` created
- [ ] `tests/test_model_registry.py` created

### Database Setup
- [ ] model_versions table created
- [ ] model_audit_logs table created
- [ ] Indexes created for performance

### Integration
- [ ] FastAPI app imports models router
- [ ] Forecasting service uses ModelLoader
- [ ] Anomaly detection service uses ModelLoader
- [ ] Dashboard shows active model versions

### Testing
- [ ] All tests pass (pytest)
- [ ] Manual API tests pass (curl)
- [ ] Model registration works
- [ ] Model activation works
- [ ] Model rollback works

### Documentation
- [ ] PHASE_11_LEARNING_GUIDE.md read
- [ ] PHASE_11_IMPLEMENTATION_GUIDE.md read
- [ ] PHASE_11_QUICK_START.md read (this file)
- [ ] API endpoints documented
- [ ] Workflows documented

### Production Readiness
- [ ] Error handling verified
- [ ] Audit logging working
- [ ] Cache clearing works
- [ ] Database transactions atomic
- [ ] No hard-coded paths

---

## 📈 Success Indicators

### Phase 11 is Complete When:

✅ **Registration Works**
- Can register new model versions via API
- Models stored in database
- Metrics recorded correctly

✅ **Activation Works**
- Can activate a model version
- Previous version archived automatically
- Status changes recorded

✅ **Loading Works**
- Forecasting service loads model from registry
- Anomaly detection loads model from registry
- Models cached for performance

✅ **Rollback Works**
- Can instantly rollback to previous version
- Previous version reactivated
- Reason recorded in audit trail

✅ **Visibility**
- Can view model history
- Can see audit trail
- Can compare versions
- Dashboard shows active versions

✅ **Tests Pass**
- 20+ unit tests pass
- Integration tests pass
- Manual tests pass

---

## 🎓 What You've Learned

### Concepts
- Model versioning patterns
- State machine design
- Audit logging
- Rollback mechanisms
- Caching strategies

### Implementation
- Database schema design
- ORM with SQLAlchemy
- Service layer architecture
- REST API design
- Error handling

### Production Practices
- Safe deployment patterns
- Audit trails for compliance
- Graceful error recovery
- Performance optimization
- Testing strategies

---

## 🚀 Next Phase: Phase 12

**Docker & Production Deployment**

After Phase 11, you're ready for:
- Containerizing your app
- Docker Compose orchestration
- Environment configuration
- Production monitoring
- CI/CD pipelines

---

## 📞 Quick Reference

### Database Tables

```sql
-- Model versions table
SELECT * FROM model_versions 
WHERE model_name = 'sales_forecast' 
ORDER BY created_at DESC;

-- Audit trail
SELECT * FROM model_audit_logs 
WHERE model_name = 'sales_forecast' 
ORDER BY performed_at DESC;
```

### Common API Calls

```bash
# List all models
curl http://localhost:8001/api/v1/models

# Get model info
curl http://localhost:8001/api/v1/models/sales_forecast

# Get active version
curl http://localhost:8001/api/v1/models/sales_forecast/active

# Get history
curl http://localhost:8001/api/v1/models/sales_forecast/history

# Compare versions
curl http://localhost:8001/api/v1/models/sales_forecast/v1/compare/v2

# Health check
curl http://localhost:8001/api/v1/models/health/models
```

---

## 🎉 Phase 11: Complete!

You now have:
- ✅ Complete model versioning system
- ✅ Safe rollback mechanism
- ✅ Full audit trail
- ✅ REST API for model management
- ✅ Integration with existing services
- ✅ Comprehensive tests
- ✅ Production-ready code

**Ready for Phase 12: Docker & Production Deployment! 🚀**

---

*Phase 11: Model Versioning & Rollback — Complete*  
*Date: 2026-08-31*  
*Status: ✅ PRODUCTION READY*  
*Next: Phase 12 — Docker & Production Deployment*
