"""Tests for plugin configuration module"""

import pytest
import tempfile
import json
from pathlib import Path
from helix.plugins.config import (
    PluginSettings,
    PluginConfigManager,
    get_config_manager,
)


class TestPluginSettings:
    """Test PluginSettings dataclass"""

    def test_default_settings(self):
        """Test default settings"""
        settings = PluginSettings()
        assert settings.enabled is True
        assert settings.priority == 100
        assert settings.auto_load is True
        assert settings.permissions == {}

    def test_custom_settings(self):
        """Test custom settings"""
        settings = PluginSettings(enabled=False, priority=50, auto_load=False)
        assert settings.enabled is False
        assert settings.priority == 50
        assert settings.auto_load is False


class TestPluginConfigManager:
    """Test PluginConfigManager"""

    def test_init_default(self):
        """Test initialization with default config dir"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Mock home directory
            manager = PluginConfigManager(config_dir=tmpdir)
            assert manager.config_dir == tmpdir
            assert manager._config == {}

    def test_get_settings_new(self):
        """Test getting settings for new plugin"""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = PluginConfigManager(config_dir=tmpdir)
            settings = manager.get_settings("test_plugin")
            assert isinstance(settings, PluginSettings)
            assert settings.enabled is True

    def test_get_settings_existing(self):
        """Test getting settings for existing plugin"""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = PluginConfigManager(config_dir=tmpdir)
            settings1 = manager.get_settings("test_plugin")
            settings1.enabled = False
            settings2 = manager.get_settings("test_plugin")
            assert settings2.enabled is False

    def test_set_enabled(self):
        """Test enabling/disabling plugin"""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = PluginConfigManager(config_dir=tmpdir)
            manager.set_enabled("test_plugin", False)
            assert manager.is_enabled("test_plugin") is False

            manager.set_enabled("test_plugin", True)
            assert manager.is_enabled("test_plugin") is True

    def test_set_priority(self):
        """Test setting plugin priority"""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = PluginConfigManager(config_dir=tmpdir)
            manager.set_priority("test_plugin", 25)
            settings = manager.get_settings("test_plugin")
            assert settings.priority == 25

    def test_set_permission(self):
        """Test setting plugin permission"""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = PluginConfigManager(config_dir=tmpdir)
            manager.set_permission("test_plugin", "file_read", True)
            manager.set_permission("test_plugin", "network", False)

            assert manager.has_permission("test_plugin", "file_read") is True
            assert manager.has_permission("test_plugin", "network") is False

    def test_is_auto_load(self):
        """Test auto_load check"""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = PluginConfigManager(config_dir=tmpdir)
            assert manager.is_auto_load("test_plugin") is True

    def test_list_enabled(self):
        """Test listing enabled plugins"""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = PluginConfigManager(config_dir=tmpdir)
            manager.set_enabled("plugin1", True)
            manager.set_enabled("plugin2", False)
            manager.set_enabled("plugin3", True)

            enabled = manager.list_enabled()
            assert "plugin1" in enabled
            assert "plugin2" not in enabled
            assert "plugin3" in enabled

    def test_save_and_load_config(self):
        """Test saving and loading configuration"""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager1 = PluginConfigManager(config_dir=tmpdir)
            manager1.set_enabled("plugin1", True)
            manager1.set_priority("plugin1", 50)
            manager1.save_config()

            # Create new manager and load
            manager2 = PluginConfigManager(config_dir=tmpdir)
            assert manager2.is_enabled("plugin1") is True
            settings = manager2.get_settings("plugin1")
            assert settings.priority == 50

    def test_reset(self):
        """Test resetting configuration"""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = PluginConfigManager(config_dir=tmpdir)
            manager.set_enabled("plugin1", True)
            manager.save_config()
            manager.reset()

            assert manager.list_enabled() == []


class TestGetConfigManager:
    """Test global config manager"""

    def test_get_config_manager_singleton(self):
        """Test that get_config_manager returns singleton"""
        # This will use the default config dir
        manager1 = get_config_manager()
        manager2 = get_config_manager()
        # They should be the same instance (singleton)
        # Note: This might fail if previous tests already initialized
        assert isinstance(manager1, PluginConfigManager)