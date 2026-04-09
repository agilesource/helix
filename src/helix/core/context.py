"""
Helix 上下文管理模块

负责：
1. 会话历史管理
2. 项目状态跟踪
3. 跨会话记忆
4. 知识图谱
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional
from enum import Enum


class SessionState(Enum):
    """会话状态"""

    IDLE = "idle"
    RUNNING = "running"
    WAITING_CONFIRMATION = "waiting_confirmation"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class Interaction:
    """单次交互记录"""

    timestamp: datetime
    intent_type: str
    user_input: str
    skill_name: str
    result_success: bool
    result_message: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProjectState:
    """项目状态"""

    project_path: str
    project_type: str  # python, javascript, go, etc.
    framework: Optional[str] = None

    # Git 状态
    current_branch: Optional[str] = None
    is_dirty: bool = False

    # 代码统计
    lines_of_code: int = 0
    test_coverage: float = 0.0

    # 质量指标
    last_review_score: Optional[float] = None
    gate_level: int = 0  # 0-3 门禁等级


class HelixContext:
    """
    Helix 上下文管理器

    维护整个会话的状态信息
    """

    def __init__(self):
        self.session_id: str = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.session_state: SessionState = SessionState.IDLE
        self.started_at: datetime = datetime.now()

        # 当前项目
        self.project: Optional[ProjectState] = None

        # 交互历史
        self.interactions: List[Interaction] = []

        # 记忆（跨会话）
        self.memories: List[Dict[str, Any]] = []

        # 临时数据
        self.temp_data: Dict[str, Any] = {}

    def start_session(self, project_path: str) -> None:
        """开始新会话"""
        self.session_state = SessionState.RUNNING
        self.project = ProjectState(project_path=project_path, project_type="unknown")

    def add_interaction(
        self,
        intent,
        result,
    ) -> None:
        """记录交互"""
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

    def add_memory(self, memory_type: str, content: str, tags: List[str] = None) -> None:
        """添加记忆"""
        self.memories.append({
            "type": memory_type,
            "content": content,
            "tags": tags or [],
            "timestamp": datetime.now().isoformat(),
        })

    def get_recent_interactions(self, count: int = 10) -> List[Interaction]:
        """获取最近交互"""
        return self.interactions[-count:]

    def get_summary(self) -> Dict[str, Any]:
        """获取上下文摘要"""
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
