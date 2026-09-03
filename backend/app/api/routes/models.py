"""
Model Management REST API endpoints.

Provides HTTP interface for:
- Registering new model versions
- Activating models for production
- Rolling back to previous versions
- Querying model history and status
"""

from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime
from app.ml.registry import ModelRegistry
from app.ml.models import SCHEMA_MODEL_VERSIONS, SCHEMA_MODEL_AUDIT_LOG
from app import db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/models", tags=["models"])


# ==================== Request/Response Schemas ====================

class RegisterModelRequest(BaseModel):
    """Request to register a new model."""
    version: str
    algorithm: str
    metrics: Dict[str, Any]
    file_path: str
    training_date: str
    training_dataset: str


class ActivateModelRequest(BaseModel):
    """Request to activate a model version."""
    reason: Optional[str] = ""


class RollbackRequest(BaseModel):
    """Request to rollback to a previous version."""
    target_version: str
    reason: Optional[str] = ""


class ModelResponse(BaseModel):
    """Response with model information."""
    model_name: str
    version: str
    algorithm: str
    status: str
    metrics: Dict[str, Any]


class ModelListResponse(BaseModel):
    """Response with list of models."""
    models: List[Dict[str, Any]]
    total: int


# ==================== Initialization ====================

def init_db():
    """Initialize database tables if they don't exist."""
    try:
        conn = db.get_connection(readonly=False)
        cursor = conn.cursor()
        cursor.execute(SCHEMA_MODEL_VERSIONS)
        cursor.execute(SCHEMA_MODEL_AUDIT_LOG)
        conn.commit()
        conn.close()
        logger.info("Model versioning tables initialized")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


# Initialize on module load
try:
    init_db()
except Exception as e:
    logger.warning(f"Could not initialize DB on import: {e}")


# ==================== API Endpoints ====================

@router.post("/{model_name}/register")
async def register_model(
    model_name: str,
    request: RegisterModelRequest
) -> Dict[str, Any]:
    """
    Register a new model version.

    The model starts in 'development' status and must be activated
    to be used in production.
    """
    try:
        result = ModelRegistry.register_model(
            model_name=model_name,
            version=request.version,
            algorithm=request.algorithm,
            metrics=request.metrics,
            file_path=request.file_path,
            training_date=request.training_date,
            training_dataset=request.training_dataset
        )
        return result
    except Exception as e:
        logger.error(f"Error registering model: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{model_name}/{version}/activate")
async def activate_model(
    model_name: str,
    version: str,
    request: ActivateModelRequest
) -> Dict[str, Any]:
    """
    Activate a model version for production.

    The previously active version (if any) is automatically archived.
    """
    try:
        result = ModelRegistry.activate_model(
            model_name=model_name,
            version=version,
            reason=request.reason
        )
        return result
    except Exception as e:
        logger.error(f"Error activating model: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{model_name}/rollback")
async def rollback_model(
    model_name: str,
    request: RollbackRequest
) -> Dict[str, Any]:
    """
    Rollback to a previous model version.

    Emergency operation to revert to a known-good version.
    """
    try:
        result = ModelRegistry.rollback_model(
            model_name=model_name,
            target_version=request.target_version,
            reason=request.reason
        )
        return result
    except Exception as e:
        logger.error(f"Error rolling back model: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{model_name}/active")
async def get_active_model(model_name: str) -> Dict[str, Any]:
    """Get the currently active model version."""
    try:
        model = ModelRegistry.get_active_model(model_name)
        if not model:
            raise HTTPException(status_code=404, detail=f"No active model found for {model_name}")
        return model
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting active model: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{model_name}/history")
async def get_model_history(model_name: str) -> Dict[str, Any]:
    """Get all versions of a model."""
    try:
        history = ModelRegistry.get_model_history(model_name)
        return {
            "model_name": model_name,
            "versions": history,
            "total": len(history)
        }
    except Exception as e:
        logger.error(f"Error getting model history: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("")
async def list_models() -> ModelListResponse:
    """List all registered models."""
    try:
        models = ModelRegistry.list_models()
        return ModelListResponse(models=models, total=len(models))
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/health/models")
async def health_check() -> Dict[str, str]:
    """Health check for model service."""
    try:
        init_db()
        return {"status": "healthy", "service": "model-registry"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")
