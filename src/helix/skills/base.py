"""
Helix Skill Base Classes

All skills must inherit from this base class
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum


class SkillCategory(Enum):
    """Skill Category"""

    INFRASTRUCTURE = "infrastructure"
    EXECUTION = "execution"
    QUALITY = "quality"
    META = "meta"


class SkillStatus(Enum):
    """Skill Status"""

    DRAFT = "draft"
    BETA = "beta"
    EXPERIMENTAL = "experimental"
    STABLE = "stable"
    DEPRECATED = "deprecated"


@dataclass
class SkillResult:
    """Skill Execution Result"""

    success: bool
    message: str
    data: Dict[str, Any] = field(default_factory=dict)

    # Additional info
    skill_name: str = ""
    execution_time_ms: int = 0
    artifacts: Dict[str, str] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


@dataclass
class SkillConfig:
    """Skill Configuration"""

    auto_confirm: bool = False
    timeout_seconds: int = 300
    max_retries: int = 3
    verbose: bool = False


class Skill(ABC):
    """
    Skill Base Class

    All Helix skills must inherit from this class and implement execute method
    """

    # Class attributes - subclasses must override
    name: str = ""
    description: str = ""
    category: SkillCategory = SkillCategory.EXECUTION
    status: SkillStatus = SkillStatus.DRAFT

    # Usage examples
    examples: List[str] = []

    def __init__(self, config: Optional[SkillConfig] = None):
        self.config = config or SkillConfig()
        self._initialized = False

    def initialize(self) -> None:
        """Initialize skill"""
        if not self._initialized:
            self._do_initialize()
            self._initialized = True

    def _do_initialize(self) -> None:
        """Subclasses can implement custom initialization"""
        pass

    @abstractmethod
    async def execute(self, intent, context) -> SkillResult:
        """
        Execute skill

        Args:
            intent: Parsed user intent
            context: Helix context

        Returns:
            SkillResult: Execution result
        """
        pass

    async def validate(self, intent, context) -> tuple[bool, str]:
        """
        Validate input

        Returns:
            (is_valid, error_message)
        """
        # Default: always valid
        return True, ""

    def get_usage(self) -> str:
        """Get usage instructions"""
        lines = [
            f"## {self.name}",
            f"",
            f"{self.description}",
            f"",
            f"**Category**: {self.category.value}",
            f"**Status**: {self.status.value}",
            f"",
        ]

        if self.examples:
            lines.append("**Examples**:")
            for example in self.examples:
                lines.append(f"```\n{self.name} {example}\n```")

        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"<Skill {self.name} ({self.status.value})>"
