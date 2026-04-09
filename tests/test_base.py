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

    def test_skill_status_values(self):
        """Test SkillStatus enum"""
        assert SkillStatus.DRAFT.value == "draft"
        assert SkillStatus.DEPRECATED.value == "deprecated"

    def test_skill_category_values(self):
        """Test SkillCategory enum"""
        assert SkillCategory.EXECUTION.value == "execution"


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
