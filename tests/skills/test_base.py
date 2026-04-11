"""Tests for Skill Base Classes"""

import pytest
import asyncio
from helix.skills.base import (
    Skill,
    SkillCategory,
    SkillStatus,
    SkillResult,
    SkillConfig,
)


class TestSkillCategory:
    """Test SkillCategory enum"""

    def test_skill_category_values(self):
        """Test SkillCategory values"""
        assert SkillCategory.INFRASTRUCTURE.value == "infrastructure"
        assert SkillCategory.EXECUTION.value == "execution"
        assert SkillCategory.QUALITY.value == "quality"
        assert SkillCategory.META.value == "meta"

    def test_skill_category_count(self):
        """Test there are exactly 4 categories"""
        assert len(SkillCategory) == 4


class TestSkillStatus:
    """Test SkillStatus enum"""

    def test_skill_status_values(self):
        """Test SkillStatus values"""
        assert SkillStatus.DRAFT.value == "draft"
        assert SkillStatus.EXPERIMENTAL.value == "experimental"
        assert SkillStatus.STABLE.value == "stable"
        assert SkillStatus.DEPRECATED.value == "deprecated"


class TestSkillResult:
    """Test SkillResult dataclass"""

    def test_skill_result_defaults(self):
        """Test default values"""
        result = SkillResult(success=True, message="Success")
        assert result.success is True
        assert result.message == "Success"
        assert result.data == {}
        assert result.skill_name == ""
        assert result.execution_time_ms == 0
        assert result.artifacts == {}
        assert result.warnings == []
        assert result.errors == []

    def test_skill_result_custom(self):
        """Test custom values"""
        result = SkillResult(
            success=False,
            message="Error occurred",
            data={"key": "value"},
            skill_name="test-skill",
            execution_time_ms=1500,
            artifacts={"output": "/path/to/output"},
            warnings=["Warning 1"],
            errors=["Error 1", "Error 2"],
        )
        assert result.success is False
        assert result.data == {"key": "value"}
        assert result.skill_name == "test-skill"
        assert result.execution_time_ms == 1500
        assert result.artifacts == {"output": "/path/to/output"}
        assert result.warnings == ["Warning 1"]
        assert result.errors == ["Error 1", "Error 2"]


class TestSkillConfig:
    """Test SkillConfig dataclass"""

    def test_skill_config_defaults(self):
        """Test default values"""
        config = SkillConfig()
        assert config.auto_confirm is False
        assert config.timeout_seconds == 300
        assert config.max_retries == 3
        assert config.verbose is False

    def test_skill_config_custom(self):
        """Test custom values"""
        config = SkillConfig(
            auto_confirm=True,
            timeout_seconds=600,
            max_retries=5,
            verbose=True,
        )
        assert config.auto_confirm is True
        assert config.timeout_seconds == 600
        assert config.max_retries == 5
        assert config.verbose is True


class MockSkill(Skill):
    """Mock skill for testing"""

    name = "mock"
    description = "Mock skill for testing"
    category = SkillCategory.EXECUTION
    status = SkillStatus.STABLE
    examples = ["mock do something"]

    async def execute(self, intent, context):
        return SkillResult(success=True, message="Mock executed")


class TestSkill:
    """Test Skill base class"""

    @pytest.mark.asyncio
    async def test_skill_creation(self):
        """Test basic skill creation"""
        skill = MockSkill()
        assert skill.name == "mock"
        assert skill.description == "Mock skill for testing"
        assert skill.category == SkillCategory.EXECUTION
        assert skill.status == SkillStatus.STABLE

    @pytest.mark.asyncio
    async def test_skill_with_config(self):
        """Test skill with custom config"""
        config = SkillConfig(timeout_seconds=60, verbose=True)
        skill = MockSkill(config=config)
        assert skill.config.timeout_seconds == 60
        assert skill.config.verbose is True

    @pytest.mark.asyncio
    async def test_initialize(self):
        """Test skill initialization"""
        skill = MockSkill()
        assert skill._initialized is False
        skill.initialize()
        assert skill._initialized is True

    @pytest.mark.asyncio
    async def test_initialize_twice(self):
        """Test initialization is idempotent"""
        skill = MockSkill()
        skill.initialize()
        skill.initialize()  # Should not error
        assert skill._initialized is True

    @pytest.mark.asyncio
    async def test_execute(self):
        """Test skill execution"""
        skill = MockSkill()
        result = await skill.execute(None, None)
        assert result.success is True
        assert result.message == "Mock executed"

    @pytest.mark.asyncio
    async def test_validate_default(self):
        """Test default validation"""
        skill = MockSkill()
        is_valid, error = await skill.validate(None, None)
        assert is_valid is True
        assert error == ""

    def test_get_usage(self):
        """Test get_usage method"""
        skill = MockSkill()
        usage = skill.get_usage()

        assert "mock" in usage
        assert "Mock skill for testing" in usage
        assert "execution" in usage
        assert "stable" in usage
        assert "mock do something" in usage

    def test_repr(self):
        """Test __repr__ method"""
        skill = MockSkill()
        assert "MockSkill" in repr(skill) or "mock" in repr(skill).lower()
        assert "stable" in repr(skill)

    def test_examples(self):
        """Test examples attribute"""
        skill = MockSkill()
        assert skill.examples == ["mock do something"]
