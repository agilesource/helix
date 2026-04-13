"""Test Build Skill"""

import pytest
from helix.skills.build import BuildSkill
from helix.skills.base import SkillConfig


class TestBuildSkill:
    """Test BuildSkill"""

    @pytest.fixture
    def skill(self):
        return BuildSkill()

    def test_skill_init(self, skill):
        """Test skill initialization"""
        assert skill.name == "build"

    def test_skill_examples(self, skill):
        """Test skill examples"""
        assert len(skill.examples) > 0