"""
Helix Context Management Module

Responsibilities:
1. Session history management
2. Project state tracking
3. Cross-session memory
4. Knowledge graph
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional
from enum import Enum


class SessionState(Enum):
    """Session state"""

    IDLE = "idle"
    RUNNING = "running"
    WAITING_CONFIRMATION = "waiting_confirmation"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class Interaction:
    """Single interaction record"""

    timestamp: datetime
    intent_type: str
    user_input: str
    skill_name: str
    result_success: bool
    result_message: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProjectState:
    """Project state"""

    project_path: str
    project_type: str  # python, javascript, go, etc.
    framework: Optional[str] = None

    # Git state
    current_branch: Optional[str] = None
    is_dirty: bool = False

    # Code statistics
    lines_of_code: int = 0
    test_coverage: float = 0.0

    # Quality metrics
    last_review_score: Optional[float] = None
    gate_level: int = 0  # 0-3 gate level


class HelixContext:
    """
    Helix Context Manager

    Maintains state information for the entire session.
    """

    def __init__(self):
        self.session_id: str = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.session_state: SessionState = SessionState.IDLE
        self.started_at: datetime = datetime.now()

        # Current project
        self.project: Optional[ProjectState] = None

        # Interaction history
        self.interactions: List[Interaction] = []

        # Memory (cross-session)
        self.memories: List[Dict[str, Any]] = []

        # Temporary data
        self.temp_data: Dict[str, Any] = {}

    def start_session(self, project_path: str) -> None:
        """Start new session"""
        self.session_state = SessionState.RUNNING
        self.project = ProjectState(project_path=project_path, project_type="unknown")

    def add_interaction(
        self,
        intent,
        result,
    ) -> None:
        """Record interaction"""
        interaction = Interaction(
            timestamp=datetime.now(),
            intent_type=intent.type.value,
            user_input=intent.raw_input,
            skill_name=result.skill_name if hasattr(result, "skill_name") else "unknown",
            result_success=result.success,
            result_message=result.message,
            metadata=result.data if hasattr(result, "data") else {},
        )
        self.interactions.append(interaction)

    def add_memory(self, memory_type: str, content: str, tags: Optional[List[str]] = None) -> None:
        """Add memory"""
        self.memories.append({
            "type": memory_type,
            "content": content,
            "tags": tags or [],
            "timestamp": datetime.now().isoformat(),
        })

    def get_recent_interactions(self, count: int = 10) -> List[Interaction]:
        """Get recent interactions"""
        return self.interactions[-count:]

    def get_summary(self) -> Dict[str, Any]:
        """Get context summary"""
        return {
            "session_id": self.session_id,
            "state": self.session_state.value,
            "duration_seconds": (datetime.now() - self.started_at).total_seconds(),
            "interaction_count": len(self.interactions),
            "memory_count": len(self.memories),
            "project": {
                "path": self.project.project_path if self.project else None,
                "type": self.project.project_type if self.project else None,
            } if self.project else None,
        }
