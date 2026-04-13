"""Test Plugin Base Classes"""

import pytest
from datetime import datetime
from helix.plugins.base import (
    Plugin,
    PluginStatus,
    PluginType,
    PluginMetadata,
    PluginConfig,
)


class TestPluginStatus:
    """Test PluginStatus enum"""

    def test_plugin_status_values(self):
        """Test enum values"""
        assert PluginStatus.UNLOADED.value == "unloaded"
        assert PluginStatus.LOADED.value == "loaded"
        assert PluginStatus.INITIALIZED.value == "initialized"
        assert PluginStatus.ACTIVE.value == "active"
        assert PluginStatus.ERROR.value == "error"
        assert PluginStatus.DISABLED.value == "disabled"


class TestPluginType:
    """Test PluginType enum"""

    def test_plugin_type_values(self):
        """Test enum values"""
        assert PluginType.SKILL.value == "skill"
        assert PluginType.ADAPTER.value == "adapter"
        assert PluginType.INTEGRATION.value == "integration"
        assert PluginType.THEME.value == "theme"
        assert PluginType.EXTENSION.value == "extension"


class TestPluginMetadata:
    """Test PluginMetadata dataclass"""

    def test_metadata_creation(self):
        """Test creating metadata"""
        metadata = PluginMetadata(
            name="test-plugin",
            version="1.0.0",
            description="A test plugin"
        )
        assert metadata.name == "test-plugin"
        assert metadata.version == "1.0.0"
        assert metadata.description == "A test plugin"
        assert metadata.author == ""
        assert metadata.license == "MIT"

    def test_metadata_with_all_fields(self):
        """Test metadata with all fields"""
        metadata = PluginMetadata(
            name="test-plugin",
            version="1.0.0",
            description="A test plugin",
            author="Test Author",
            author_email="test@example.com",
            license="MIT",
            homepage="https://example.com",
            repository="https://github.com/test/plugin",
            keywords=["test", "plugin"],
            dependencies=["helix-core"]
        )
        assert metadata.author == "Test Author"
        assert metadata.author_email == "test@example.com"
        assert metadata.homepage == "https://example.com"
        assert "test" in metadata.keywords
        assert "helix-core" in metadata.dependencies


class TestPluginConfig:
    """Test PluginConfig dataclass"""

    def test_config_creation(self):
        """Test creating config"""
        config = PluginConfig()
        assert config.enabled is True
        assert config.priority == 100
        assert config.config == {}
        assert config.secrets == {}

    def test_config_with_values(self):
        """Test config with custom values"""
        config = PluginConfig(
            enabled=False,
            priority=50,
            config={"key": "value"},
            secrets={"api_key": "secret"}
        )
        assert config.enabled is False
        assert config.priority == 50
        assert config.config["key"] == "value"
        assert config.secrets["api_key"] == "secret"


class TestPlugin:
    """Test Plugin base class"""

    @pytest.fixture
    def metadata(self):
        return PluginMetadata(
            name="test-plugin",
            version="1.0.0",
            description="Test plugin"
        )

    @pytest.fixture
    def config(self):
        return PluginConfig(enabled=True, priority=100)

    @pytest.fixture
    def plugin(self, metadata, config):
        """Create a concrete plugin for testing"""
        class TestPlugin(Plugin):
            metadata = PluginMetadata(
                name="test-plugin",
                version="1.0.0",
                description="Test plugin"
            )
            plugin_type = PluginType.SKILL

            def _do_initialize(self):
                self._initialized = True
                self._status = PluginStatus.INITIALIZED

            def _do_activate(self):
                self._status = PluginStatus.ACTIVE

            def _do_deactivate(self):
                self._status = PluginStatus.INITIALIZED

            def cleanup(self):
                self._status = PluginStatus.UNLOADED

        return TestPlugin(config)

    def test_plugin_init(self, plugin, metadata):
        """Test plugin initialization"""
        assert plugin.name == "test-plugin"
        assert plugin.config.enabled is True
        assert plugin.status == PluginStatus.UNLOADED
        assert plugin._initialized is False

    def test_plugin_properties(self, plugin):
        """Test plugin properties"""
        assert plugin.name == "test-plugin"
        assert plugin.plugin_type == PluginType.SKILL

    def test_plugin_initialize(self, plugin):
        """Test plugin initialization"""
        plugin.initialize()
        assert plugin._initialized is True
        assert plugin.status == PluginStatus.INITIALIZED

    def test_plugin_activate(self, plugin):
        """Test plugin activation"""
        plugin.initialize()
        plugin.activate()
        assert plugin.status == PluginStatus.ACTIVE

    def test_plugin_deactivate(self, plugin):
        """Test plugin deactivation"""
        plugin.initialize()
        plugin.activate()
        plugin.deactivate()
        assert plugin.status == PluginStatus.LOADED

    def test_plugin_cleanup(self, plugin):
        """Test plugin cleanup"""
        plugin.initialize()
        plugin.cleanup()
        assert plugin.status == PluginStatus.UNLOADED


class TestPluginStatusTransitions:
    """Test plugin status transitions"""

    def test_status_transitions(self):
        """Test valid status transitions"""
        # Create a minimal implementation for testing
        class TestPlugin(Plugin):
            plugin_type = PluginType.EXTENSION

        plugin = TestPlugin()

        # Initial state
        assert plugin.status == PluginStatus.UNLOADED

        # Simulate loading
        plugin._status = PluginStatus.LOADED
        assert plugin.status == PluginStatus.LOADED

        # Simulate initialization
        plugin._status = PluginStatus.INITIALIZED
        assert plugin.status == PluginStatus.INITIALIZED

        # Simulate activation
        plugin._status = PluginStatus.ACTIVE
        assert plugin.status == PluginStatus.ACTIVE

        # Simulate error
        plugin._status = PluginStatus.ERROR
        assert plugin.status == PluginStatus.ERROR

        # Simulate disabled
        plugin._status = PluginStatus.DISABLED
        assert plugin.status == PluginStatus.DISABLED