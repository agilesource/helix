"""Test base skill and result models"""

import pytest
from helix.skills.base import Skill, SkillResult, SkillConfig, SkillCategory, SkillStatus


class TestSkill:
    """Test Skill base class"""

    def test_skill_config_defaults(self):
        """Test SkillConfig default values"""
        config = SkillConfig()
        assert config.auto_confirm is False
        assert config.timeout_seconds == 300
        assert config.max_retries == 3
        assert config.verbose is False

    def test_skill_config_custom(self):
        """Test SkillConfig with custom values"""
        config = SkillConfig(
            auto_confirm=True,
            timeout_seconds=600,
            max_retries=5,
            verbose=True
        )
        assert config.auto_confirm is True
        assert config.timeout_seconds == 600
        assert config.max_retries == 5
        assert config.verbose is True

    def test_skill_status_values(self):
        """Test SkillStatus enum"""
        assert SkillStatus.DRAFT.value == "draft"
        assert SkillStatus.BETA.value == "beta"
        assert SkillStatus.EXPERIMENTAL.value == "experimental"
        assert SkillStatus.STABLE.value == "stable"
        assert SkillStatus.DEPRECATED.value == "deprecated"

    def test_skill_category_values(self):
        """Test SkillCategory enum"""
        assert SkillCategory.INFRASTRUCTURE.value == "infrastructure"
        assert SkillCategory.EXECUTION.value == "execution"
        assert SkillCategory.QUALITY.value == "quality"
        assert SkillCategory.META.value == "meta"


class TestSkillResult:
    """Test SkillResult"""

    def test_success_result(self):
        """Test successful result"""
        result = SkillResult(
            success=True,
            message="Operation completed",
            skill_name="test"
        )
        assert result.success is True
        assert result.message == "Operation completed"
        assert result.skill_name == "test"

    def test_failure_result(self):
        """Test failure result"""
        result = SkillResult(
            success=False,
            message="Something went wrong",
            skill_name="test"
        )
        assert result.success is False
        # Note: error field doesn't exist, errors are part of message

    def test_result_with_data(self):
        """Test result with data"""
        result = SkillResult(
            success=True,
            message="Done",
            skill_name="test",
            data={"key": "value"}
        )
        assert result.data["key"] == "value"

    def test_result_with_artifacts(self):
        """Test result with artifacts"""
        result = SkillResult(
            success=True,
            message="Done",
            skill_name="test",
            artifacts={"output": "content"}
        )
        assert result.artifacts["output"] == "content"

    def test_result_with_warnings(self):
        """Test result with warnings"""
        result = SkillResult(
            success=True,
            message="Done",
            skill_name="test",
            warnings=["Warning 1", "Warning 2"]
        )
        assert len(result.warnings) == 2
        assert "Warning 1" in result.warnings

    def test_result_with_errors(self):
        """Test result with errors"""
        result = SkillResult(
            success=False,
            message="Failed",
            skill_name="test",
            errors=["Error 1"]
        )
        assert len(result.errors) == 1

    def test_result_execution_time(self):
        """Test execution time tracking"""
        result = SkillResult(
            success=True,
            message="Done",
            skill_name="test",
            execution_time_ms=1500
        )
        assert result.execution_time_ms == 1500


class TestSkillBaseClass:
    """Test Skill base class functionality"""

    def test_skill_init(self):
        """Test skill initialization"""
        class TestSkillImpl(Skill):
            name = "test"
            description = "Test skill"
            category = SkillCategory.EXECUTION
            status = SkillStatus.STABLE

            async def execute(self, intent, context):
                return SkillResult(success=True, message="done")

        skill = TestSkillImpl()
        assert skill.name == "test"
        assert skill._initialized is False

    def test_skill_init_with_config(self):
        """Test skill initialization with config"""
        class TestSkillImpl(Skill):
            name = "test"
            description = "Test skill"
            category = SkillCategory.EXECUTION
            status = SkillStatus.STABLE

            async def execute(self, intent, context):
                return SkillResult(success=True, message="done")

        config = SkillConfig(timeout_seconds=600)
        skill = TestSkillImpl(config=config)
        assert skill.config.timeout_seconds == 600

    def test_skill_initialize(self):
        """Test skill initialize method"""
        class TestSkillImpl(Skill):
            name = "test"
            description = "Test skill"
            category = SkillCategory.EXECUTION
            status = SkillStatus.STABLE

            def _do_initialize(self):
                self._ready = True

            async def execute(self, intent, context):
                return SkillResult(success=True, message="done")

        skill = TestSkillImpl()
        skill.initialize()
        assert skill._initialized is True

    @pytest.mark.asyncio
    async def test_skill_validate(self):
        """Test skill validate method"""
        class TestSkillImpl(Skill):
            name = "test"
            description = "Test skill"
            category = SkillCategory.EXECUTION
            status = SkillStatus.STABLE

            async def execute(self, intent, context):
                return SkillResult(success=True, message="done")

        skill = TestSkillImpl()
        is_valid, error = await skill.validate(None, None)
        assert is_valid is True
        assert error == ""

    def test_skill_get_usage(self):
        """Test get usage method"""
        class TestSkillImpl(Skill):
            name = "test"
            description = "Test skill description"
            category = SkillCategory.EXECUTION
            status = SkillStatus.STABLE
            examples = ["example1", "example2"]

            async def execute(self, intent, context):
                return SkillResult(success=True, message="done")

        skill = TestSkillImpl()
        usage = skill.get_usage()
        assert "## test" in usage
        assert "Test skill description" in usage
        assert "execution" in usage
        assert "stable" in usage

    def test_skill_repr(self):
        """Test skill repr"""
        class TestSkillImpl(Skill):
            name = "test"
            description = "Test skill"
            category = SkillCategory.EXECUTION
            status = SkillStatus.STABLE

            async def execute(self, intent, context):
                return SkillResult(success=True, message="done")

        skill = TestSkillImpl()
        assert "test" in repr(skill)
        assert "stable" in repr(skill)
