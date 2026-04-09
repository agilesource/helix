"""
/spec Skill - Specification Generator (LLM Enhanced)

Transform user requirements into structured specifications using LLM
"""

import asyncio
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum

from helix.skills.base import Skill, SkillResult, SkillConfig, SkillCategory, SkillStatus
from helix.core.intent import Intent, IntentType
from helix.core.context import HelixContext
from helix.adapters.llm import get_llm_adapter, AnthropicAdapter, AIRequest


class RequirementType(Enum):
    """Requirement types"""

    CRUD = "crud"
    API = "api"
    ALGORITHM = "algorithm"
    INTEGRATION = "integration"
    UI = "ui"
    SCRIPT = "script"
    INFRASTRUCTURE = "infrastructure"
    GENERAL = "general"


@dataclass
class ExtractedEntities:
    """Entities extracted from requirements"""

    domain: str = ""
    action: str = ""
    entities: List[str] = field(default_factory=list)
    integrations: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    target_users: List[str] = field(default_factory=list)
    value_proposition: str = ""
    features: List[str] = field(default_factory=list)
    project_context: str = ""


# LLM Prompt Templates
SPEC_SYSTEM_PROMPT = """You are a senior software architect specializing in requirement analysis and specification writing.
Your task is to transform user requirements into comprehensive, structured specifications.

Guidelines:
1. Analyze the user's requirement thoroughly
2. Identify the domain, entities, and relationships
3. Define clear acceptance criteria
4. Consider edge cases and error scenarios
5. Output in clean Markdown format

Focus on creating specifications that are:
- Clear and unambiguous
- Testable (have measurable acceptance criteria)
- Complete (cover happy path and edge cases)
- Pragmatic (not over-engineered)
"""


SPEC_GENERATION_PROMPT = """Transform the following requirement into a detailed specification:

Requirement: {requirement}

Requirement Type: {req_type}
Domain: {domain}

Generate a complete specification including:
1. Feature Overview (one sentence)
2. User Story (As a [role], I want [feature], so that [value])
3. Functional Requirements (core features with acceptance criteria)
4. Non-Functional Requirements (performance, security, etc.)
5. API Design (if applicable)
6. Data Model (if applicable)
7. Acceptance Criteria (testable scenarios)
8. Edge Cases
9. Technical Constraints

Output ONLY the specification in Markdown format. No introductions or conclusions.
"""


SOCRATIC_PROMPT = """Analyze this requirement and identify what information is missing that would help create a better specification.

Requirement: {requirement}
Known: {known_info}

Provide 3-5 clarifying questions that would help understand the requirement better.
Output ONLY the questions, one per line, in English.
"""


LLM_CLASSIFICATION_PROMPT = """Classify this requirement into one of these categories:
- CRUD (create, add, delete, modify, manage)
- API (api, service, REST, GraphQL)
- ALGORITHM (calculate, sort, search, optimize)
- INTEGRATION (integrate, third-party, stripe, payment)
- UI (page, component, frontend, button, form)
- SCRIPT (script, tool, CLI, command)
- INFRASTRUCTURE (deploy, CI/CD, docker, k8s)
- GENERAL (anything else)

Requirement: {requirement}

Output ONLY the category name in lowercase.
"""


LLM_ENTITY_EXTRACTION_PROMPT = """Extract key information from this requirement:

Requirement: {requirement}

Output a JSON object with:
- domain: The business domain (e.g., user, order, payment, product)
- action: The main action (e.g., login, create, search, pay)
- target_users: Who is this for
- value_proposition: What problem does this solve
- integrations: Any third-party systems mentioned
- features: List of specific features mentioned

Output ONLY valid JSON.
"""


