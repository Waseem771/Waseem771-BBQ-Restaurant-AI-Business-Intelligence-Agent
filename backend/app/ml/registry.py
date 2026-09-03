"""
Model Registry Service - SQLite version for tracking model versions and rollbacks.

Simpler implementation optimized for the BBQ project's SQLite setup.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
import logging
import json
from app import db

logger = logging.getLogger(__name__)


class ModelRegistry:
    """Simple model registry for SQLite."""

    @staticmethod
    def register_model(
        model_name: str,
        version: str,
        algorithm: str,
        metrics: Dict[str, Any],
        file_path: str,
        training_date: str,
        training_dataset: str,
    ) -> Dict[str, Any]:
        """Register a new model version."""
        try:
            conn = db.get_connection(readonly=False)
            cursor = conn.cursor()

            # Create table if not exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS model_versions (
                    id INTEGER PRIMARY KEY,
                    model_name TEXT NOT NULL,
                    version TEXT NOT NULL,
                    algorithm TEXT,
                    status TEXT DEFAULT 'development',
                    metrics TEXT,
                    file_path TEXT,
                    training_date TEXT,
                    training_dataset TEXT,
                    created_at TEXT,
                    activated_at TEXT,
                    UNIQUE(model_name, version)
                )
            """)

            # Check if already exists
            cursor.execute(
                "SELECT * FROM model_versions WHERE model_name=? AND version=?",
                (model_name, version)
            )
            if cursor.fetchone():
                raise Exception(f"Model {model_name} v{version} already exists")

            # Insert
            cursor.execute("""
                INSERT INTO model_versions
                (model_name, version, algorithm, status, metrics, file_path,
                 training_date, training_dataset, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                model_name, version, algorithm, "development",
                json.dumps(metrics), file_path,
                training_date, training_dataset, datetime.now().isoformat()
            ))
            conn.commit()
            conn.close()

            return {"success": True, "message": f"Registered {model_name} version {version}"}
        except Exception as e:
            logger.error(f"Error registering model: {e}")
            raise

    @staticmethod
    def activate_model(model_name: str, version: str, reason: str = "") -> Dict[str, Any]:
        """Activate a model version for production."""
        try:
            conn = db.get_connection(readonly=False)
            cursor = conn.cursor()

            # Archive current active
            cursor.execute("""
                UPDATE model_versions
                SET status='archived'
                WHERE model_name=? AND status='active'
            """, (model_name,))

            # Activate new
            cursor.execute("""
                UPDATE model_versions
                SET status='active', activated_at=?
                WHERE model_name=? AND version=?
            """, (datetime.now().isoformat(), model_name, version))

            conn.commit()
            conn.close()

            return {"success": True, "message": f"Activated {model_name} v{version}"}
        except Exception as e:
            logger.error(f"Error activating model: {e}")
            raise

    @staticmethod
    def get_active_model(model_name: str) -> Optional[Dict[str, Any]]:
        """Get the currently active model version."""
        try:
            conn = db.get_connection(readonly=True)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM model_versions
                WHERE model_name=? AND status='active'
                LIMIT 1
            """, (model_name,))

            row = cursor.fetchone()
            conn.close()

            if not row:
                return None

            # Convert to dict
            cols = [description[0] for description in cursor.description]
            result = dict(zip(cols, row))
            if result['metrics']:
                result['metrics'] = json.loads(result['metrics'])
            return result
        except Exception as e:
            logger.error(f"Error getting active model: {e}")
            raise

    @staticmethod
    def rollback_model(model_name: str, target_version: str, reason: str = "") -> Dict[str, Any]:
        """Rollback to a previous model version."""
        try:
            conn = db.get_connection(readonly=False)
            cursor = conn.cursor()

            # Verify target exists
            cursor.execute(
                "SELECT * FROM model_versions WHERE model_name=? AND version=?",
                (model_name, target_version)
            )
            if not cursor.fetchone():
                raise Exception(f"Version {target_version} not found")

            # Archive current active
            cursor.execute("""
                UPDATE model_versions
                SET status='archived'
                WHERE model_name=? AND status='active'
            """, (model_name,))

            # Activate target
            cursor.execute("""
                UPDATE model_versions
                SET status='active', activated_at=?
                WHERE model_name=? AND version=?
            """, (datetime.now().isoformat(), model_name, target_version))

            conn.commit()
            conn.close()

            return {"success": True, "message": f"Rolled back to {model_name} v{target_version}"}
        except Exception as e:
            logger.error(f"Error rolling back model: {e}")
            raise

    @staticmethod
    def get_model_history(model_name: str) -> List[Dict[str, Any]]:
        """Get all versions of a model."""
        try:
            conn = db.get_connection(readonly=True)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM model_versions
                WHERE model_name=?
                ORDER BY created_at DESC
            """, (model_name,))

            rows = cursor.fetchall()
            cols = [description[0] for description in cursor.description]
            conn.close()

            results = []
            for row in rows:
                result = dict(zip(cols, row))
                if result.get('metrics'):
                    result['metrics'] = json.loads(result['metrics'])
                results.append(result)

            return results
        except Exception as e:
            logger.error(f"Error getting model history: {e}")
            raise

    @staticmethod
    def list_models() -> List[Dict[str, Any]]:
        """List all unique models."""
        try:
            conn = db.get_connection(readonly=True)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT DISTINCT model_name FROM model_versions
                ORDER BY model_name
            """)

            models = [row[0] for row in cursor.fetchall()]
            conn.close()

            result = []
            for model_name in models:
                active = ModelRegistry.get_active_model(model_name)
                result.append({
                    "model_name": model_name,
                    "active_version": active['version'] if active else None,
                    "status": "active" if active else "inactive"
                })

            return result
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            raise
