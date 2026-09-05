"""
Model Loader - Safe loading of models with caching.

Loads the active model version and caches it in memory for fast inference.
"""

from typing import Optional, Dict, Any
import logging
import pickle
from app import db
from app.ml.models import MODEL_STATUS_ACTIVE

logger = logging.getLogger(__name__)


class ModelCache:
    """Simple in-memory cache for loaded models."""

    def __init__(self):
        self.cache: Dict[str, Any] = {}

    def get(self, key: str) -> Optional[Any]:
        """Get cached model."""
        return self.cache.get(key)

    def set(self, key: str, value: Any) -> None:
        """Cache a model."""
        self.cache[key] = value

    def clear(self, key: str = None) -> None:
        """Clear cache."""
        if key:
            self.cache.pop(key, None)
        else:
            self.cache.clear()


# Global cache instance
_model_cache = ModelCache()


class ModelLoader:
    """Load and cache models for inference."""

    @staticmethod
    def load_model(model_name: str) -> Optional[Any]:
        """
        Load the active model version for a model.

        Uses cache when available. Falls back to disk if needed.

        Args:
            model_name: Name of model (e.g., "sales_forecast")

        Returns:
            Loaded model or None if not found

        Raises:
            Exception: If model cannot be loaded
        """
        try:
            # Check cache
            cached = _model_cache.get(model_name)
            if cached:
                logger.debug(f"Model {model_name} loaded from cache")
                return cached

            # Get active version from DB
            conn = db.get_connection(readonly=True)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT file_path FROM model_versions
                WHERE model_name=? AND status=?
                LIMIT 1
            """, (model_name, MODEL_STATUS_ACTIVE))

            row = cursor.fetchone()
            conn.close()

            if not row:
                logger.warning(f"No active model found for {model_name}")
                return None

            file_path = row[0]

            # Load from disk
            try:
                with open(file_path, 'rb') as f:
                    model = pickle.load(f)
                logger.debug(f"Model {model_name} loaded from {file_path}")

                # Cache it
                _model_cache.set(model_name, model)

                return model
            except FileNotFoundError:
                logger.error(f"Model file not found: {file_path}")
                return None

        except Exception as e:
            logger.error(f"Error loading model {model_name}: {e}")
            raise

    @staticmethod
    def load_model_version(model_name: str, version: str) -> Optional[Any]:
        """
        Load a specific model version.

        Args:
            model_name: Name of model
            version: Version to load (e.g., "v1", "v2")

        Returns:
            Loaded model or None if not found
        """
        try:
            conn = db.get_connection(readonly=True)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT file_path FROM model_versions
                WHERE model_name=? AND version=?
                LIMIT 1
            """, (model_name, version))

            row = cursor.fetchone()
            conn.close()

            if not row:
                logger.warning(f"Model {model_name} v{version} not found")
                return None

            file_path = row[0]

            try:
                with open(file_path, 'rb') as f:
                    model = pickle.load(f)
                logger.debug(f"Model {model_name} v{version} loaded from {file_path}")
                return model
            except FileNotFoundError:
                logger.error(f"Model file not found: {file_path}")
                return None

        except Exception as e:
            logger.error(f"Error loading model {model_name} v{version}: {e}")
            raise

    @staticmethod
    def clear_cache(model_name: str = None) -> None:
        """
        Clear model cache.

        Args:
            model_name: Specific model to clear, or None to clear all
        """
        _model_cache.clear(model_name)
        logger.debug(f"Cache cleared for {model_name or 'all models'}")


def get_model_loader() -> ModelLoader:
    """Get the model loader instance."""
    return ModelLoader()
