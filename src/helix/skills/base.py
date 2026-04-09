"""
Helix 技能基类

所有技能都必须继承这个基类
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum


class SkillCategory(Enum):
    """技能分类"""

    INFRASTRUCTURE = "infrastructure"  # 基础设施
    EXECUTION = "execution"  # 执行引擎
    QUALITY = "quality"  # 质量保障
    META = "meta"  # 元技能


class SkillStatus(Enum):
    """技能状态"""

    DRAFT = "draft"  # 设计中
    EXPERIMENTAL = "experimental"  # 实验中
    STABLE = "stable"  # 稳定
    DEPRECATED = "deprecated"  # 已废弃


@dataclass
class SkillResult:
    """技能执行结果"""

    success: bool
    message: str
    data: Dict[str, Any] = field(default_factory=dict)

    # 附加信息
    skill_name: str = ""
    execution_time_ms: int = 0
    artifacts: Dict[str, str] = field(default_factory=dict)  # 生成的文件
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


@dataclass
class SkillConfig:
    """技能配置"""

    auto_confirm: bool = False  # 是否自动确认
    timeout_seconds: int = 300
    max_retries: int = 3
    verbose: bool = False


class Skill(ABC):
    """
    技能基类

    所有 Helix 技能必须继承这个类并实现 execute 方法
    """

    # 类属性 - 子类必须覆盖
    name: str = ""  # 技能名称（命令名）
    description: str = ""  # 技能描述
    category: SkillCategory = SkillCategory.EXECUTION
    status: SkillStatus = SkillStatus.DRAFT

    # 用法示例
    examples: List[str] = []

    def __init__(self, config: Optional[SkillConfig] = None):
        self.config = config or SkillConfig()
        self._initialized = False

    def initialize(self) -> None:
        """初始化技能"""
        if not self._initialized:
            self._do_initialize()
            self._initialized = True

    def _do_initialize(self) -> None:
        """子类可以实现的自定义初始化"""
        pass

    @abstractmethod
    async def execute(self, intent, context) -> SkillResult:
        """
        执行技能

        Args:
            intent: 解析后的用户意图
            context: Helix 上下文

        Returns:
            SkillResult: 执行结果
        """
        pass

    async def validate(self, intent, context) -> tuple[bool, str]:
        """
        验证输入是否合法

        Returns:
            (is_valid, error_message)
        """
        # 默认实现：总是有效
        return True, ""

    def get_usage(self) -> str:
        """获取使用说明"""
        lines = [
            f"## {self.name}",
            f"",
            f"{self.description}",
            f"",
            f"**分类**: {self.category.value}",
            f"**状态**: {self.status.value}",
            f"",
        ]

        if self.examples:
            lines.append("**示例**:")
            for example in self.examples:
                lines.append(f"```\n{self.name} {example}\n```")

        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"<Skill {self.name} ({self.status.value})>"
