"""
Helix AI Engines Package

Multi-engine AI orchestration:
- AIEngineManager: Multi-engine load balancing and failover
- IntentRecognizer: Natural language to skill routing
- Claude Code integration
- OpenClaw integration
"""

from helix.engines.manager import (
    AIEngineManager,
    EngineConfig,
    EngineHealth,
    EngineStatus,
    get_engine_manager,
)
from helix.engines.recognizer import (
    IntentRecognizer,
    RecognitionResult,
    IntentSource,
    get_recognizer,
)

__all__ = [
    "AIEngineManager",
    "EngineConfig",
    "EngineHealth",
    "EngineStatus",
    "get_engine_manager",
    "IntentRecognizer",
    "RecognitionResult",
    "IntentSource",
    "get_recognizer",
]
