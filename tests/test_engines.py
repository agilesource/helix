"""Test AI Engine Manager"""

import pytest
from unittest.mock import Mock, AsyncMock
from helix.engines.manager import (
    AIEngineManager,
    EngineConfig,
    EngineHealth,
    EngineStatus,
    get_engine_manager,
)


class TestEngineConfig:
    """Test EngineConfig dataclass"""

    def test_engine_config_creation(self):
        """Test creating engine config"""
        adapter = Mock()
        config = EngineConfig(name="test-engine", adapter=adapter)
        assert config.name == "test-engine"
        assert config.adapter is adapter
        assert config.priority == 0
        assert config.max_concurrent == 3
        assert config.timeout == 60
        assert config.enabled is True


class TestEngineHealth:
    """Test EngineHealth dataclass"""

    def test_engine_health_creation(self):
        """Test creating engine health"""
        health = EngineHealth(
            name="test-engine",
            status=EngineStatus.AVAILABLE,
            latency_ms=50.0,
            error_count=0
        )
        assert health.name == "test-engine"
        assert health.status == EngineStatus.AVAILABLE
        assert health.latency_ms == 50.0
        assert health.error_count == 0


class TestAIEngineManager:
    """Test AIEngineManager"""

    @pytest.fixture
    def manager(self):
        """Create a fresh manager"""
        return AIEngineManager()

    @pytest.fixture
    def mock_adapter(self):
        """Create a mock adapter"""
        adapter = Mock()
        adapter.is_available = Mock(return_value=True)
        adapter.execute = AsyncMock(return_value=Mock(content="test response", success=True))
        return adapter

    def test_manager_init(self, manager):
        """Test manager initialization"""
        assert manager._engines == {}
        assert manager._health == {}
        assert manager._active_requests == {}
        assert manager._default_engine is None

    def test_register_engine(self, manager, mock_adapter):
        """Test registering an engine"""
        config = EngineConfig(name="test-engine", adapter=mock_adapter, priority=10)
        manager.register_engine(config)

        assert "test-engine" in manager._engines
        assert "test-engine" in manager._health
        assert "test-engine" in manager._active_requests

    def test_register_engine_sets_default(self, manager, mock_adapter):
        """Test registering sets first engine as default"""
        config1 = EngineConfig(name="engine1", adapter=mock_adapter, priority=5)
        config2 = EngineConfig(name="engine2", adapter=mock_adapter, priority=10)

        manager.register_engine(config1)
        assert manager._default_engine == "engine1"

        manager.register_engine(config2)
        assert manager._default_engine == "engine2"

    def test_get_engine_by_name(self, manager, mock_adapter):
        """Test getting engine by name"""
        config = EngineConfig(name="test-engine", adapter=mock_adapter)
        manager.register_engine(config)

        result = manager.get_engine("test-engine")
        assert result is not None
        assert result.name == "test-engine"

    def test_get_engine_not_found(self, manager, mock_adapter):
        """Test getting non-existent engine returns None"""
        result = manager.get_engine("nonexistent")
        assert result is None

    def test_get_status(self, manager, mock_adapter):
        """Test getting manager status"""
        config = EngineConfig(name="test-engine", adapter=mock_adapter, priority=5)
        manager.register_engine(config)

        status = manager.get_status()
        assert "engines" in status
        assert "test-engine" in status["engines"]
        assert status["default"] == "test-engine"
        assert status["total_engines"] == 1


@pytest.mark.asyncio
class TestAIEngineManagerExecute:
    """Test async execution"""

    @pytest.fixture
    def manager(self):
        return AIEngineManager()

    @pytest.fixture
    def mock_adapter(self):
        adapter = Mock()
        adapter.is_available = Mock(return_value=True)
        adapter.execute = AsyncMock(return_value=Mock(content="response", success=True))
        return adapter

    async def test_execute_success(self, manager, mock_adapter):
        """Test successful execution"""
        from helix.adapters.base import AIRequest

        config = EngineConfig(name="test", adapter=mock_adapter)
        manager.register_engine(config)

        # Set engine as available
        manager._health["test"].status = EngineStatus.AVAILABLE

        request = AIRequest(prompt="test")
        response = await manager.execute(request)

        assert response.success is True
        assert mock_adapter.execute.called

    async def test_execute_no_engine(self, manager):
        """Test execution with no available engine"""
        from helix.adapters.base import AIRequest

        request = AIRequest(prompt="test")
        response = await manager.execute(request)

        assert response.success is False
        assert "No available AI engine" in response.error


class TestGetEngineManager:
    """Test global engine manager"""

    def test_get_engine_manager_singleton(self):
        """Test singleton pattern"""
        manager1 = get_engine_manager()
        manager2 = get_engine_manager()
        assert manager1 is manager2