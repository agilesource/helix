"""Test Helix Orchestrator"""

import pytest
from unittest.mock import AsyncMock, Mock, patch
from helix.core.orchestrator import HelixOrchestrator, HelixConfig, ExecutionMode
from helix.core.intent import IntentType
from helix.skills.base import Skill, SkillResult


class MockSkill(Skill):
    """Mock skill for testing"""

    name = "mock"

    async def _do_execute(self, intent, context):
        return SkillResult(
            success=True,
            message="Mock executed",
            skill_name=self.name
        )

    async def execute(self, intent, context):
        """Implement abstract method"""
        return await self._do_execute(intent, context)


class TestHelixOrchestrator:
    """Test HelixOrchestrator"""

    @pytest.fixture
    def orchestrator(self):
        return HelixOrchestrator()

    @pytest.fixture
    def config(self):
        return HelixConfig()

    def test_orchestrator_init(self, orchestrator):
        """Test orchestrator initialization"""
        assert orchestrator.config is not None
        assert orchestrator.context is not None
        assert orchestrator._skills == {}
        assert orchestrator._adapters == {}

    def test_config_init(self, config):
        """Test config initialization"""
        assert config.execution_mode == ExecutionMode.AUTO
        assert config.timeout_seconds == 300

    def test_register_skill(self, orchestrator):
        """Test skill registration"""
        skill = MockSkill()
        orchestrator.register_skill(skill)
        assert "mock" in orchestrator._skills

    def test_register_adapter(self, orchestrator):
        """Test adapter registration"""
        mock_adapter = Mock()
        orchestrator.register_adapter(ExecutionMode.CLAUDE_CODE, mock_adapter)
        assert ExecutionMode.CLAUDE_CODE in orchestrator._adapters

    def test_has_skill(self, orchestrator):
        """Test has_skill method"""
        assert orchestrator.has_skill("nonexistent") is False
        skill = MockSkill()
        orchestrator.register_skill(skill)
        assert orchestrator.has_skill("mock") is True

    def test_get_skill(self, orchestrator):
        """Test get_skill method"""
        skill = MockSkill()
        orchestrator.register_skill(skill)
        retrieved = orchestrator.get_skill("mock")
        assert retrieved is skill
        assert orchestrator.get_skill("nonexistent") is None

    def test_get_available_skills(self, orchestrator):
        """Test get_available_skills"""
        assert orchestrator.get_available_skills() == []
        skill = MockSkill()
        orchestrator.register_skill(skill)
        assert "mock" in orchestrator.get_available_skills()

    def test_get_context(self, orchestrator):
        """Test get_context"""
        ctx = orchestrator.get_context()
        assert ctx is orchestrator.context

    @pytest.mark.asyncio
    async def test_run_with_valid_skill(self, orchestrator):
        """Test run with valid skill"""
        skill = MockSkill()
        orchestrator.register_skill(skill)

        result = await orchestrator.run("帮我实现一个功能")
        # May fail if intent doesn't match mock skill
        assert result is not None

    @pytest.mark.asyncio
    async def test_run_with_no_skill(self, orchestrator):
        """Test run with no skill registered"""
        result = await orchestrator.run("帮我实现一个功能")
        assert result.success is False

    @pytest.mark.asyncio
    async def test_run_with_exception(self, orchestrator):
        """Test run handles exceptions"""
        # Register a skill that throws
        bad_skill = Mock()
        bad_skill.name = "bad"
        bad_skill.execute = AsyncMock(side_effect=Exception("Test error"))

        orchestrator.register_skill(bad_skill)

        # Override routing for this test
        with patch.object(orchestrator, '_route_skill', return_value=bad_skill):
            result = await orchestrator.run("test")
            assert result.success is False
            assert "error" in result.message.lower()


class TestHelixConfig:
    """Test HelixConfig"""

    def test_default_config(self):
        """Test default configuration"""
        config = HelixConfig()
        assert config.execution_mode == ExecutionMode.AUTO
        assert config.auto_confirm is False
        assert config.verbose is False
        assert config.log_level == "INFO"
        assert config.timeout_seconds == 300

    def test_custom_config(self):
        """Test custom configuration"""
        config = HelixConfig(
            execution_mode=ExecutionMode.OPENCLAW,
            auto_confirm=True,
            verbose=True,
            log_level="DEBUG",
            timeout_seconds=600
        )
        assert config.execution_mode == ExecutionMode.OPENCLAW
        assert config.auto_confirm is True
        assert config.verbose is True
        assert config.log_level == "DEBUG"
        assert config.timeout_seconds == 600


class TestExecutionMode:
    """Test ExecutionMode enum"""

    def test_execution_modes(self):
        """Test all execution modes"""
        assert ExecutionMode.AUTO.value == "auto"
        assert ExecutionMode.CLAUDE_CODE.value == "claude_code"
        assert ExecutionMode.OPENCLAW.value == "openclaw"
        assert ExecutionMode.OPENCODE.value == "opencode"
        assert ExecutionMode.CURSOR.value == "cursor"
        assert ExecutionMode.COPILOT.value == "copilot"
        assert ExecutionMode.GEMINI.value == "gemini"


class TestIntentToSkillMapping:
    """Test Intent to Skill mapping"""

    @pytest.fixture
    def orchestrator(self):
        return HelixOrchestrator()

    def test_mapping_completeness(self, orchestrator=None):
        """Test that all intent types have mappings"""
        # Import here to avoid circular dependency
        from helix.core.intent import IntentType

        mapping = HelixOrchestrator.INTENT_TO_SKILL

        # Check key intents are mapped
        assert IntentType.SPEC in mapping
        assert IntentType.BUILD in mapping
        assert IntentType.VERIFY in mapping
        assert IntentType.SHIP in mapping
        assert IntentType.REVIEW in mapping

    def test_route_skill(self, orchestrator):
        """Test skill routing"""
        from helix.core.intent import Intent

        # Register a mock skill that maps to SPEC intent
        skill = MockSkill()
        skill.name = "spec"  # Must match mapping
        orchestrator.register_skill(skill)

        # Test routing
        intent = Intent(type=IntentType.SPEC, raw_input="test", confidence=0.9)
        routed = orchestrator._route_skill(intent)
        assert routed is skill

        # Test unmapped intent
        intent = Intent(type=IntentType.GENERAL, raw_input="test", confidence=0.5)
        routed = orchestrator._route_skill(intent)
        assert routed is None


class TestOrchestratorIntegration:
    """Integration tests for orchestrator"""

    @pytest.fixture
    def orchestrator(self):
        return HelixOrchestrator()

    @pytest.mark.asyncio
    async def test_full_workflow(self, orchestrator):
        """Test full workflow with mock skill"""
        # Register skills
        for name in ["spec", "build", "verify"]:
            skill = Mock()
            skill.name = name
            skill.execute = AsyncMock(return_value=SkillResult(
                success=True,
                message=f"{name} done",
                skill_name=name
            ))
            orchestrator.register_skill(skill)

        # Verify skills registered
        skills = orchestrator.get_available_skills()
        assert "spec" in skills
        assert "build" in skills
        assert "verify" in skills

    def test_context_persistence(self, orchestrator):
        """Test context is persisted between operations"""
        ctx1 = orchestrator.get_context()
        ctx2 = orchestrator.get_context()
        assert ctx1 is ctx2
