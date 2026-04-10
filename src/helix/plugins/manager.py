"""
Helix Plugin Manager

Manages plugin lifecycle: discovery, loading, activation, and deactivation
"""

import os
import importlib
import importlib.util
import json
from pathlib import Path
from typing import Dict, List, Optional, Type, Any
from dataclasses import dataclass, field
import logging

from helix.plugins.base import (
    Plugin, PluginConfig, PluginMetadata, PluginStatus, PluginType,
    SkillPlugin, AdapterPlugin, PluginResult
)

logger = logging.getLogger(__name__)


@dataclass
class PluginInfo:
    """Plugin information"""
    plugin_class: Type[Plugin]
    instance: Optional[Plugin] = None
    metadata: Optional[PluginMetadata] = None
    config: Optional[PluginConfig] = None
    status: PluginStatus = PluginStatus.UNLOADED
    error_message: str = ""


class PluginManager:
    """
    Plugin Manager

    Manages all plugins in the Helix system
    """

    def __init__(self, plugins_dir: Optional[str] = None):
        self._plugins: Dict[str, PluginInfo] = {}
        self._plugins_dir = plugins_dir or self._get_default_plugins_dir()
        self._enabled = True
        self._context = None

    def _get_default_plugins_dir(self) -> str:
        """Get default plugins directory"""
        # Check multiple locations
        possible_dirs = [
            Path.cwd() / "plugins",
            Path.home() / ".helix" / "plugins",
            Path(__file__).parent.parent.parent.parent / "plugins",
        ]

        for d in possible_dirs:
            if d.exists():
                return str(d)

        # Use first option if none exist
        return str(possible_dirs[0])

    def initialize(self, context: Any = None) -> None:
        """Initialize plugin manager"""
        self._context = context

        # Ensure plugins directory exists
        os.makedirs(self._plugins_dir, exist_ok=True)

        # Load built-in plugins
        self._load_builtin_plugins()

        # Discover and load plugins
        self.discover_plugins()

        logger.info(f"PluginManager initialized with {len(self._plugins)} plugins")

    def _load_builtin_plugins(self) -> None:
        """Load built-in plugins"""
        # Built-in plugins are registered here
        # They will be imported when needed
        pass

    def discover_plugins(self) -> List[str]:
        """Discover plugins in the plugins directory"""
        discovered = []

        plugins_path = Path(self._plugins_dir)
        if not plugins_path.exists():
            return discovered

        # Look for Python files
        for plugin_file in plugins_path.glob("*.py"):
            if plugin_file.name.startswith("_"):
                continue

            try:
                plugin_name = plugin_file.stem
                self._discover_plugin(plugin_name, str(plugin_file))
                discovered.append(plugin_name)
            except Exception as e:
                logger.error(f"Failed to discover plugin {plugin_file}: {e}")

        return discovered

    def _discover_plugin(self, name: str, file_path: str) -> None:
        """Discover a single plugin"""
        try:
            # Import the module
            spec = importlib.util.spec_from_file_location(name, file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Find plugin classes
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, Plugin) and attr != Plugin:
                        # Register plugin
                        self.register_plugin(name, attr)

        except Exception as e:
            logger.error(f"Failed to load plugin {name}: {e}")

    def register_plugin(self, name: str, plugin_class: Type[Plugin],
                       config: Optional[PluginConfig] = None) -> bool:
        """
        Register a plugin class

        Args:
            name: Plugin name
            plugin_class: Plugin class
            config: Plugin configuration

        Returns:
            True if successful
        """
        if name in self._plugins:
            logger.warning(f"Plugin {name} already registered")
            return False

        try:
            # Create instance
            instance = plugin_class(config)

            # Store plugin info
            self._plugins[name] = PluginInfo(
                plugin_class=plugin_class,
                instance=instance,
                metadata=instance.metadata,
                config=config or PluginConfig(),
                status=PluginStatus.LOADED,
            )

            logger.info(f"Registered plugin: {name}")
            return True

        except Exception as e:
            logger.error(f"Failed to register plugin {name}: {e}")
            self._plugins[name] = PluginInfo(
                plugin_class=plugin_class,
                error_message=str(e),
                status=PluginStatus.ERROR,
            )
            return False

    def load_plugin(self, name: str) -> bool:
        """
        Load and initialize a plugin

        Args:
            name: Plugin name

        Returns:
            True if successful
        """
        if name not in self._plugins:
            logger.error(f"Plugin {name} not found")
            return False

        plugin_info = self._plugins[name]

        if plugin_info.status != PluginStatus.LOADED:
            logger.warning(f"Plugin {name} not in LOADED state")
            return False

        try:
            # Initialize plugin
            plugin_info.instance.initialize(self._context)

            # Activate if enabled
            if plugin_info.config.enabled:
                plugin_info.instance.activate()

            plugin_info.status = PluginStatus.ACTIVE
            logger.info(f"Loaded plugin: {name}")
            return True

        except Exception as e:
            plugin_info.status = PluginStatus.ERROR
            plugin_info.error_message = str(e)
            logger.error(f"Failed to load plugin {name}: {e}")
            return False

    def unload_plugin(self, name: str) -> bool:
        """
        Unload a plugin

        Args:
            name: Plugin name

        Returns:
            True if successful
        """
        if name not in self._plugins:
            return False

        plugin_info = self._plugins[name]

        if plugin_info.instance:
            try:
                plugin_info.instance.shutdown()
                plugin_info.status = PluginStatus.UNLOADED
                logger.info(f"Unloaded plugin: {name}")
                return True
            except Exception as e:
                logger.error(f"Failed to unload plugin {name}: {e}")
                return False

        return False

    def enable_plugin(self, name: str) -> bool:
        """Enable a plugin"""
        if name not in self._plugins:
            return False

        plugin_info = self._plugins[name]
        plugin_info.config.enabled = True

        if plugin_info.status == PluginStatus.LOADED:
            return self.load_plugin(name)

        return True

    def disable_plugin(self, name: str) -> bool:
        """Disable a plugin"""
        if name not in self._plugins:
            return False

        plugin_info = self._plugins[name]
        plugin_info.config.enabled = False

        if plugin_info.status == PluginStatus.ACTIVE:
            return self.unload_plugin(name)

        return True

    def get_plugin(self, name: str) -> Optional[Plugin]:
        """Get plugin instance"""
        if name in self._plugins:
            return self._plugins[name].instance
        return None

    def get_all_plugins(self) -> List[Plugin]:
        """Get all loaded plugins"""
        return [
            pi.instance for pi in self._plugins.values()
            if pi.instance and pi.status == PluginStatus.ACTIVE
        ]

    def get_plugins_by_type(self, plugin_type: PluginType) -> List[Plugin]:
        """Get plugins by type"""
        return [
            pi.instance for pi in self._plugins.values()
            if pi.instance and pi.plugin_type == plugin_type
        ]

    def get_skill_plugins(self) -> List[SkillPlugin]:
        """Get all skill plugins"""
        return [p for p in self.get_plugins_by_type(PluginType.SKILL) if isinstance(p, SkillPlugin)]

    def get_adapter_plugins(self) -> List[AdapterPlugin]:
        """Get all adapter plugins"""
        return [p for p in self.get_plugins_by_type(PluginType.ADAPTER) if isinstance(p, AdapterPlugin)]

    def list_plugins(self) -> List[Dict[str, Any]]:
        """List all plugins"""
        return [
            {
                "name": name,
                "version": pi.metadata.version if pi.metadata else "unknown",
                "description": pi.metadata.description if pi.metadata else "",
                "status": pi.status.value,
                "enabled": pi.config.enabled if pi.config else False,
                "error": pi.error_message,
            }
            for name, pi in self._plugins.items()
        ]

    def shutdown(self) -> None:
        """Shutdown all plugins"""
        for name in list(self._plugins.keys()):
            self.unload_plugin(name)

        self._plugins.clear()
        logger.info("PluginManager shutdown complete")


# Global plugin manager instance
_plugin_manager: Optional[PluginManager] = None


def get_plugin_manager() -> PluginManager:
    """Get global plugin manager"""
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
    return _plugin_manager
