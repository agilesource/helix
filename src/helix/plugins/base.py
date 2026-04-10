"""
Helix Plugin Base Classes

All plugins must inherit from the Plugin base class
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum


class PluginStatus(Enum):
    """Plugin status"""
    UNLOADED = "unloaded"
    LOADED = "loaded"
    INITIALIZED = "initialized"
    ACTIVE = "active"
    ERROR = "error"
    DISABLED = "disabled"


class PluginType(Enum):
    """Plugin types"""
    SKILL = "skill"           # Adds new skills
    ADAPTER = "adapter"       # AI engine adapters
    INTEGRATION = "integration"  # Third-party integrations
    THEME = "theme"           # UI themes
    EXTENSION = "extension"   # General extensions


@dataclass
class PluginMetadata:
    """Plugin metadata"""
    name: str
    version: str
    description: str
    author: str = ""
    author_email: str = ""
    license: str = "MIT"
    homepage: str = ""
    repository: str = ""
    keywords: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class PluginConfig:
    """Plugin configuration"""
    enabled: bool = True
    priority: int = 100  # Lower = higher priority
    config: Dict[str, Any] = field(default_factory=dict)
    secrets: Dict[str, str] = field(default_factory=dict)  # Encrypted


class Plugin(ABC):
    """
    Base Plugin Class

    All Helix plugins must inherit from this class
    """

    # Class attributes - subclasses must override
    metadata: PluginMetadata
    plugin_type: PluginType = PluginType.EXTENSION

    def __init__(self, config: Optional[PluginConfig] = None):
        self.config = config or PluginConfig()
        self._status = PluginStatus.UNLOADED
        self._initialized = False
        self._context = None

    @property
    def name(self) -> str:
        return self.metadata.name

    @property
    def version(self) -> str:
        return self.metadata.version

    @property
    def status(self) -> PluginStatus:
        return self._status

    def initialize(self, context: Any = None) -> None:
        """
        Initialize the plugin

        Args:
            context: Helix context or other shared context
        """
        if self._initialized:
            return

        self._context = context
        self._do_initialize()
        self._initialized = True
        self._status = PluginStatus.INITIALIZED

    def _do_initialize(self) -> None:
        """
        Custom initialization logic

        Override in subclasses
        """
        pass

    def activate(self) -> None:
        """
        Activate the plugin

        Called when plugin is loaded and ready to use
        """
        if not self._initialized:
            self.initialize()

        self._do_activate()
        self._status = PluginStatus.ACTIVE

    def _do_activate(self) -> None:
        """
        Custom activation logic

        Override in subclasses
        """
        pass

    def deactivate(self) -> None:
        """
        Deactivate the plugin

        Called when plugin is unloaded
        """
        self._do_deactivate()
        self._status = PluginStatus.LOADED

    def _do_deactivate(self) -> None:
        """
        Custom deactivation logic

        Override in subclasses
        """
        pass

    def shutdown(self) -> None:
        """
        Shutdown the plugin

        Called when Helix is shutting down
        """
        self._do_shutdown()
        self._status = PluginStatus.UNLOADED

    def _do_shutdown(self) -> None:
        """
        Custom shutdown logic

        Override in subclasses
        """
        pass

    def get_info(self) -> Dict[str, Any]:
        """Get plugin info"""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.metadata.description,
            "type": self.plugin_type.value,
            "status": self._status.value,
            "author": self.metadata.author,
        }

    def validate_config(self) -> tuple[bool, str]:
        """
        Validate plugin configuration

        Returns:
            (is_valid, error_message)
        """
        return True, ""

    def __repr__(self) -> str:
        return f"<Plugin {self.name} v{self.version} ({self._status.value})>"


class SkillPlugin(Plugin):
    """
    Skill Plugin

    A plugin that adds new skills to Helix
    """

    plugin_type = PluginType.SKILL

    @abstractmethod
    def get_skill_class(self):
        """Return the skill class this plugin provides"""
        pass


class AdapterPlugin(Plugin):
    """
    Adapter Plugin

    A plugin that adds new AI engine adapters
    """

    plugin_type = PluginType.ADAPTER

    @abstractmethod
    def get_adapter_class(self):
        """Return the adapter class this plugin provides"""
        pass


# Plugin result
@dataclass
class PluginResult:
    """Plugin execution result"""
    success: bool
    data: Dict[str, Any] = field(default_factory=dict)
    message: str = ""
    errors: List[str] = field(default_factory=list)
