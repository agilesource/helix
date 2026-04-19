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
from helix.core.intent_classifier import IntentClassifier
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
    timeout_seconds: int = 300  # Default 5 minute timeout

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

    # Intent type to skill name mapping
    INTENT_TO_SKILL: Dict[IntentType, str] = {
        IntentType.SPEC: "spec",
        IntentType.BUILD: "build",
        IntentType.VERIFY: "verify",
        IntentType.SHIP: "ship",
        IntentType.REVIEW: "review",
        IntentType.TEST: "test",
        IntentType.AUDIT: "audit",
        IntentType.GATE: "gate",
        IntentType.BROWSE: "browse",
        IntentType.DESIGN: "design",
        IntentType.LEARN: "learn",
        IntentType.CHECKPOINT: "checkpoint",
    }

    def __init__(self, config: Optional[HelixConfig] = None):
        self.config = config or HelixConfig()
        self.context = HelixContext()
        self._skills: Dict[str, Skill] = {}
        self._adapters: Dict[ExecutionMode, Any] = {}
        self._intent_classifier = IntentClassifier()

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
        1. Parse intent (using IntentClassifier)
        2. Route to skill
        3. Execute skill
        4. Return result
        """
        try:
            # Step 1: Intent recognition with classifier
            intent = await self._parse_intent(user_input)

            # Step 2: Skill routing
            skill = self._route_skill(intent)

            if not skill:
                return SkillResult(
                    success=False,
                    message=f"No skill available for intent: {intent.type.value}",
                    skill_name="orchestrator"
                )

            # Step 3: Execute skill
            result = await skill.execute(intent, self.context)

            # Step 4: Update context
            self.context.add_interaction(intent, result)

            return result

        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Orchestrator error: {str(e)}",
                skill_name="orchestrator"
            )

    async def _parse_intent(self, user_input: str) -> Intent:
        """Parse user intent using IntentClassifier"""
        return await self._intent_classifier.classify(user_input, self.context)

    def _route_skill(self, intent: Intent) -> Optional[Skill]:
        """Route intent to skill"""
        skill_name = self.INTENT_TO_SKILL.get(intent.type)
        if skill_name and skill_name in self._skills:
            return self._skills[skill_name]
        return None

    def get_available_skills(self) -> List[str]:
        """Get all available skills"""
        return list(self._skills.keys())

    def get_context(self) -> HelixContext:
        """Get current context"""
        return self.context

    def has_skill(self, skill_name: str) -> bool:
        """Check if a skill is registered"""
        return skill_name in self._skills

    def get_skill(self, skill_name: str) -> Optional[Skill]:
        """Get a skill by name"""
        return self._skills.get(skill_name)
