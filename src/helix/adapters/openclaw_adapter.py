"""
Helix OpenClaw Adapter

Integrates with OpenClaw for AI-powered software engineering
"""

import asyncio
import json
import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from pathlib import Path

from helix.adapters.base import AIAdapter, AIRequest, AIResponse


@dataclass
class OpenClawConfig:
    """OpenClaw configuration"""
    workspace: str = ""  # Workspace directory
    model: str = "sonnet"
    max_tokens: int = 8192
    temperature: float = 0.7
    auto_approve: bool = False
    watch_mode: bool = False


class OpenClawAdapter(AIAdapter):
    """
    OpenClaw Adapter

    Provides AI software engineering using OpenClaw
    """

    name = "openclaw"
    description = "OpenClaw - AI-powered software engineering framework"

    def __init__(self, config: Optional[OpenClawConfig] = None):
        super().__init__()
        self.config = config or OpenClawConfig()
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize the adapter"""
        if self._initialized:
            return

        # Check if OpenClaw is available
        try:
            result = await asyncio.create_subprocess_exec(
                "openclaw", "--version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await result.communicate()
            self._initialized = result.returncode == 0
        except FileNotFoundError:
            self._initialized = False

        if not self._initialized:
            raise RuntimeError("OpenClaw not found. Please install OpenClaw.")

    async def execute(self, request: AIRequest) -> AIResponse:
        """
        Execute a request using OpenClaw

        Args:
            request: AI request

        Returns:
            AI response
        """
        if not self._initialized:
            await self.initialize()

        try:
            # Build OpenClaw command
            cmd = self._build_command(request)

            # Execute
            result = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.config.workspace or os.getcwd(),
            )

            stdout, stderr = await result.communicate()

            if result.returncode != 0:
                return AIResponse(
                    success=False,
                    content="",
                    error=stderr.decode() or "OpenClaw execution failed",
                )

            # Parse response
            response_text = stdout.decode()
            return AIResponse(
                success=True,
                content=response_text,
                model=self.config.model,
            )

        except Exception as e:
            return AIResponse(
                success=False,
                content="",
                error=str(e),
            )

    def _build_command(self, request: AIRequest) -> List[str]:
        """Build OpenClaw command"""
        cmd = ["openclaw", "exec", request.prompt]

        # Add model
        if self.config.model:
            cmd.extend(["--model", self.config.model])

        # Add max tokens
        if self.config.max_tokens:
            cmd.extend(["--max-tokens", str(self.config.max_tokens)])

        # Auto-approve dangerous commands
        if self.config.auto_approve:
            cmd.append("--yes")

        return cmd

    async def execute_task(self, task: str, context: Dict[str, Any]) -> AIResponse:
        """
        Execute a task (higher-level operation)

        Args:
            task: Task description
            context: Execution context

        Returns:
            AI response
        """
        prompt = f"Task: {task}\n\nContext: {json.dumps(context)}"
        request = AIRequest(prompt=prompt, context=context)
        return await self.execute(request)

    def get_available_actions(self) -> List[str]:
        """Get list of available OpenClaw actions"""
        return [
            "read",
            "write",
            "edit",
            "bash",
            "grep",
            "glob",
            "web-fetch",
            "tool",
            "task",
        ]

    def supports_streaming(self) -> bool:
        """Check if streaming is supported"""
        return True

    def get_context_limit(self) -> int:
        """Get maximum context size in tokens"""
        # OpenClaw uses Claude models
        return 200000


# OpenClaw Workspace Manager
@dataclass
class WorkspaceInfo:
    """Workspace information"""
    path: str
    name: str
    is_active: bool = False
    last_task: str = ""


class OpenClawWorkspace:
    """
    OpenClaw Workspace Manager

    Manages OpenClaw workspace for multi-project usage
    """

    def __init__(self, workspace_root: Optional[str] = None):
        self.workspace_root = workspace_root or os.path.expanduser("~/.openclaw")
        self._current_workspace: Optional[WorkspaceInfo] = None

    async def initialize(self) -> None:
        """Initialize workspace"""
        os.makedirs(self.workspace_root, exist_ok=True)

        # Create default workspace if needed
        default_ws = os.path.join(self.workspace_root, "default")
        if not os.path.exists(default_ws):
            os.makedirs(default_ws, exist_ok=True)

    def get_workspaces(self) -> List[WorkspaceInfo]:
        """Get all workspaces"""
        workspaces: list[WorkspaceInfo] = []

        if not os.path.exists(self.workspace_root):
            return workspaces

        for name in os.listdir(self.workspace_root):
            path = os.path.join(self.workspace_root, name)
            if os.path.isdir(path) and not name.startswith("."):
                is_active = bool(self._current_workspace and self._current_workspace.name == name)
                workspaces.append(WorkspaceInfo(
                    path=path,
                    name=name,
                    is_active=is_active,
                ))

        return workspaces

    def create_workspace(self, name: str) -> WorkspaceInfo:
        """Create a new workspace"""
        path = os.path.join(self.workspace_root, name)
        os.makedirs(path, exist_ok=True)

        info = WorkspaceInfo(path=path, name=name)
        return info

    def switch_workspace(self, name: str) -> bool:
        """Switch to a different workspace"""
        path = os.path.join(self.workspace_root, name)
        if not os.path.exists(path):
            return False

        self._current_workspace = WorkspaceInfo(
            path=path,
            name=name,
            is_active=True,
        )
        return True

    def get_current_workspace(self) -> Optional[WorkspaceInfo]:
        """Get current workspace"""
        return self._current_workspace
