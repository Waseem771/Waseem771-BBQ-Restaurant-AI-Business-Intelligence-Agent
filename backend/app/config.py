"""Central configuration and path resolution for the BBQ BI MVP.

All paths are resolved relative to the project root (the folder that
contains this ``app`` package) so the app works regardless of the current
working directory. Every value can be overridden with an environment
variable, and a local ``.env`` file is loaded automatically if present.
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Project root = parent of the `app` package directory.
APP_ROOT: Path = Path(__file__).resolve().parent.parent

# Load .env from the project root (no-op if the file doesn't exist).
# Try both the backend directory and the project root (one level up),
# since the main .env lives at the project root.
load_dotenv(APP_ROOT.parent / ".env")
load_dotenv(APP_ROOT / ".env", override=True)


# The actual project root is one level above APP_ROOT (backend/) when the
# .env and data/ directory live at the top-level project folder.
PROJECT_ROOT: Path = APP_ROOT.parent


def _path_env(name: str, default: Path) -> Path:
    """Return a Path from an env var, falling back to ``default``.

    Relative paths from env vars are resolved against PROJECT_ROOT
    (where `.env` lives) so that `./data/bbq.db` works regardless of CWD.
    """
    value = os.getenv(name)
    if value:
        p = Path(value)
        if not p.is_absolute():
            p = PROJECT_ROOT / p
        return p
    return default


# --- Data locations -------------------------------------------------------
DATA_DIR: Path = _path_env("BBQ_DATA_DIR", PROJECT_ROOT / "data")
DB_PATH: Path = _path_env("BBQ_DB_PATH", DATA_DIR / "bbq.db")

# The Phase 1 CSVs live in a sibling `dataset/` folder by default:
#   Projects/dataset/*.csv   (this app lives in Projects/BBQ.../)
DATASET_DIR: Path = _path_env("BBQ_DATASET_DIR", PROJECT_ROOT.parent / "dataset")

# --- AI assistant ---------------------------------------------------------
# Which backend translates questions into SQL and phrases the answer.
#   auto (default) -> Groq if GROQ_API_KEY is set, else Anthropic, else the
#                     built-in deterministic engine.
#   groq | anthropic -> force that provider.
#   off              -> deterministic engine only.
LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "auto").lower()
LLM_ENABLED: str = os.getenv("LLM_ENABLED", "auto").lower()  # auto | on | off

# Groq (OpenAI-compatible chat completions)
GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY") or None
GROQ_MODEL: str = os.getenv("GROQ_MODEL", "qwen/qwen3.6-27b")
GROQ_REASONING_EFFORT: str = os.getenv("GROQ_REASONING_EFFORT", "default")

# Anthropic (Claude). ``LLM_MODEL`` is accepted for backwards compatibility.
# Some setups export the key as ``ANTHROPIC_AUTH_TOKEN`` instead of the
# canonical ``ANTHROPIC_API_KEY``; accept both and normalize into the standard
# env name used by the Anthropic Python SDK.
ANTHROPIC_API_KEY: str | None = os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_AUTH_TOKEN") or None
if ANTHROPIC_API_KEY and not os.getenv("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY
ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL") or os.getenv("LLM_MODEL") or "claude-opus-4-8"

_PROVIDERS: tuple[str, ...] = ("groq", "anthropic")

# --- Dashboard -> API -----------------------------------------------------
API_BASE_URL: str = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

# --- Display --------------------------------------------------------------
CURRENCY: str = "PKR"


def _sdk_importable(provider: str) -> bool:
    """True when the provider's Python SDK is installed."""
    try:
        if provider == "groq":
            import groq  # noqa: F401
        elif provider == "anthropic":
            import anthropic  # noqa: F401
        else:
            return False
    except ImportError:
        return False
    return True


def _api_key(provider: str) -> str | None:
    return {"groq": GROQ_API_KEY, "anthropic": ANTHROPIC_API_KEY}.get(provider)


def llm_provider() -> str | None:
    """The LLM backend to use, or ``None`` for the deterministic engine.

    A provider is usable when its SDK is importable and either its API key is
    present (``LLM_ENABLED=auto``) or the path is forced (``LLM_ENABLED=on``,
    e.g. when credentials come from a CLI profile instead of the environment).
    """
    if LLM_ENABLED == "off" or LLM_PROVIDER == "off":
        return None
    candidates = (LLM_PROVIDER,) if LLM_PROVIDER in _PROVIDERS else _PROVIDERS
    for provider in candidates:
        if _sdk_importable(provider) and (_api_key(provider) or LLM_ENABLED == "on"):
            return provider
    return None


def llm_model() -> str | None:
    """The model id of the active provider, or ``None`` if there is none."""
    return {"groq": GROQ_MODEL, "anthropic": ANTHROPIC_MODEL}.get(llm_provider())


def llm_available() -> bool:
    """True when a natural-language (LLM) path is available."""
    return llm_provider() is not None
