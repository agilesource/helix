"""
Helix 意图识别模块
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, Optional


class IntentType(Enum):
    """意图类型枚举"""

    # 执行层
    SPEC = "spec"  # 规格说明
    BUILD = "build"  # 代码构建
    VERIFY = "verify"  # 验证测试
    SHIP = "ship"  # 发布交付

    # 质量层
    REVIEW = "review"  # 代码审查
    TEST = "test"  # 智能测试
    AUDIT = "audit"  # 安全审计
    GATE = "gate"  # 质量门禁

    # 基础设施层
    DESIGN = "design"  # 设计生成
    LEARN = "learn"  # 持续学习
    CHECKPOINT = "checkpoint"  # 状态保存

    # 其他
    GENERAL = "general"  # 通用对话
    HELP = "help"  # 帮助


@dataclass
class Intent:
    """用户意图"""

    type: IntentType
    raw_input: str
    confidence: float  # 0-1 置信度

    # 解析后的结构化信息
    entities: Dict[str, Any] = field(default_factory=dict)
    parameters: Dict[str, Any] = field(default_factory=dict)

    # 上下文信息
    context_window: Optional[str] = None  # 上下文窗口标识
    related_intents: list = field(default_factory=list)  # 关联意图

    def __post_init__(self):
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")

    @property
    def is_clear(self) -> bool:
        """意图是否足够清晰"""
        return self.confidence >= 0.7

    def add_entity(self, key: str, value: Any) -> None:
        """添加实体"""
        self.entities[key] = value

    def set_parameter(self, key: str, value: Any) -> None:
        """设置参数"""
        self.parameters[key] = value
