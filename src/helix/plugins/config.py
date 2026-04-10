"""
Helix Plugin Configuration

Manages plugin configuration including settings, secrets, and permissions
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field, asdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class PluginSettings:
    """Plugin settings"""
    enabled: bool = True
    priority: int = 100
    auto_load: bool = True
    permissions: Dict[str, bool] = field(default_factory=dict)


class PluginConfigManager:
    """
    Plugin Configuration Manager

    Handles plugin configuration loading, saving, and validation
    """

    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = config_dir or self._get_default_config_dir()
        self._config: Dict[str, PluginSettings] = {}
        self._load_config()

    def _get_default_config_dir(self) -> str:
        """Get default config directory"""
        return str(Path.home() / ".helix" / "config")

    def _load_config(self) -> None:
        """Load plugin configuration"""
        config_file = Path(self.config_dir) / "plugins.json"

        if not config_file.exists():
            return

        try:
            with open(config_file, "r") as f:
                data = json.load(f)
                for name, settings in data.items():
                    self._config[name] = PluginSettings(**settings)
        except Exception as e:
            logger.error(f"Failed to load plugin config: {e}")

    def save_config(self) -> None:
        """Save plugin configuration"""
        config_file = Path(self.config_dir) / "plugins.json"
        config_file.parent.mkdir(parents=True, exist_ok=True)

        data = {
            name: asdict(settings)
            for name, settings in self._config.items()
        }

        with open(config_file, "w") as f:
            json.dump(data, f, indent=2)

    def get_settings(self, plugin_name: str) -> PluginSettings:
        """Get plugin settings"""
        if plugin_name not in self._config:
            self._config[plugin_name] = PluginSettings()
        return self._config[plugin_name]

    def set_enabled(self, plugin_name: str, enabled: bool) -> None:
        """Enable or disable a plugin"""
        settings = self.get_settings(plugin_name)
        settings.enabled = enabled
        self.save_config()

    def set_priority(self, plugin_name: str, priority: int) -> None:
        """Set plugin priority"""
        settings = self.get_settings(plugin_name)
        settings.priority = priority
        self.save_config()

    def set_permission(self, plugin_name: str, permission: str, granted: bool) -> None:
        """Set plugin permission"""
        settings = self.get_settings(plugin_name)
        settings.permissions[permission] = granted
        self.save_config()

    def is_enabled(self, plugin_name: str) -> bool:
        """Check if plugin is enabled"""
        return self.get_settings(plugin_name).enabled

    def is_auto_load(self, plugin_name: str) -> bool:
        """Check if plugin should auto-load"""
        return self.get_settings(plugin_name).auto_load

    def has_permission(self, plugin_name: str, permission: str) -> bool:
        """Check if plugin has permission"""
        return self.get_settings(plugin_name).permissions.get(permission, False)

    def list_enabled(self) -> list:
        """List enabled plugins"""
        return [
            name for name, settings in self._config.items()
            if settings.enabled
        ]

    def reset(self) -> None:
        """Reset all configuration"""
        self._config.clear()
        self.save_config()


# Global config manager instance
_config_manager: Optional[PluginConfigManager] = None


def get_config_manager() -> PluginConfigManager:
    """Get global config manager"""
    global _config_manager
    if _config_manager is None:
        _config_manager = PluginConfigManager()
    return _config_manager
