"""
Model versioning database schema - SQLite version.

Simple schema for tracking model versions and deployments.
No ORM needed - using raw SQL for simplicity with SQLite.
"""

# SQL Schema Definitions
# These are the table definitions needed for model versioning

SCHEMA_MODEL_VERSIONS = """
CREATE TABLE IF NOT EXISTS model_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    UNIQUE(model_name, version),
    CHECK(status IN ('development', 'staged', 'active', 'archived'))
);
"""

SCHEMA_MODEL_AUDIT_LOG = """
CREATE TABLE IF NOT EXISTS model_audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_name TEXT NOT NULL,
    version TEXT NOT NULL,
    action TEXT NOT NULL,
    reason TEXT,
    performed_by TEXT DEFAULT 'system',
    performed_at TEXT,
    details TEXT
);
"""

# Status constants
MODEL_STATUS_DEVELOPMENT = "development"
MODEL_STATUS_STAGED = "staged"
MODEL_STATUS_ACTIVE = "active"
MODEL_STATUS_ARCHIVED = "archived"

VALID_STATUSES = [
    MODEL_STATUS_DEVELOPMENT,
    MODEL_STATUS_STAGED,
    MODEL_STATUS_ACTIVE,
    MODEL_STATUS_ARCHIVED,
]

# Action constants for audit log
ACTION_REGISTER = "register"
ACTION_ACTIVATE = "activate"
ACTION_ROLLBACK = "rollback"
ACTION_ARCHIVE = "archive"
