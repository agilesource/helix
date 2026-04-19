"""
Anthropic API Adapter

Use Anthropic Claude API for LLM calls
"""

import os
import asyncio
from typing import Any, Dict, Optional

from helix.adapters.base import AIAdapter, AIRequest, AIResponse


class AnthropicAdapter(AIAdapter):
    """Anthropic Claude API adapter"""

    name = "anthropic"
    supported_models = ["claude-sonnet-4-20250514", "claude-sonnet-3-5-20241022", "claude-haiku-3-20240307"]

    def __init__(self, api_key: Optional[str] = None):
        # Check multiple environment variables
        self.api_key = (
            api_key or
            os.environ.get("ANTHROPIC_API_KEY") or
            os.environ.get("ANTHROPIC_AUTH_TOKEN")
        )
        self.base_url = os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com/v1")
        self.default_model = "claude-sonnet-3-5-20241022"
        # Disable SSL verification for custom endpoints (like JD Cloud)
        self.verify_ssl = self.base_url == "https://api.anthropic.com/v1"

    def is_available(self) -> bool:
        """Check if API is available"""
        return bool(self.api_key)

    async def execute(self, request: AIRequest) -> AIResponse:
        """Execute Anthropic API call"""
        if not self.is_available():
            return AIResponse(
                content="",
                success=False,
                error="ANTHROPIC_API_KEY not set"
            )

        try:
            import aiohttp

            model = request.model if request.model != "default" else self.default_model

            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }

            payload = {
                "model": model,
                "max_tokens": 4096,
                "messages": [
                    {"role": "user", "content": request.prompt}
                ]
            }

            if request.context:
                payload["system"] = str(request.context)

            # Configure SSL verification for custom endpoints (e.g., JD Cloud)
            ssl_context: bool = False if self.verify_ssl is False else True
            connector = aiohttp.TCPConnector(ssl=ssl_context)

            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.post(
                    f"{self.base_url}/messages",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        content = data.get("content", [{}])[0].get("text", "")

                        return AIResponse(
                            content=content,
                            success=True,
                            metadata={
                                "model": data.get("model"),
                                "usage": data.get("usage")
                            }
                        )
                    else:
                        error_text = await response.text()
                        return AIResponse(
                            content="",
                            success=False,
                            error=f"API error: {response.status} - {error_text}"
                        )

        except ImportError:
            return AIResponse(
                content="",
                success=False,
                error="aiohttp not installed. Run: pip install aiohttp"
            )
        except Exception as e:
            return AIResponse(
                content="",
                success=False,
                error=str(e)
            )


class OpenAIAdapter(AIAdapter):
    """OpenAI API adapter (fallback)"""

    name = "openai"
    supported_models = ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"]

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.base_url = "https://api.openai.com/v1"
        self.default_model = "gpt-4o"

    def is_available(self) -> bool:
        return bool(self.api_key)

    async def execute(self, request: AIRequest) -> AIResponse:
        if not self.is_available():
            return AIResponse(
                content="",
                success=False,
                error="OPENAI_API_KEY not set"
            )

        try:
            import aiohttp

            model = request.model if request.model != "default" else self.default_model

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "content-type": "application/json"
            }

            payload = {
                "model": model,
                "max_tokens": 4096,
                "messages": [
                    {"role": "user", "content": request.prompt}
                ]
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")

                        return AIResponse(
                            content=content,
                            success=True,
                            metadata={
                                "model": data.get("model"),
                                "usage": data.get("usage")
                            }
                        )
                    else:
                        error_text = await response.text()
                        return AIResponse(
                            content="",
                            success=False,
                            error=f"API error: {response.status} - {error_text}"
                        )

        except ImportError:
            return AIResponse(
                content="",
                success=False,
                error="aiohttp not installed. Run: pip install aiohttp"
            )
        except Exception as e:
            return AIResponse(
                content="",
                success=False,
                error=str(e)
            )


# Factory function - automatically select available adapter
def get_llm_adapter() -> Optional[AIAdapter]:
    """Get available LLM adapter"""

    # Try Anthropic first
    anthropic = AnthropicAdapter()
    if anthropic.is_available():
        return anthropic

    # Then try OpenAI
    openai = OpenAIAdapter()
    if openai.is_available():
        return openai

    # Neither is available
    return None
