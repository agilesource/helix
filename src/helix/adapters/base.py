"""
AI 引擎适配器基类

Helix 支持多种 AI 引擎作为执行后端：
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
    """AI 请求"""
    prompt: str
    context: Optional[Dict[str, Any]] = None
    model: str = "default"


@dataclass
class AIResponse:
    """AI 响应"""
    content: str
    success: bool
    error: Optional[str] = None
    metadata: Dict[str, Any] = None


class AIAdapter(ABC):
    """AI 适配器基类"""

    name: str = "base"
    supported_models: list = []

    @abstractmethod
    async def execute(self, request: AIRequest) -> AIResponse:
        """执行 AI 请求"""
        pass

    def is_available(self) -> bool:
        """检查适配器是否可用"""
        raise NotImplementedError


class ClaudeCodeAdapter(AIAdapter):
    """Claude Code 适配器"""

    name = "claude_code"
    supported_models = ["sonnet", "haiku", "opus"]

    async def execute(self, request: AIRequest) -> AIResponse:
        # TODO: 实现 Claude Code 调用
        pass

    def is_available(self) -> bool:
        # TODO: 检查 CLI 是否可用
        return False


class OpenClawAdapter(AIAdapter):
    """OpenClaw 适配器"""

    name = "openclaw"
    supported_models = ["default"]

    async def execute(self, request: AIRequest) -> AIResponse:
        # TODO: 实现 OpenClaw 调用
        pass

    def is_available(self) -> bool:
        # TODO: 检查 CLI 是否可用
        return False
