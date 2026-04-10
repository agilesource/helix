"""
Helix Core Orchestrator

Core responsibilities:
1. Intent recognition - Understand what the user wants
2. Skill routing - Select appropriate skill to execute
3. Execution scheduling - Manage skill execution flow
4. Result aggregation - Aggregate and return results
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum

from helix.core.context import HelixContext
from helix.core.intent import Intent, IntentType
from helix.skills.base import Skill, SkillResult


class ExecutionMode(Enum):
    """Execution mode - supports different AI engines"""

    AUTO = "auto"
    CLAUDE_CODE = "claude_code"
    OPENCLAW = "openclaw"
    OPENCODE = "opencode"
    CURSOR = "cursor"
    COPILOT = "copilot"
    GEMINI = "gemini"


@dataclass
class HelixConfig:
    """Helix Global Configuration"""

    execution_mode: ExecutionMode = ExecutionMode.AUTO
    auto_confirm: bool = False
    verbose: bool = False
    log_level: str = "INFO"

    # Adapter configuration
    adapters: Dict[str, Dict[str, Any]] = field(default_factory=dict)


class HelixOrchestrator:
    """
    Helix Orchestrator

    Core responsibilities:
    - Intent recognition and parsing
    - Skill routing and scheduling
    - Multi-engine adaptation
    - Context management
    """

    def __init__(self, config: Optional[HelixConfig] = None):
        self.config = config or HelixConfig()
        self.context = HelixContext()
        self._skills: Dict[str, Skill] = {}
        self._adapters: Dict[ExecutionMode, Any] = {}

    def register_skill(self, skill: Skill) -> None:
        """Register a skill"""
        self._skills[skill.name] = skill

    def register_adapter(self, mode: ExecutionMode, adapter: Any) -> None:
        """Register an AI engine adapter"""
        self._adapters[mode] = adapter

    async def run(self, user_input: str) -> SkillResult:
        """
        Main entry point: Process user input

        Flow:
        1. Parse intent
        2. Route to skill
        3. Execute skill
        4. Return result
        """
        # Step 1: Intent recognition
        intent = self._parse_intent(user_input)

        # Step 2: Skill routing
        skill = self._route_skill(intent)

        if not skill:
            return SkillResult(
                success=False,
                message=f"Cannot handle intent: {intent.type.value}",
                data={"intent": intent}
            )

        # Step 3: Execute skill
        result = await skill.execute(intent, self.context)

        # Step 4: Update context
        self.context.add_interaction(intent, result)

        return result

    def _parse_intent(self, user_input: str) -> Intent:
        """Parse user intent"""
        # TODO: Implement smarter intent recognition
        # For now, use simple keyword matching

        input_lower = user_input.lower()

        # Specification requirements
        if any(kw in input_lower for kw in ["want", "need", "build", "feature", "requirement", "spec"]):
            return Intent(
                type=IntentType.SPEC,
                raw_input=user_input,
                confidence=0.9
            )

        # Build requirements
        if any(kw in input_lower for kw in ["implement", "develop", "write code", "build", "create"]):
            return Intent(
                type=IntentType.BUILD,
                raw_input=user_input,
                confidence=0.8
            )

        # Verification requirements
        if any(kw in input_lower for kw in ["test", "verify", "check", "verify", "test"]):
            return Intent(
                type=IntentType.VERIFY,
                raw_input=user_input,
                confidence=0.9
            )

        # Ship/Deploy requirements
        if any(kw in input_lower for kw in ["ship", "deploy", "release", "publish"]):
            return Intent(
                type=IntentType.SHIP,
                raw_input=user_input,
                confidence=0.9
            )

        # Review requirements
        if any(kw in input_lower for kw in ["review", "check code", "audit"]):
            return Intent(
                type=IntentType.REVIEW,
                raw_input=user_input,
                confidence=0.9
            )

        # Default: general conversation
        return Intent(
            type=IntentType.GENERAL,
            raw_input=user_input,
            confidence=0.5
        )

    def _route_skill(self, intent: Intent) -> Optional[Skill]:
        """Route intent to skill"""

        # Intent type to skill name mapping
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
        """Get all available skills"""
        return list(self._skills.keys())

    def get_context(self) -> HelixContext:
        """Get current context"""
        return self.context
