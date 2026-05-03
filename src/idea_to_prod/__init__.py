"""
Idea-To-Prod: Multi-Agent Core

A sophisticated system that transforms application ideas into fully 
implemented, tested, and deployable code using multiple AI agents.

Use cases:
  - Desktop App: python run_desktop_app.py
  - Web UI: python run_ui.py
"""

__version__ = "0.1.0"
__author__ = "AI For Dev Team"

# Core imports - always available
from idea_to_prod.agents import *  # noqa: F401, F403

__all__ = ["__version__", "__author__"]


# Lazy imports for UI servers (only loaded if explicitly imported)
def __getattr__(name):
    """Lazy load web UI dependencies"""
    if name == "app":
        from idea_to_prod.ui_server import app as _app
        return _app
    elif name == "run_ui_server":
        from idea_to_prod.ui_server import run_ui_server as _run
        return _run
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
