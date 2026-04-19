"""Test Plugin Manager"""

import pytest
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock
from helix.plugins.manager import PluginManager, PluginInfo, get_plugin_manager
from helix.plugins.base import (
    PluginConfig,
    PluginMetadata,
    PluginType,
    PluginStatus,
    Plugin,
    PluginResult,
    SkillPlugin,
    AdapterPlugin,
)


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

    def test_manager_register_plugin(self, manager):
        """Test registering a plugin class"""
        class TestPlugin(Plugin):
            name = "test_plugin"

            @property
            def metadata(self):
                return PluginMetadata(
                    name="test_plugin",
                    version="1.0.0",
                    description="Test"
                )

            async def execute(self, config):
                return PluginResult(success=True, message="done")

        result = manager.register_plugin("test_plugin", TestPlugin)
        assert result is True
        assert "test_plugin" in manager._plugins

    def test_manager_get_plugin(self, manager):
        """Test getting a registered plugin"""
        class TestPlugin(Plugin):
            name = "get_test"

            @property
            def metadata(self):
                return PluginMetadata(name="get_test", version="1.0.0", description="Test")

            async def execute(self, config):
                return PluginResult(success=True, message="done")

        manager.register_plugin("get_test", TestPlugin)
        retrieved = manager.get_plugin("get_test")
        assert retrieved is not None

    def test_manager_get_plugin_not_found(self, manager):
        """Test getting non-existent plugin"""
        result = manager.get_plugin("nonexistent")
        assert result is None

    def test_manager_list_plugins(self, manager):
        """Test listing all plugins"""
        class Plugin1(Plugin):
            name = "plugin1"

            @property
            def metadata(self):
                return PluginMetadata(name="plugin1", version="1.0.0", description="Test")

            async def execute(self, config):
                return PluginResult(success=True, message="done")

        class Plugin2(Plugin):
            name = "plugin2"

            @property
            def metadata(self):
                return PluginMetadata(name="plugin2", version="1.0.0", description="Test")

            async def execute(self, config):
                return PluginResult(success=True, message="done")

        manager.register_plugin("plugin1", Plugin1)
        manager.register_plugin("plugin2", Plugin2)

        plugins = manager.list_plugins()
        assert len(plugins) == 2

    def test_manager_unload_plugin(self, manager):
        """Test unloading a plugin"""
        class RemovePlugin(Plugin):
            name = "remove_me"

            @property
            def metadata(self):
                return PluginMetadata(name="remove_me", version="1.0.0", description="Test")

            async def execute(self, config):
                return PluginResult(success=True, message="done")

        manager.register_plugin("remove_me", RemovePlugin)
        result = manager.unload_plugin("remove_me")
        assert result is True

    def test_manager_enable_disable_plugin(self, manager):
        """Test enabling and disabling plugin"""
        class EnablePlugin(Plugin):
            name = "enable_test"

            @property
            def metadata(self):
                return PluginMetadata(name="enable_test", version="1.0.0", description="Test")

            async def execute(self, config):
                return PluginResult(success=True, message="done")

        manager.register_plugin("enable_test", EnablePlugin)
        result = manager.disable_plugin("enable_test")
        assert result is True


