"""
Helix AI Engine Manager

Multi-engine orchestration:
- Engine discovery and registration
- Load balancing
- Fallback handling
- Health checking
"""

import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

from helix.adapters.base import AIAdapter, AIRequest, AIResponse


class EngineStatus(Enum):
    """Engine status"""
    AVAILABLE = "available"
    BUSY = "busy"
    UNAVAILABLE = "unavailable"
    ERROR = "error"


@dataclass
class EngineConfig:
    """Engine configuration"""
    name: str
    adapter: AIAdapter
    priority: int = 0  # Higher = preferred
    max_concurrent: int = 3
    timeout: int = 60
    enabled: bool = True


@dataclass
class EngineHealth:
    """Engine health status"""
    name: str
    status: EngineStatus
    latency_ms: float = 0
    error_count: int = 0
    last_used: str = ""


class AIEngineManager:
    """
    AI Engine Manager

    Manages multiple AI engines with:
    - Automatic failover
    - Load balancing
    - Health monitoring
    """

    def __init__(self):
        self._engines: Dict[str, EngineConfig] = {}
        self._health: Dict[str, EngineHealth] = {}
        self._active_requests: Dict[str, int] = {}
        self._default_engine: Optional[str] = None

    def register_engine(self, config: EngineConfig) -> None:
        """Register an AI engine"""
        self._engines[config.name] = config
        self._health[config.name] = EngineHealth(
            name=config.name,
            status=EngineStatus.UNAVAILABLE
        )
        self._active_requests[config.name] = 0

        # Set as default if highest priority
        if self._default_engine is None or config.priority > self._engines[self._default_engine].priority:
            self._default_engine = config.name

    def get_engine(self, name: Optional[str] = None) -> Optional[EngineConfig]:
        """Get engine by name or get best available"""
        if name and name in self._engines:
            return self._engines[name]

        # Find best available engine
        return self._select_best_engine()

    def _select_best_engine(self) -> Optional[EngineConfig]:
        """Select best available engine based on priority and load"""
        available = []

        for name, config in self._engines.items():
            if not config.enabled:
                continue

            health = self._health.get(name, EngineHealth(name, EngineStatus.UNAVAILABLE))

            if health.status == EngineStatus.AVAILABLE:
                # Check concurrent limit
                if self._active_requests[name] < config.max_concurrent:
                    available.append((config.priority, name))

        if not available:
            return None

        # Sort by priority (highest first)
        available.sort(key=lambda x: x[0], reverse=True)
        return self._engines[available[0][1]]

    async def execute(
        self,
        request: AIRequest,
        engine_name: Optional[str] = None,
        fallback: bool = True
    ) -> AIResponse:
        """Execute request with engine selection"""
        config = self.get_engine(engine_name)

        if not config:
            return AIResponse(
                content="",
                success=False,
                error="No available AI engine"
            )

        # Track active request
        self._active_requests[config.name] += 1

        try:
            # Execute with timeout
            result = await asyncio.wait_for(
                config.adapter.execute(request),
                timeout=config.timeout
            )

            # Update health
            self._health[config.name].status = EngineStatus.AVAILABLE

            return result

        except asyncio.TimeoutError:
            error_msg = f"Request timeout after {config.timeout}s"
            self._health[config.name].error_count += 1
            return AIResponse(
                content="",
                success=False,
                error=error_msg
            )

        except Exception as e:
            self._health[config.name].error_count += 1

            # Try fallback
            if fallback:
                return await self.execute(request, fallback=False)

            return AIResponse(
                content="",
                success=False,
                error=str(e)
            )

        finally:
            self._active_requests[config.name] -= 1

    async def health_check(self) -> Dict[str, EngineHealth]:
        """Check health of all engines"""
        for name, config in self._engines.items():
            try:
                is_available = config.adapter.is_available()
                health = self._health[name]
                health.status = EngineStatus.AVAILABLE if is_available else EngineStatus.UNAVAILABLE
            except Exception:
                self._health[name].status = EngineStatus.ERROR

        return self._health

    def get_status(self) -> Dict[str, Any]:
        """Get manager status"""
        return {
            "engines": {
                name: {
                    "enabled": config.enabled,
                    "priority": config.priority,
                    "active_requests": self._active_requests[name],
                    "health": self._health[name].status.value
                }
                for name, config in self._engines.items()
            },
            "default": self._default_engine,
            "total_engines": len(self._engines),
        }


# Global instance
_engine_manager: Optional[AIEngineManager] = None


def get_engine_manager() -> AIEngineManager:
    """Get global engine manager"""
    global _engine_manager
    if _engine_manager is None:
        _engine_manager = AIEngineManager()
    return _engine_manager
