"""
Test suite for Phase 11 - Model Versioning & Rollback.

Tests cover:
- Model registration
- Model activation
- Model rollback
- History tracking
- List models
"""

import pytest
from datetime import datetime
import tempfile
import os
import json
from app.ml.registry import ModelRegistry
from app.ml.models import MODEL_STATUS_ACTIVE, MODEL_STATUS_ARCHIVED, MODEL_STATUS_DEVELOPMENT
from app import db


@pytest.fixture(autouse=True)
def setup_and_cleanup_db():
    """Setup and cleanup database for each test."""
    # Before each test: clean up and ensure tables exist
    try:
        conn = db.get_connection(readonly=False)
        cursor = conn.cursor()
        # Clean first
        cursor.execute("DELETE FROM model_versions")
        cursor.execute("DELETE FROM model_audit_logs")
        conn.commit()
        # Then create if not exists
        from app.ml.models import SCHEMA_MODEL_VERSIONS, SCHEMA_MODEL_AUDIT_LOG
        cursor.execute(SCHEMA_MODEL_VERSIONS)
        cursor.execute(SCHEMA_MODEL_AUDIT_LOG)
        conn.commit()
        conn.close()
    except Exception as e:
        # Tables might not exist yet, that's okay
        try:
            conn = db.get_connection(readonly=False)
            cursor = conn.cursor()
            from app.ml.models import SCHEMA_MODEL_VERSIONS, SCHEMA_MODEL_AUDIT_LOG
            cursor.execute(SCHEMA_MODEL_VERSIONS)
            cursor.execute(SCHEMA_MODEL_AUDIT_LOG)
            conn.commit()
            conn.close()
        except Exception as e2:
            print(f"Setup error: {e2}")

    yield

    # After each test: clean up test data
    try:
        conn = db.get_connection(readonly=False)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM model_versions")
        cursor.execute("DELETE FROM model_audit_logs")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Cleanup error: {e}")


