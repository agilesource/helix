"""
AI Engine Adapter Base Classes

Helix supports multiple AI engines as execution backends:
- Claude Code
- OpenClaw
- OpenCode
- Cursor
- GitHub Copilot CLI
- Gemini CLI
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class AIRequest:
    """AI Request"""
    prompt: str
    context: Optional[Dict[str, Any]] = None
    model: str = "default"


@dataclass
class AIResponse:
    """AI Response"""
    content: str
    success: bool
    error: Optional[str] = None
    metadata: Dict[str, Any] = None


class AIAdapter(ABC):
    """AI Adapter Base Class"""

    name: str = "base"
    supported_models: list = []

    @abstractmethod
    async def execute(self, request: AIRequest) -> AIResponse:
        """Execute AI request"""
        pass

    def is_available(self) -> bool:
        """Check if adapter is available"""
        raise NotImplementedError


class ClaudeCodeAdapter(AIAdapter):
    """Claude Code Adapter"""

    name = "claude_code"
    supported_models = ["sonnet", "haiku", "opus"]

    async def execute(self, request: AIRequest) -> AIResponse:
        # TODO: Implement Claude Code invocation
        pass

    def is_available(self) -> bool:
        # TODO: Check if CLI is available
        return False


class OpenClawAdapter(AIAdapter):
    """OpenClaw Adapter"""

    name = "openclaw"
    supported_models = ["default"]

    async def execute(self, request: AIRequest) -> AIResponse:
        # TODO: Implement OpenClaw invocation
        pass

    def is_available(self) -> bool:
        # TODO: Check if CLI is available
        return False