class SpecSkill(Skill):
    """Specification generation skill with LLM enhancement"""

    name = "spec"
    description = "Transform requirements into structured specifications"
    category = SkillCategory.EXECUTION
    status = SkillStatus.DRAFT

    examples = [
        "I want to build a user login feature",
        "Create a user management API",
        "Implement a recommendation algorithm",
    ]

    def __init__(self, config: Optional[SkillConfig] = None):
        super().__init__(config)
        self._llm_adapter = None
        self._fallback_skill = None  # Fallback to rule-based if LLM unavailable

    def _do_initialize(self) -> None:
        """Initialize and get LLM adapter"""
        self._llm_adapter = get_llm_adapter()

        # Import fallback skill for when LLM is unavailable
        from helix.skills.spec_fallback import SpecSkillFallback
        self._fallback_skill = SpecSkillFallback(self.config)

    async def execute(self, intent: Intent, context: HelixContext) -> SkillResult:
        """Execute specification generation"""
        self.initialize()
        start_time = asyncio.get_event_loop().time()

        user_input = intent.raw_input

        # Check if LLM is available
        if self._llm_adapter and self._llm_adapter.is_available():
            result = await self._execute_with_llm(user_input, start_time)
        else:
            # Fallback to rule-based
            if self._fallback_skill:
                return await self._fallback_skill.execute(intent, context)
            else:
                return SkillResult(
                    success=False,
                    message="No LLM available and fallback failed",
                    skill_name=self.name
                )

        return result

    async def _execute_with_llm(self, user_input: str, start_time: float) -> SkillResult:
        """Execute with LLM enhancement"""

        # Step 1: Classify requirement type using LLM
        req_type = await self._llm_classify(user_input)

        # Step 2: Extract entities using LLM
        entities = await self._llm_extract_entities(user_input)

        # Step 3: Generate clarifying questions (Socratic)
        clarifications = await self._llm_socratic_questions(user_input, entities)

        # Step 4: Generate specification using LLM
        spec_content = await self._llm_generate_spec(
            user_input, req_type, entities, clarifications
        )

        execution_time = int((asyncio.get_event_loop().time() - start_time) * 1000)

        return SkillResult(
            success=True,
            message="Specification generated with LLM",
            data={
                "requirement_type": req_type.value,
                "entities": {
                    "domain": entities.domain,
                    "action": entities.action,
                    "entities": entities.entities,
                },
                "clarifications": clarifications,
                "spec_content": spec_content,
                "llm_used": True,
            },
            skill_name=self.name,
            execution_time_ms=execution_time,
            artifacts={"spec": spec_content},
        )

    async def _llm_classify(self, requirement: str) -> RequirementType:
        """Use LLM to classify requirement type"""
        prompt = LLM_CLASSIFICATION_PROMPT.format(requirement=requirement)

        response = await self._llm_adapter.execute(
            AIRequest(prompt=prompt, context=SPEC_SYSTEM_PROMPT)
        )

        if response.success:
            try:
                return RequirementType(response.content.strip().lower())
            except ValueError:
                pass

        # Fallback to rule-based classification if LLM fails
        if self._fallback_skill:
            self._fallback_skill.initialize()
            return self._fallback_skill._classify_requirement(requirement)

        return RequirementType.GENERAL

    async def _llm_extract_entities(self, requirement: str) -> ExtractedEntities:
        """Use LLM to extract entities"""
        prompt = LLM_ENTITY_EXTRACTION_PROMPT.format(requirement=requirement)

        response = await self._llm_adapter.execute(
            AIRequest(prompt=prompt, context=SPEC_SYSTEM_PROMPT)
        )

        if response.success:
            try:
                import json
                data = json.loads(response.content)
                return ExtractedEntities(
                    domain=data.get("domain", ""),
                    action=data.get("action", ""),
                    target_users=data.get("target_users", []),
                    value_proposition=data.get("value_proposition", ""),
                    integrations=data.get("integrations", []),
                    features=data.get("features", []),
                )
            except (json.JSONDecodeError, KeyError):
                pass

        # Fallback to rule-based extraction if LLM fails
        if self._fallback_skill:
            self._fallback_skill.initialize()
            return self._fallback_skill._extract_entities(requirement)

        return ExtractedEntities()

    async def _llm_socratic_questions(
        self,
        requirement: str,
        entities: ExtractedEntities
    ) -> Dict[str, str]:
        """Use LLM to generate clarifying questions"""
        known_info = f"Domain: {entities.domain}, Action: {entities.action}, Target: {entities.target_users}"
        prompt = SOCRATIC_PROMPT.format(requirement=requirement, known_info=known_info)

        response = await self._llm_adapter.execute(
            AIRequest(prompt=prompt, context=SPEC_SYSTEM_PROMPT)
        )

        clarifications = {}
        if response.success:
            questions = response.content.strip().split("\n")
            for i, q in enumerate(questions[:5]):
                q = q.strip()
                if q and not q.startswith("#"):
                    clarifications[f"question_{i+1}"] = q

        return clarifications

    async def _llm_generate_spec(
        self,
        requirement: str,
        req_type: RequirementType,
        entities: ExtractedEntities,
        clarifications: Dict[str, str]
    ) -> str:
        """Use LLM to generate specification"""
        prompt = SPEC_GENERATION_PROMPT.format(
            requirement=requirement,
            req_type=req_type.value,
            domain=entities.domain or "Not specified"
        )

        response = await self._llm_adapter.execute(
            AIRequest(prompt=prompt, context=SPEC_SYSTEM_PROMPT)
        )

        if response.success:
            return response.content

        # Fallback to template if LLM fails
        return self._fallback_generate(requirement, req_type, entities)

    def _fallback_generate(
        self,
        requirement: str,
        req_type: RequirementType,
        entities: ExtractedEntities
    ) -> str:
        """Fallback template-based generation"""
        # Import and use fallback skill
        if self._fallback_skill:
            self._fallback_skill.initialize()  # Initialize the fallback skill
            return self._fallback_skill._generate_spec(
                requirement, req_type.value, entities, {}
            )

        # Basic fallback
        return f"# Specification\n\n{requirement}\n\n**Domain:** {entities.domain}\n**Type:** {req_type.value}"