class TestModelRegistry:
    """Test ModelRegistry functionality."""

    def test_register_model_success(self):
        """Test successful model registration."""
        result = ModelRegistry.register_model(
            model_name="sales_forecast",
            version="v1",
            algorithm="XGBoost",
            metrics={"MAE": 14200, "RMSE": 16800},
            file_path="/models/sales_forecast/v1/model.pkl",
            training_date="2026-08-31T08:00:00",
            training_dataset="Q3_2026"
        )
        assert result["success"] is True
        assert "v1" in result["message"]

    def test_register_model_duplicate_fails(self):
        """Test that duplicate registration fails."""
        ModelRegistry.register_model(
            model_name="sales_forecast",
            version="v1",
            algorithm="XGBoost",
            metrics={"MAE": 14200},
            file_path="/models/sales_forecast/v1/model.pkl",
            training_date="2026-08-31T08:00:00",
            training_dataset="Q3_2026"
        )

        with pytest.raises(Exception):
            ModelRegistry.register_model(
                model_name="sales_forecast",
                version="v1",
                algorithm="XGBoost",
                metrics={"MAE": 14200},
                file_path="/models/sales_forecast/v1/model.pkl",
                training_date="2026-08-31T08:00:00",
                training_dataset="Q3_2026"
            )

    def test_activate_model_success(self):
        """Test successful model activation."""
        ModelRegistry.register_model(
            model_name="anomaly_detector",
            version="v1",
            algorithm="IsolationForest",
            metrics={"Precision": 0.92},
            file_path="/models/anomaly_detector/v1/model.pkl",
            training_date="2026-08-31T08:00:00",
            training_dataset="Q3_2026"
        )

        result = ModelRegistry.activate_model(
            model_name="anomaly_detector",
            version="v1",
            reason="Initial deployment"
        )
        assert result["success"] is True

    def test_get_active_model(self):
        """Test retrieving active model."""
        ModelRegistry.register_model(
            model_name="test_model",
            version="v1",
            algorithm="XGBoost",
            metrics={"MAE": 100},
            file_path="/models/test_model/v1/model.pkl",
            training_date="2026-08-31T08:00:00",
            training_dataset="test"
        )

        ModelRegistry.activate_model(
            model_name="test_model",
            version="v1"
        )

        active = ModelRegistry.get_active_model("test_model")
        assert active is not None
        assert active["version"] == "v1"
        assert active["status"] == MODEL_STATUS_ACTIVE

    def test_rollback_to_previous_version(self):
        """Test rollback functionality."""
        # Register v1
        ModelRegistry.register_model(
            model_name="rollback_test",
            version="v1",
            algorithm="XGBoost",
            metrics={"MAE": 14200},
            file_path="/models/rollback_test/v1/model.pkl",
            training_date="2026-08-31T08:00:00",
            training_dataset="Q3_2026"
        )

        # Activate v1
        ModelRegistry.activate_model("rollback_test", "v1")

        # Register v2
        ModelRegistry.register_model(
            model_name="rollback_test",
            version="v2",
            algorithm="XGBoost",
            metrics={"MAE": 12800},
            file_path="/models/rollback_test/v2/model.pkl",
            training_date="2026-08-31T09:00:00",
            training_dataset="Q3_2026"
        )

        # Activate v2
        ModelRegistry.activate_model("rollback_test", "v2")

        # Verify v2 is active
        active = ModelRegistry.get_active_model("rollback_test")
        assert active["version"] == "v2"

        # Rollback to v1
        result = ModelRegistry.rollback_model(
            model_name="rollback_test",
            target_version="v1",
            reason="v2 has production bug"
        )
        assert result["success"] is True

        # Verify v1 is active again
        active = ModelRegistry.get_active_model("rollback_test")
        assert active["version"] == "v1"

    def test_get_model_history(self):
        """Test retrieving model history."""
        model_name = "history_test"

        # Register multiple versions
        for i in range(1, 4):
            ModelRegistry.register_model(
                model_name=model_name,
                version=f"v{i}",
                algorithm="XGBoost",
                metrics={"MAE": 14200 - (i * 1000)},
                file_path=f"/models/{model_name}/v{i}/model.pkl",
                training_date="2026-08-31T08:00:00",
                training_dataset="Q3_2026"
            )

        history = ModelRegistry.get_model_history(model_name)
        assert len(history) >= 3
        assert all(v["model_name"] == model_name for v in history)

    def test_list_models(self):
        """Test listing all models."""
        models = ModelRegistry.list_models()
        assert isinstance(models, list)
        assert all("model_name" in m for m in models)

    def test_metrics_stored_as_json(self):
        """Test that metrics are properly stored and retrieved."""
        metrics = {"MAE": 14200, "RMSE": 16800, "MAPE": 0.15}
        ModelRegistry.register_model(
            model_name="metrics_test",
            version="v1",
            algorithm="XGBoost",
            metrics=metrics,
            file_path="/models/metrics_test/v1/model.pkl",
            training_date="2026-08-31T08:00:00",
            training_dataset="Q3_2026"
        )

        ModelRegistry.activate_model("metrics_test", "v1")
        active = ModelRegistry.get_active_model("metrics_test")

        assert active["metrics"] == metrics
        assert active["metrics"]["MAE"] == 14200
        assert active["metrics"]["MAPE"] == 0.15

    def test_multiple_model_types(self):
        """Test handling multiple different model types."""
        models_to_register = [
            ("sales_forecast", "v1", "XGBoost"),
            ("anomaly_detector", "v1", "IsolationForest"),
            ("demand_predictor", "v1", "RandomForest"),
        ]

        for model_name, version, algorithm in models_to_register:
            ModelRegistry.register_model(
                model_name=model_name,
                version=version,
                algorithm=algorithm,
                metrics={"score": 0.95},
                file_path=f"/models/{model_name}/{version}/model.pkl",
                training_date="2026-08-31T08:00:00",
                training_dataset="Q3_2026"
            )

        models = ModelRegistry.list_models()
        model_names = [m["model_name"] for m in models]

        assert "sales_forecast" in model_names
        assert "anomaly_detector" in model_names
        assert "demand_predictor" in model_names

    def test_activate_archives_previous(self):
        """Test that activating a new version archives the previous one."""
        model_name = "archive_test"

        # Register and activate v1
        ModelRegistry.register_model(
            model_name=model_name,
            version="v1",
            algorithm="XGBoost",
            metrics={"MAE": 14200},
            file_path=f"/models/{model_name}/v1/model.pkl",
            training_date="2026-08-31T08:00:00",
            training_dataset="Q3_2026"
        )
        ModelRegistry.activate_model(model_name, "v1")

        # Register and activate v2
        ModelRegistry.register_model(
            model_name=model_name,
            version="v2",
            algorithm="XGBoost",
            metrics={"MAE": 12800},
            file_path=f"/models/{model_name}/v2/model.pkl",
            training_date="2026-08-31T09:00:00",
            training_dataset="Q3_2026"
        )
        ModelRegistry.activate_model(model_name, "v2")

        # Get history
        history = ModelRegistry.get_model_history(model_name)

        # Should have both versions with different statuses
        v1 = next((v for v in history if v["version"] == "v1"), None)
        v2 = next((v for v in history if v["version"] == "v2"), None)

        assert v1 is not None
        assert v2 is not None
        assert v2["status"] == MODEL_STATUS_ACTIVE
        assert v1["status"] == MODEL_STATUS_ARCHIVED

    def test_no_active_model_returns_none(self):
        """Test that getting active model for non-existent model returns None."""
        active = ModelRegistry.get_active_model("nonexistent_model")
        assert active is None

    def test_rollback_nonexistent_version_fails(self):
        """Test that rollback to nonexistent version fails."""
        ModelRegistry.register_model(
            model_name="rollback_fail_test",
            version="v1",
            algorithm="XGBoost",
            metrics={"MAE": 14200},
            file_path="/models/rollback_fail_test/v1/model.pkl",
            training_date="2026-08-31T08:00:00",
            training_dataset="Q3_2026"
        )

        with pytest.raises(Exception):
            ModelRegistry.rollback_model(
                model_name="rollback_fail_test",
                target_version="v999",
                reason="This should fail"
            )
