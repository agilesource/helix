"""Test LLM adapters"""

import pytest
import os
from helix.adapters.base import AIRequest, AIResponse
from helix.adapters.llm import AnthropicAdapter, OpenAIAdapter, get_llm_adapter


class TestAIRequest:
    """Test AIRequest"""

    def test_create_request(self):
        """Test creating request"""
        req = AIRequest(prompt="Hello")
        assert req.prompt == "Hello"
        assert req.model == "default"

    def test_request_with_context(self):
        """Test request with context"""
        req = AIRequest(prompt="Hello", context="You are a helpful assistant")
        assert req.context == "You are a helpful assistant"

    def test_request_with_model(self):
        """Test request with custom model"""
        req = AIRequest(prompt="Hello", model="claude-sonnet-4-20250514")
        assert req.model == "claude-sonnet-4-20250514"


class TestAIResponse:
    """Test AIResponse"""

    def test_success_response(self):
        """Test successful response"""
        resp = AIResponse(
            content="Hello there!",
            success=True
        )
        assert resp.success is True
        assert resp.content == "Hello there!"

    def test_failure_response(self):
        """Test failure response"""
        resp = AIResponse(
            content="",
            success=False,
            error="API error"
        )
        assert resp.success is False
        assert resp.error == "API error"

    def test_response_with_metadata(self):
        """Test response with metadata"""
        resp = AIResponse(
            content="Hello",
            success=True,
            metadata={"model": "claude-3", "usage": {"tokens": 100}}
        )
        assert resp.metadata["model"] == "claude-3"


class TestAnthropicAdapter:
    """Test AnthropicAdapter"""

    def test_adapter_init_with_key(self):
        """Test adapter initialization with API key"""
        os.environ.pop("ANTHROPIC_API_KEY", None)
        os.environ.pop("ANTHROPIC_AUTH_TOKEN", None)

        adapter = AnthropicAdapter(api_key="test-key")
        assert adapter.api_key == "test-key"

    def test_adapter_init_with_env(self):
        """Test adapter initialization from env"""
        os.environ["ANTHROPIC_API_KEY"] = "env-key"

        adapter = AnthropicAdapter()
        assert adapter.api_key == "env-key"

        del os.environ["ANTHROPIC_API_KEY"]

    def test_adapter_default_model(self):
        """Test default model"""
        adapter = AnthropicAdapter(api_key="test")
        assert adapter.default_model == "claude-sonnet-3-5-20241022"

    def test_adapter_is_available(self):
        """Test availability check"""
        adapter = AnthropicAdapter(api_key="test")
        assert adapter.is_available() is True

        adapter_no_key = AnthropicAdapter(api_key=None)
        os.environ.pop("ANTHROPIC_API_KEY", None)
        os.environ.pop("ANTHROPIC_AUTH_TOKEN", None)
        assert adapter_no_key.is_available() is False


class TestOpenAIAdapter:
    """Test OpenAIAdapter"""

    def test_openai_adapter_init(self):
        """Test OpenAI adapter initialization"""
        adapter = OpenAIAdapter(api_key="test-key")
        assert adapter.api_key == "test-key"
        assert adapter.default_model == "gpt-4o"
        assert adapter.base_url == "https://api.openai.com/v1"


class TestGetLLMAdapter:
    """Test adapter factory"""

    def test_get_llm_adapter_priority(self):
        """Test Anthropic takes priority over OpenAI"""
        os.environ["ANTHROPIC_API_KEY"] = "test"
        os.environ["OPENAI_API_KEY"] = "test"

        adapter = get_llm_adapter()
        assert isinstance(adapter, AnthropicAdapter)

        del os.environ["ANTHROPIC_API_KEY"]
        del os.environ["OPENAI_API_KEY"]

    def test_get_llm_adapter_fallback_to_openai(self):
        """Test fallback to OpenAI when Anthropic unavailable"""
        os.environ.pop("ANTHROPIC_API_KEY", None)
        os.environ.pop("ANTHROPIC_AUTH_TOKEN", None)
        os.environ["OPENAI_API_KEY"] = "test"

        adapter = get_llm_adapter()
        assert isinstance(adapter, OpenAIAdapter)

        del os.environ["OPENAI_API_KEY"]

    def test_get_llm_adapter_none_available(self):
        """Test returns None when no adapter available"""
        os.environ.pop("ANTHROPIC_API_KEY", None)
        os.environ.pop("ANTHROPIC_AUTH_TOKEN", None)
        os.environ.pop("OPENAI_API_KEY", None)

        adapter = get_llm_adapter()
        assert adapter is None


class TestAnthropicAdapterExecute:
    """Test AnthropicAdapter async execution"""

    @pytest.mark.asyncio
    async def test_execute_no_api_key(self):
        """Test execute fails without API key"""
        os.environ.pop("ANTHROPIC_API_KEY", None)
        os.environ.pop("ANTHROPIC_AUTH_TOKEN", None)

        adapter = AnthropicAdapter()
        request = AIRequest(prompt="test")

        response = await adapter.execute(request)
        assert response.success is False
        assert "not set" in response.error.lower()

    @pytest.mark.asyncio
    async def test_execute_import_error(self):
        """Test execute handles missing aiohttp"""
        import sys
        import importlib

        # Mock aiohttp as not installed by temporarily modifying import
        adapter = AnthropicAdapter(api_key="test-key")

        # Patch the import to raise ImportError
        import helix.adapters.llm as llm_module
        original_import = __builtins__["__import__"]

        def mock_import(name, *args, **kwargs):
            if name == "aiohttp":
                raise ImportError("No module named 'aiohttp'")
            return original_import(name, *args, **kwargs)

        try:
            __builtins__["__import__"] = mock_import
            request = AIRequest(prompt="test")
            response = await adapter.execute(request)
            assert response.success is False
            assert "aiohttp" in response.error
        finally:
            __builtins__["__import__"] = original_import


class TestOpenAIAdapterExecute:
    """Test OpenAIAdapter async execution"""

    @pytest.mark.asyncio
    async def test_execute_no_api_key(self):
        """Test execute fails without API key"""
        os.environ.pop("OPENAI_API_KEY", None)

        adapter = OpenAIAdapter()
        request = AIRequest(prompt="test")

        response = await adapter.execute(request)
        assert response.success is False
        assert "not set" in response.error.lower()
