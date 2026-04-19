"""
Helix Claude Code Adapter

Integrates with Claude Code for AI-powered code generation
"""

import asyncio
import json
import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from pathlib import Path

from helix.adapters.base import AIAdapter, AIRequest, AIResponse


@dataclass
class ClaudeCodeConfig:
    """Claude Code configuration"""
    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 4096
    temperature: float = 0.7
    tools_enabled: bool = True
    mcp_enabled: bool = True
    workspace_root: str = ""


class ClaudeCodeAdapter(AIAdapter):
    """
    Claude Code Adapter

    Provides AI code generation using Claude Code
    """

    name = "claude_code"
    description = "Claude Code - Anthropic's AI coding assistant"

    def __init__(self, config: Optional[ClaudeCodeConfig] = None):
        super().__init__()
        self.config = config or ClaudeCodeConfig()
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize the adapter"""
        if self._initialized:
            return

        # Check if Claude Code is available
        try:
            result = await asyncio.create_subprocess_exec(
                "claude", "--version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await result.communicate()
            self._initialized = result.returncode == 0
        except FileNotFoundError:
            self._initialized = False

        if not self._initialized:
            raise RuntimeError("Claude Code not found. Please install Claude Code.")

    async def execute(self, request: AIRequest) -> AIResponse:
        """
        Execute a request using Claude Code

        Args:
            request: AI request with prompt and context

        Returns:
            AI response
        """
        if not self._initialized:
            await self.initialize()

        try:
            # Build Claude Code command
            cmd = self._build_command(request)

            # Execute
            result = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.config.workspace_root or os.getcwd(),
            )

            stdout, stderr = await result.communicate()

            if result.returncode != 0:
                return AIResponse(
                    success=False,
                    content="",
                    error=stderr.decode() or "Claude Code execution failed",
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
        """Build Claude Code command"""
        cmd = ["claude", "-p", request.prompt]

        # Add model
        cmd.extend(["--model", self.config.model])

        # Add max tokens
        if self.config.max_tokens:
            cmd.extend(["--max-tokens", str(self.config.max_tokens)])

        # Add temperature
        if self.config.temperature:
            cmd.extend(["--temperature", str(self.config.temperature)])

        return cmd

    async def execute_with_tools(self, prompt: str, tools: List[str],
                                  context: Dict[str, Any]) -> AIResponse:
        """
        Execute with tool access

        Args:
            prompt: User prompt
            tools: List of tool names to enable
            context: Execution context

        Returns:
            AI response
        """
        # Claude Code handles tools via --allowedTools in newer versions
        # For now, return a basic response
        request = AIRequest(prompt=prompt, context=context)
        return await self.execute(request)

    def get_available_tools(self) -> List[str]:
        """Get list of available tools"""
        return [
            "read",
            "write",
            "edit",
            "bash",
            "grep",
            "glob",
            "web-fetch",
        ]

    def supports_streaming(self) -> bool:
        """Check if streaming is supported"""
        return False  # Claude Code CLI doesn't support streaming

    def get_context_limit(self) -> int:
        """Get maximum context size in tokens"""
        # Claude Sonnet 4 has 200K context
        return 200000


# Alternative: Direct API adapter (for when Claude Code CLI isn't available)
@dataclass
class AnthropicConfig:
    """Anthropic API configuration"""
    api_key: str = ""
    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 4096
    temperature: float = 0.7


class AnthropicAdapter(AIAdapter):
    """
    Anthropic API Adapter

    Direct API access to Claude
    """

    name = "anthropic"
    description = "Anthropic API - Direct access to Claude"

    def __init__(self, config: Optional[AnthropicConfig] = None):
        super().__init__()
        self.config = config or AnthropicConfig()
        self._api_key: Optional[str] = None

    async def initialize(self) -> None:
        """Initialize the adapter"""
        # Get API key from environment or config
        self._api_key = self.config.api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self._api_key:
            raise RuntimeError("ANTHROPIC_API_KEY not set")

    async def execute(self, request: AIRequest) -> AIResponse:
        """Execute request via Anthropic API"""
        import aiohttp

        if not self._api_key:
            await self.initialize()

        headers = {
            "x-api-key": self._api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

        body = {
            "model": self.config.model,
            "max_tokens": self.config.max_tokens,
            "messages": [
                {"role": "user", "content": request.prompt}
            ],
        }

        if self.config.temperature:
            body["temperature"] = self.config.temperature

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.anthropic.com/v1/messages",
                    headers=headers,
                    json=body,
                ) as response:
                    if response.status != 200:
                        error = await response.text()
                        return AIResponse(
                            success=False,
                            content="",
                            error=f"API error: {response.status} - {error}",
                        )

                    data = await response.json()
                    return AIResponse(
                        success=True,
                        content=data["content"][0]["text"],
                        model=self.config.model,
                    )

        except Exception as e:
            return AIResponse(
                success=False,
                content="",
                error=str(e),
            )

    def get_context_limit(self) -> int:
        """Get maximum context size"""
        return 200000

    def supports_streaming(self) -> bool:
        """Check streaming support"""
        return True
