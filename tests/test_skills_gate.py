"""Test Gate Skill"""

import pytest
from helix.skills.gate import GateSkill


class TestGateSkill:
    """Test GateSkill"""

    @pytest.fixture
    def skill(self):
        return GateSkill()

    def test_skill_init(self, skill):
        """Test skill initialization"""
        assert skill.name == "gate"

    def test_skill_examples(self, skill):
        """Test skill examples"""
        assert len(skill.examples) > 0