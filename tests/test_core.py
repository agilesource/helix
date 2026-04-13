"""Test Core Modules"""

import pytest
from helix.core.orchestrator import HelixOrchestrator, HelixConfig
from helix.core.context import HelixContext


class TestHelixConfig:
    """Test HelixConfig"""

    def test_config_defaults(self):
        """Test config default values"""
        config = HelixConfig()
        assert config.auto_confirm is False
        assert config.verbose is False
        assert config.log_level == "INFO"

    def test_config_custom(self):
        """Test config with custom values"""
        config = HelixConfig(
            auto_confirm=True,
            verbose=True,
            log_level="DEBUG"
        )
        assert config.auto_confirm is True
        assert config.verbose is True
        assert config.log_level == "DEBUG"


class TestHelixContext:
    """Test HelixContext"""

    def test_context_init(self):
        """Test context initialization"""
        context = HelixContext()
        assert context.session_id is not None
        assert context.session_state is not None

    def test_context_session_state(self):
        """Test context session state"""
        from helix.core.context import SessionState
        context = HelixContext()
        assert context.session_state == SessionState.IDLE


class TestHelixOrchestrator:
    """Test HelixOrchestrator"""

    def test_orchestrator_init(self):
        """Test orchestrator initialization"""
        config = HelixConfig()
        orchestrator = HelixOrchestrator(config)
        assert orchestrator.config is config
        assert orchestrator._skills == {}

    def test_orchestrator_register_skill(self):
        """Test registering a skill"""
        from helix.skills.base import Skill, SkillCategory, SkillStatus

        class TestSkill(Skill):
            name = "test"
            description = "Test skill"
            category = SkillCategory.EXECUTION
            status = SkillStatus.STABLE

            def execute(self, intent, context):
                pass

        config = HelixConfig()
        orchestrator = HelixOrchestrator(config)

        skill = TestSkill()
        orchestrator.register_skill(skill)

        assert "test" in orchestrator._skills

    def test_orchestrator_get_available_skills(self):
        """Test getting available skills"""
        from helix.skills.base import Skill, SkillCategory, SkillStatus

        class TestSkill(Skill):
            name = "test-skill"
            description = "Test skill"
            category = SkillCategory.EXECUTION
            status = SkillStatus.STABLE

            def execute(self, intent, context):
                pass

        config = HelixConfig()
        orchestrator = HelixOrchestrator(config)

        skill = TestSkill()
        orchestrator.register_skill(skill)

        available = orchestrator.get_available_skills()
        assert "test-skill" in available