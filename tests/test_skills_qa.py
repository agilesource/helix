"""Test QA Skill"""

import pytest
from helix.skills.qa import QASkill
from helix.skills.base import SkillConfig


class TestQASkill:
    """Test QASkill"""

    @pytest.fixture
    def skill(self):
        config = SkillConfig()
        return QASkill(config)

    def test_skill_init(self, skill):
        """Test skill initialization"""
        assert skill.name == "qa"

    def test_skill_examples(self, skill):
        """Test skill examples"""
        assert len(skill.examples) > 0