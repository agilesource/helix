"""
Helix API Package

REST API for Helix:
- FastAPI-based server
- Skill execution endpoints
- Plugin management
- Webhook handlers
"""

from helix.api.server import app, run_server

__all__ = ["app", "run_server"]
