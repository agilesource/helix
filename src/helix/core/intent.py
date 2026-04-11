"""
Helix Intent Recognition Module
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, Optional


class IntentType(Enum):
    """Intent type enumeration"""

    # Execution layer
    SPEC = "spec"  # Specification
    BUILD = "build"  # Code build
    VERIFY = "verify"  # Verification test
    SHIP = "ship"  # Release delivery

    # Quality layer
    REVIEW = "review"  # Code review
    TEST = "test"  # Smart test
    AUDIT = "audit"  # Security audit
    GATE = "gate"  # Quality gate

    # Infrastructure layer
    BROWSE = "browse"  # Browser control
    DESIGN = "design"  # Design generation
    LEARN = "learn"  # Continuous learning
    CHECKPOINT = "checkpoint"  # State save

    # Others
    GENERAL = "general"  # General conversation
    HELP = "help"  # Help


@dataclass
class Intent:
    """User intent"""

    type: IntentType
    raw_input: str
    confidence: float  # 0-1 confidence

    # Parsed structured information
    entities: Dict[str, Any] = field(default_factory=dict)
    parameters: Dict[str, Any] = field(default_factory=dict)

    # Context information
    context_window: Optional[str] = None  # Context window identifier
    related_intents: list = field(default_factory=list)  # Related intents

    def __post_init__(self):
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")

    @property
    def is_clear(self) -> bool:
        """Whether intent is clear enough"""
        return self.confidence >= 0.7

    def add_entity(self, key: str, value: Any) -> None:
        """Add entity"""
        self.entities[key] = value

    def set_parameter(self, key: str, value: Any) -> None:
        """Set parameter"""
        self.parameters[key] = value
