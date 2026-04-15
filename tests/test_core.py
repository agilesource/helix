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

    def test_context_start_session(self):
        """Test starting a session"""
        from helix.core.context import SessionState
        context = HelixContext()
        context.start_session("/test/path")
        assert context.project is not None
        assert context.project.project_path == "/test/path"
        assert context.session_state == SessionState.RUNNING

    def test_context_add_memory(self):
        """Test adding memory"""
        context = HelixContext()
        context.add_memory("test", "test content", ["tag1", "tag2"])
        assert len(context.memories) == 1
        assert context.memories[0]["type"] == "test"
        assert context.memories[0]["content"] == "test content"
        assert "tag1" in context.memories[0]["tags"]

    def test_context_get_recent_interactions(self):
        """Test getting recent interactions"""
        context = HelixContext()
        interactions = context.get_recent_interactions(5)
        assert isinstance(interactions, list)

    def test_context_get_summary(self):
        """Test getting context summary"""
        context = HelixContext()
        summary = context.get_summary()
        assert "session_id" in summary
        assert "state" in summary
        assert "duration_seconds" in summary


class TestSessionState:
    """Test SessionState enum"""

    def test_session_state_values(self):
        """Test SessionState enum values"""
        from helix.core.context import SessionState
        assert SessionState.IDLE.value == "idle"
        assert SessionState.RUNNING.value == "running"
        assert SessionState.WAITING_CONFIRMATION.value == "waiting_confirmation"
        assert SessionState.COMPLETED.value == "completed"
        assert SessionState.ERROR.value == "error"


class TestProjectState:
    """Test ProjectState dataclass"""

    def test_project_state_creation(self):
        """Test ProjectState creation"""
        from helix.core.context import ProjectState
        project = ProjectState(project_path="/test", project_type="python")
        assert project.project_path == "/test"
        assert project.project_type == "python"
        assert project.framework is None
        assert project.current_branch is None
        assert project.is_dirty is False
        assert project.lines_of_code == 0
        assert project.test_coverage == 0.0
        assert project.gate_level == 0

    def test_project_state_with_optional(self):
        """Test ProjectState with optional fields"""
        from helix.core.context import ProjectState
        project = ProjectState(
            project_path="/test",
            project_type="python",
            framework="fastapi",
            current_branch="main",
            is_dirty=True,
            lines_of_code=1000,
            test_coverage=85.5,
            last_review_score=9.5,
            gate_level=2
        )
        assert project.framework == "fastapi"
        assert project.current_branch == "main"
        assert project.is_dirty is True
        assert project.lines_of_code == 1000
        assert project.test_coverage == 85.5
        assert project.last_review_score == 9.5
        assert project.gate_level == 2


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