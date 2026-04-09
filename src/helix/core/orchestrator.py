"""
Helix 核心调度中心

负责：
1. 意图识别 - 理解用户想要什么
2. 技能路由 - 选择合适的技能执行
3. 执行调度 - 管理技能执行流程
4. 结果整合 - 汇总并返回结果
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum

from helix.core.context import HelixContext
from helix.core.intent import Intent, IntentType
from helix.skills.base import Skill, SkillResult


class ExecutionMode(Enum):
    """执行模式 - 支持不同 AI 引擎"""

    AUTO = "auto"  # 自动选择
    CLAUDE_CODE = "claude_code"
    OPENCLAW = "openclaw"
    OPENCODE = "opencode"
    CURSOR = "cursor"
    COPILOT = "copilot"
    GEMINI = "gemini"


@dataclass
class HelixConfig:
    """Helix 全局配置"""

    execution_mode: ExecutionMode = ExecutionMode.AUTO
    auto_confirm: bool = False  # 是否自动确认每个步骤
    verbose: bool = False
    log_level: str = "INFO"

    # 适配器配置
    adapters: Dict[str, Dict[str, Any]] = field(default_factory=dict)


class HelixOrchestrator:
    """
    Helix 调度中心

    核心职责：
    - 意图识别与解析
    - 技能路由与调度
    - 多引擎适配
    - 上下文管理
    """

    def __init__(self, config: Optional[HelixConfig] = None):
        self.config = config or HelixConfig()
        self.context = HelixContext()
        self._skills: Dict[str, Skill] = {}
        self._adapters: Dict[ExecutionMode, Any] = {}

    def register_skill(self, skill: Skill) -> None:
        """注册技能"""
        self._skills[skill.name] = skill

    def register_adapter(self, mode: ExecutionMode, adapter: Any) -> None:
        """注册 AI 引擎适配器"""
        self._adapters[mode] = adapter

    async def run(self, user_input: str) -> SkillResult:
        """
        主入口：处理用户输入

        流程：
        1. 解析意图
        2. 路由到技能
        3. 执行技能
        4. 返回结果
        """
        # Step 1: 意图识别
        intent = self._parse_intent(user_input)

        # Step 2: 技能路由
        skill = self._route_skill(intent)

        if not skill:
            return SkillResult(
                success=False,
                message=f"无法处理该意图: {intent.type.value}",
                data={"intent": intent}
            )

        # Step 3: 执行技能
        result = await skill.execute(intent, self.context)

        # Step 4: 更新上下文
        self.context.add_interaction(intent, result)

        return result

    def _parse_intent(self, user_input: str) -> Intent:
        """解析用户意图"""
        # TODO: 实现更智能的意图识别
        # 暂时使用简单的关键词匹配

        input_lower = user_input.lower()

        # 规格类需求
        if any(kw in input_lower for kw in ["想要", "需要", "做一个", "功能", "需求", "spec"]):
            return Intent(
                type=IntentType.SPEC,
                raw_input=user_input,
                confidence=0.9
            )

        # 构建类需求
        if any(kw in input_lower for kw in ["实现", "开发", "写代码", "build", "创建"]):
            return Intent(
                type=IntentType.BUILD,
                raw_input=user_input,
                confidence=0.8
            )

        # 验证类需求
        if any(kw in input_lower for kw in ["测试", "验证", "检查", "verify", "test"]):
            return Intent(
                type=IntentType.VERIFY,
                raw_input=user_input,
                confidence=0.9
            )

        # 发布类需求
        if any(kw in input_lower for kw in ["发布", "部署", "ship", "deploy"]):
            return Intent(
                type=IntentType.SHIP,
                raw_input=user_input,
                confidence=0.9
            )

        # 审查类需求
        if any(kw in input_lower for kw in ["审查", "review", "检查代码"]):
            return Intent(
                type=IntentType.REVIEW,
                raw_input=user_input,
                confidence=0.9
            )

        # 默认：通用对话
        return Intent(
            type=IntentType.GENERAL,
            raw_input=user_input,
            confidence=0.5
        )

    def _route_skill(self, intent: Intent) -> Optional[Skill]:
        """根据意图路由到技能"""

        # 意图类型到技能名的映射
        mapping = {
            IntentType.SPEC: "spec",
            IntentType.BUILD: "build",
            IntentType.VERIFY: "verify",
            IntentType.SHIP: "ship",
            IntentType.REVIEW: "review",
            IntentType.TEST: "test",
            IntentType.AUDIT: "audit",
            IntentType.GATE: "gate",
            IntentType.DESIGN: "design",
            IntentType.LEARN: "learn",
            IntentType.CHECKPOINT: "checkpoint",
        }

        skill_name = mapping.get(intent.type)
        if skill_name and skill_name in self._skills:
            return self._skills[skill_name]

        return None

    def get_available_skills(self) -> List[str]:
        """获取所有可用技能"""
        return list(self._skills.keys())

    def get_context(self) -> HelixContext:
        """获取当前上下文"""
        return self.context
