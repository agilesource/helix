"""Test Verify Skill"""

import pytest
from helix.skills.verify import VerifySkill


class TestVerifySkill:
    """Test VerifySkill"""

    @pytest.fixture
    def skill(self):
        return VerifySkill()

    def test_skill_init(self, skill):
        """Test skill initialization"""
        assert skill.name == "verify"

    def test_skill_examples(self, skill):
        """Test skill examples"""
        assert len(skill.examples) > 0