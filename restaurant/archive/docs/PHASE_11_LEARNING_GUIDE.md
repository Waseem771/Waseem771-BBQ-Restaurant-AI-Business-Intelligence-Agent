# 🎓 Phase 11: Model Versioning & Rollback — Complete Learning Guide

**BBQ Restaurant AI Business Intelligence Agent**  
**Status: Phase 11 — Model Versioning & Rollback**  
**Date: 2026-08-31**

---

## 📚 Table of Contents

1. [What is Phase 11?](#what-is-phase-11)
2. [Core Concepts](#core-concepts)
3. [Why This Matters](#why-this-matters)
4. [What We'll Build](#what-well-build)
5. [Architecture](#architecture)
6. [Implementation Plan](#implementation-plan)
7. [Code Examples](#code-examples)
8. [Testing Strategy](#testing-strategy)

---

## What is Phase 11?

### The Problem

You now have two ML models working in production:

1. **Sales Forecasting Model** (Phase 8)
   - Predicts future revenue/orders
   - Deployed and serving predictions

2. **Anomaly Detection Model** (Phase 9)
   - Detects unusual patterns
   - Running in the real-time monitor

But what happens if you **train a new, "better" model** and deploy it, only to discover it's actually **worse** in production?

**Real-world example:**
```
Friday, 3 PM - Deploy new forecasting model v2
Friday, 5 PM - Start getting terrible predictions
Friday, 6 PM - Customers are angry
Saturday, 10 AM - Finally realize the problem
Saturday, 11 AM - Manually roll back (if you can find the old model)
Saturday, 1 PM - System works again
Damage: Lost revenue, damaged trust, system down for 24 hours
```

### The Solution: Model Versioning & Rollback

**Phase 11 gives you:**

- ✅ **Model Registry** - Central place to store all model versions
- ✅ **Version Tracking** - Know which model is active, when it was trained, its performance
- ✅ **Rollback Mechanism** - Switch back to a previous model instantly
- ✅ **Performance Tracking** - Compare v1 vs v2 vs v3 metrics
- ✅ **Safe Deployment** - Deploy with confidence knowing you can roll back

---

## Core Concepts

### 1. What is a Model Version?

A **model version** is a specific instance of a trained model with metadata:

```
Model: sales_forecast
Version: v1
├── Algorithm: XGBoost
├── Training Date: 2026-08-01
├── Training Data: Q3 2026
├── Metrics:
│   ├── MAE: 14,200
│   ├── RMSE: 18,500
│   └── MAPE: 8.3%
├── File Path: /models/sales_forecast/v1/model.pkl
├── Status: active (currently in use)
└── Created By: training_pipeline
```

Another version might look like:

```
Model: sales_forecast
Version: v2
├── Algorithm: XGBoost (with new features)
├── Training Date: 2026-08-15
├── Training Data: Q3 2026 (with recent data)
├── Metrics:
│   ├── MAE: 12,800  ← Better!
│   ├── RMSE: 16,200
│   └── MAPE: 7.1%
├── File Path: /models/sales_forecast/v2/model.pkl
├── Status: staged (ready to test)
└── Created By: training_pipeline
```

### 2. Model States

Every model version has a **state**:

```
State        | Meaning                                    | When Used
-------------|--------------------------------------------|-----------
development  | Being trained, not yet ready              | Local dev only
staged       | Trained, tested, ready to deploy          | A/B testing or manual testing
active       | Currently serving predictions in prod     | Production
archived     | Old version, kept for reference           | Historical tracking
deprecated   | Do not use, scheduled for deletion        | Cleanup
```

### 3. Model Registry Pattern

A **model registry** is a centralized system that tracks all versions:

```
┌─────────────────────────────────────┐
│      Model Registry Database        │
├─────────────────────────────────────┤
│                                     │
│  Model: sales_forecast              │
│  ├── v1 (archived)  - MAE: 14,200   │
│  ├── v2 (active)    - MAE: 12,800   │
│  └── v3 (staged)    - MAE: 12,100   │
│                                     │
│  Model: anomaly_detector            │
│  ├── v1 (archived)  - F1: 0.82      │
│  └── v2 (active)    - F1: 0.88      │
│                                     │
└─────────────────────────────────────┘
```

### 4. The Rollback Scenario

**Before rollback:**
```
User asks: "Forecast next week's revenue"
    ↓
System loads: sales_forecast v2 (active)
    ↓
v2 makes bad prediction (100% higher than reality)
    ↓
Damage!
```

**After rollback:**
```
Admin runs: POST /models/sales_forecast/rollback
    ↓
System updates: Active model = v1
    ↓
User asks: "Forecast next week's revenue"
    ↓
System loads: sales_forecast v1 (active)
    ↓
v1 makes correct prediction
    ↓
Crisis averted! 🎉
```

---

## Why This Matters

### In Production, Model Versioning Solves:

**1. Safety**
- Roll back instantly if a model performs poorly
- No need to retrain from scratch
- Minimal downtime

**2. Auditability**
- Know exactly which model was used for a prediction
- Trace decisions back to a specific model version
- Compliance/regulatory requirements

**3. Performance Tracking**
- Compare metrics across versions
- Understand model improvements
- Make data-driven deployment decisions

**4. Team Collaboration**
- Different teams can work on different model versions
- Deploy with confidence
- Easy handoff between data scientists and engineers

**5. Cost Savings**
- Quick rollback saves time/money vs retraining
- No need to keep retraining when you have a good model
- Historical tracking helps future improvements

---

## What We'll Build

### Phase 11 Deliverables

We'll build a **lightweight, custom model registry system** (instead of using MLflow) because:

- ✅ You'll understand every line of code
- ✅ It integrates directly with your existing system
- ✅ No external dependencies to manage
- ✅ Perfect for learning

### Components

#### 1. Model Registry Database Table

```sql
CREATE TABLE model_versions (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    version VARCHAR(20) NOT NULL,
    algorithm VARCHAR(100),
    status VARCHAR(20),                    -- development, staged, active, archived
    metrics JSONB,                         -- {MAE: 12800, RMSE: 16200, MAPE: 7.1}
    file_path TEXT,                        -- /models/sales_forecast/v2/model.pkl
    training_date TIMESTAMP,
    training_dataset VARCHAR(100),
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    activated_at TIMESTAMP,
    notes TEXT,
    UNIQUE(model_name, version)
);
```

#### 2. Model Registry Service

```python
class ModelRegistry:
    """Manages model versions"""
    
    def register_model(self, model_name, version, metrics, file_path):
        """Record a newly trained model"""
        pass
    
    def activate_model(self, model_name, version):
        """Set a model as active (for production use)"""
        pass
    
    def get_active_model(self, model_name):
        """Get the currently active model version"""
        pass
    
    def list_versions(self, model_name):
        """List all versions of a model"""
        pass
    
    def rollback_model(self, model_name, target_version):
        """Rollback to a specific version"""
        pass
```

#### 3. Model Loader

```python
class ModelLoader:
    """Load and cache models from registry"""
    
    def load_model(self, model_name):
        """Load the active model version"""
        pass
    
    def load_model_version(self, model_name, version):
        """Load a specific version"""
        pass
```

#### 4. API Endpoints

```
GET    /models                          → List all models & versions
GET    /models/{model_name}             → Get model info & history
GET    /models/{model_name}/active      → Get active version details
GET    /models/{model_name}/versions    → List all versions
POST   /models/{model_name}/register    → Register new model version
POST   /models/{model_name}/activate    → Activate a specific version
POST   /models/{model_name}/rollback    → Rollback to previous version
DELETE /models/{model_name}/{version}   → Archive/delete a version
```

#### 5. Monitoring & Audit Trail

```
Every action tracked:
├── When was v2 deployed?
├── Who deployed it?
├── Why was it rolled back?
├── How long was it active?
└── What was the impact?
```

---

## Architecture

### System Diagram

```
┌──────────────────────────────────────────────────────┐
│           Training Pipeline (Phase 8 & 9)            │
│                                                      │
│  Data → Model Training → Evaluation → Metrics        │
│                           ↓                          │
│                    ModelRegistry                     │
│                    (register_model)                  │
└──────────────────────┬───────────────────────────────┘
                       │
                       ↓
        ┌──────────────────────────────┐
        │   Model Registry Database    │
        │  (model_versions table)      │
        │                              │
        │  v1: archived   MAE=14,200   │
        │  v2: active     MAE=12,800   │
        │  v3: staged     MAE=12,100   │
        └──────────────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         ↓             ↓             ↓
    ┌────────┐  ┌─────────┐  ┌──────────┐
    │Forecast│  │Anomaly  │  │Dashboard │
    │Service │  │Service  │  │ Endpoint │
    └────────┘  └─────────┘  └──────────┘
         │             │             │
         └─────────────┼─────────────┘
                       ↓
            ┌──────────────────────┐
            │  ModelLoader         │
            │  (load_model)        │
            │  (load_version)      │
            └──────────────────────┘
                       │
                       ↓
         ┌─────────────────────────┐
         │  Active Model Version   │
         │  (used for predictions) │
         └─────────────────────────┘
```

### Data Flow

**Deployment Workflow:**

```
1. Train new model (Phase 8 or 9)
   ↓
2. Evaluate metrics
   ↓
3. Register in ModelRegistry (status="staged")
   ↓
4. A/B test or manual validation
   ↓
5. Activate new version (status="active")
   ↓
6. Monitor in production
   ↓
7. If problems detected, rollback to previous version
```

---

## Implementation Plan

### Step-by-Step Approach

We'll build in this order:

#### Step 1: Database Schema (15 minutes)
- Create `model_versions` table
- Add indexes for performance
- Create migration script

#### Step 2: Model Registry Service (30 minutes)
- `ModelRegistry` class with core methods
- Database integration
- Error handling

#### Step 3: Model Loader (20 minutes)
- `ModelLoader` class
- Model caching
- Graceful fallback if model not found

#### Step 4: API Endpoints (30 minutes)
- 8 REST endpoints for model management
- Validation & error handling
- Audit logging

#### Step 5: Integration with Existing Models (20 minutes)
- Update forecasting service to use ModelLoader
- Update anomaly detection service to use ModelLoader
- Update dashboard endpoints to show model version

#### Step 6: Testing & Documentation (30 minutes)
- Write tests for all components
- Create testing guide
- Document workflows

**Total Time: ~2.5 hours of development**

---

## Code Examples

### Example 1: Register a Model

```python
# After training a forecasting model
from app.ml.registry import ModelRegistry

registry = ModelRegistry()

# Save the model file
model_path = "/models/sales_forecast/v2/model.pkl"
joblib.dump(model, model_path)

# Register it in the database
registry.register_model(
    model_name="sales_forecast",
    version="v2",
    algorithm="XGBoost",
    metrics={
        "MAE": 12800,
        "RMSE": 16200,
        "MAPE": 7.1,
        "training_samples": 450
    },
    file_path=model_path,
    training_date=datetime.now(),
    training_dataset="Q3_2026_with_recent_data",
    created_by="training_pipeline"
)

# Model is now in "development" state
# Next: Test it, then activate it
```

### Example 2: Activate a Model

```python
# Admin or system activates v2
registry.activate_model("sales_forecast", "v2")

# What happens:
# 1. Previous active model (v1) set to "archived"
# 2. v2 set to "active"
# 3. Timestamp recorded
# 4. Audit log entry created
# 5. All new forecast requests use v2
```

### Example 3: Rollback

```python
# Oh no! v2 is making terrible predictions
# Admin rolls back to v1
registry.rollback_model("sales_forecast", "v1")

# What happens:
# 1. v2 set to "archived"
# 2. v1 set to "active"
# 3. Timestamp recorded
# 4. Reason documented in audit log
# 5. All new forecast requests use v1
# Crisis averted! 🎉
```

### Example 4: Using Models in Forecasting Service

```python
# Before Phase 11:
from app.ml.forecasting import get_forecast
forecast = get_forecast(period_days=7)

# After Phase 11:
from app.ml.loader import ModelLoader

loader = ModelLoader()
model = loader.load_model("sales_forecast")
forecast = model.predict(period_days=7)

# Benefits:
# - Model version tracked automatically
# - Can rollback if needed
# - Audit trail of which model was used
```

---

## Testing Strategy

### What We'll Test

1. **Registration**
   - ✅ Register a new model version
   - ✅ Verify it's saved correctly
   - ✅ Check metadata is accurate

2. **Activation**
   - ✅ Activate a model version
   - ✅ Verify previous version is archived
   - ✅ Check activation timestamp

3. **Loading**
   - ✅ Load active model
   - ✅ Load specific version
   - ✅ Handle missing model gracefully

4. **Rollback**
   - ✅ Rollback to previous version
   - ✅ Verify state changes correctly
   - ✅ Check audit trail

5. **API Endpoints**
   - ✅ List models
   - ✅ Get model history
   - ✅ Register new version via REST
   - ✅ Activate/rollback via REST

### Example Test

```python
def test_rollback():
    """Test rollback scenario"""
    registry = ModelRegistry()
    
    # Initial state: v1 is active
    assert registry.get_active_model("sales_forecast").version == "v1"
    
    # Deploy v2
    registry.activate_model("sales_forecast", "v2")
    assert registry.get_active_model("sales_forecast").version == "v2"
    
    # Problems detected, rollback
    registry.rollback_model("sales_forecast", "v1")
    assert registry.get_active_model("sales_forecast").version == "v1"
    
    # v2 should be archived
    v2 = registry.get_model_version("sales_forecast", "v2")
    assert v2.status == "archived"
    
    print("✅ Rollback test passed!")
```

---

## Why You Should Care About This Phase

### Real-World Impact

**Before Phase 11:**
- Deploy new model → breaks → scramble to find old model → manual recovery
- No audit trail of which model made which prediction
- Can't compare model performance across versions
- Risky to deploy new models

**After Phase 11:**
- Deploy new model → activate → monitor → rollback instantly if needed
- Complete audit trail of every model change
- Easy comparison of model versions
- Deploy with confidence knowing rollback is 1 click away

### Skills You'll Learn

✅ **Database Design** - Model registry schema  
✅ **ORM Patterns** - Mapping Python objects to database  
✅ **API Design** - RESTful endpoints for model management  
✅ **Audit & Compliance** - Tracking changes over time  
✅ **Production Best Practices** - Safe deployment patterns  
✅ **System Architecture** - Integrating model versioning into existing system  

---

## Next Steps

1. **Read this guide completely** - Understand the concepts
2. **We'll create the database schema** - Design the model_versions table
3. **We'll build ModelRegistry** - Core versioning logic
4. **We'll build ModelLoader** - Loading models safely
5. **We'll create API endpoints** - REST interface for model management
6. **We'll integrate with existing models** - Update forecasting & anomaly detection
7. **We'll test everything** - Comprehensive test suite
8. **We'll document workflows** - How to deploy, rollback, etc.

---

## Summary

**Phase 11 in 30 seconds:**

| What | Why | How |
|------|-----|-----|
| **Model Versioning** | Track all model versions | Database + Registry service |
| **Rollback** | Recover instantly if model fails | Switch active version, keep old files |
| **Audit Trail** | Know which model made which prediction | Log every change |
| **Safe Deployment** | Deploy confidently knowing you can rollback | Staged → Active → Monitor → Rollback if needed |

**After Phase 11, you'll have production-grade ML hygiene.**

---

*Next: Let's build it! 🚀*