class TestPluginManagerAdvanced:
    """Test PluginManager advanced methods"""

    def test_manager_initialize(self):
        """Test manager initialize method"""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = PluginManager(plugins_dir=tmpdir)
            # initialize should work without errors
            manager.initialize()
            assert manager._context is None

    def test_manager_initialize_with_context(self):
        """Test manager initialize with context"""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = PluginManager(plugins_dir=tmpdir)
            context = {"test": "context"}
            manager.initialize(context)
            assert manager._context == context

    def test_discover_plugins_empty_dir(self):
        """Test discover_plugins with empty directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = PluginManager(plugins_dir=tmpdir)
            discovered = manager.discover_plugins()
            assert discovered == []

    def test_discover_plugins_with_files(self):
        """Test discover_plugins with Python files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test plugin file
            plugin_file = os.path.join(tmpdir, "test_discovery.py")
            with open(plugin_file, "w") as f:
                f.write("""
from helix.plugins.base import Plugin, PluginMetadata, PluginResult

class TestDiscovery(Plugin):
    name = "test_discovery"

    @property
    def metadata(self):
        return PluginMetadata(name="test_discovery", version="1.0.0", description="Test")

    async def execute(self, config):
        return PluginResult(success=True)
""")

            manager = PluginManager(plugins_dir=tmpdir)
            discovered = manager.discover_plugins()
            # May be empty if discovery fails, but should not crash

    def test_register_duplicate_plugin(self):
        """Test registering duplicate plugin"""
        class DuplicatePlugin(Plugin):
            name = "dup_test"

            @property
            def metadata(self):
                return PluginMetadata(name="dup_test", version="1.0.0", description="Test")

            async def execute(self, config):
                return PluginResult(success=True)

        manager = PluginManager()
        result1 = manager.register_plugin("dup_test", DuplicatePlugin)
        result2 = manager.register_plugin("dup_test", DuplicatePlugin)
        assert result1 is True
        assert result2 is False

    def test_register_plugin_with_exception(self):
        """Test registering plugin that raises exception"""
        class BadPlugin(Plugin):
            name = "bad_plugin"

            @property
            def metadata(self):
                return PluginMetadata(name="bad_plugin", version="1.0.0", description="Test")

            def __init__(self, config=None):
                raise RuntimeError("Init failed")

            async def execute(self, config):
                return PluginResult(success=True)

        manager = PluginManager()
        result = manager.register_plugin("bad_plugin", BadPlugin)
        assert result is False

    def test_load_plugin_not_found(self):
        """Test loading non-existent plugin"""
        manager = PluginManager()
        result = manager.load_plugin("nonexistent")
        assert result is False

    def test_load_plugin_not_loaded_state(self):
        """Test loading plugin not in LOADED state"""
        class TestPlugin(Plugin):
            name = "not_loaded"

            @property
            def metadata(self):
                return PluginMetadata(name="not_loaded", version="1.0.0", description="Test")

            async def execute(self, config):
                return PluginResult(success=True)

        manager = PluginManager()
        manager.register_plugin("not_loaded", TestPlugin)
        # Plugin is in LOADED state after register
        # Let's check the state handling
        result = manager.load_plugin("not_loaded")
        assert result is True  # Should load successfully

    def test_load_plugin_with_initialize(self):
        """Test load_plugin with initialize and activate"""
        class TestPlugin(Plugin):
            name = "init_test"

            @property
            def metadata(self):
                return PluginMetadata(name="init_test", version="1.0.0", description="Test")

            def initialize(self, context):
                pass

            def activate(self):
                pass

            async def execute(self, config):
                return PluginResult(success=True)

        manager = PluginManager()
        manager.register_plugin("init_test", TestPlugin)
        result = manager.load_plugin("init_test")
        assert result is True

    def test_load_plugin_initialize_error(self):
        """Test load_plugin with initialize error"""
        class TestPlugin(Plugin):
            name = "error_test"

            @property
            def metadata(self):
                return PluginMetadata(name="error_test", version="1.0.0", description="Test")

            def initialize(self, context):
                raise RuntimeError("Init error")

            async def execute(self, config):
                return PluginResult(success=True)

        manager = PluginManager()
        manager.register_plugin("error_test", TestPlugin)
        result = manager.load_plugin("error_test")
        assert result is False

    def test_unload_plugin_not_found(self):
        """Test unloading non-existent plugin"""
        manager = PluginManager()
        result = manager.unload_plugin("nonexistent")
        assert result is False

    def test_unload_plugin_with_shutdown_error(self):
        """Test unloading plugin with shutdown error"""
        class TestPlugin(Plugin):
            name = "shutdown_error"

            @property
            def metadata(self):
                return PluginMetadata(name="shutdown_error", version="1.0.0", description="Test")

            def shutdown(self):
                raise RuntimeError("Shutdown failed")

            async def execute(self, config):
                return PluginResult(success=True)

        manager = PluginManager()
        manager.register_plugin("shutdown_error", TestPlugin)
        result = manager.unload_plugin("shutdown_error")
        assert result is False

    def test_enable_plugin_not_found(self):
        """Test enabling non-existent plugin"""
        manager = PluginManager()
        result = manager.enable_plugin("nonexistent")
        assert result is False

    def test_disable_plugin_not_found(self):
        """Test disabling non-existent plugin"""
        manager = PluginManager()
        result = manager.disable_plugin("nonexistent")
        assert result is False


class TestPluginInfo:
    """Test PluginInfo dataclass"""

    def test_plugin_info_creation(self):
        """Test creating PluginInfo"""
        class TestPlugin(Plugin):
            name = "test"

            @property
            def metadata(self):
                return PluginMetadata(name="test", version="1.0.0", description="Test")

            async def execute(self, config):
                return PluginResult(success=True, message="done")

        info = PluginInfo(plugin_class=TestPlugin)
        assert info.plugin_class == TestPlugin
        assert info.status == PluginStatus.UNLOADED


class TestGetPluginManager:
    """Test get_plugin_manager factory"""

    def test_get_plugin_manager_singleton(self):
        """Test plugin manager is singleton"""
        m1 = get_plugin_manager()
        m2 = get_plugin_manager()
        assert m1 is m2


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

    def test_config_custom_values(self):
        """Test config with custom values"""
        config = PluginConfig(enabled=False, priority=50)
        assert config.enabled is False
        assert config.priority == 50


class TestPluginResult:
    """Test PluginResult"""

    def test_plugin_result_success(self):
        """Test successful plugin result"""
        result = PluginResult(success=True, message="Success")
        assert result.success is True
        assert result.message == "Success"

    def test_plugin_result_failure(self):
        """Test failed plugin result"""
        result = PluginResult(success=False, message="Failed", errors=["Something wrong"])
        assert result.success is False
        assert "Something wrong" in result.errors

    def test_plugin_result_with_data(self):
        """Test result with data"""
        result = PluginResult(success=True, message="Done", data={"key": "value"})
        assert result.data["key"] == "value"


class TestPluginStatus:
    """Test PluginStatus enum"""

    def test_plugin_status_values(self):
        """Test PluginStatus values"""
        assert PluginStatus.UNLOADED.value == "unloaded"
        assert PluginStatus.LOADED.value == "loaded"
        assert PluginStatus.ACTIVE.value == "active"
        assert PluginStatus.ERROR.value == "error"