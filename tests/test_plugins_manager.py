"""Test Plugin Manager"""

import pytest
from helix.plugins.manager import PluginManager
from helix.plugins.base import PluginConfig, PluginMetadata, PluginType, PluginStatus


class TestPluginManager:
    """Test PluginManager"""

    @pytest.fixture
    def manager(self):
        return PluginManager()

    def test_manager_init(self, manager):
        """Test manager initialization"""
        assert manager is not None

    def test_manager_plugins_dict(self, manager):
        """Test plugins dictionary exists"""
        assert hasattr(manager, '_plugins')


class TestPluginMetadata:
    """Test PluginMetadata"""

    def test_metadata_with_all_fields(self):
        """Test metadata with all fields"""
        metadata = PluginMetadata(
            name="test-plugin",
            version="1.0.0",
            description="Test plugin",
            author="Test Author",
            keywords=["test", "plugin"]
        )
        assert metadata.name == "test-plugin"
        assert metadata.author == "Test Author"
        assert "test" in metadata.keywords


class TestPluginConfig:
    """Test PluginConfig"""

    def test_config_defaults(self):
        """Test config default values"""
        config = PluginConfig()
        assert config.enabled is True
        assert config.priority == 100