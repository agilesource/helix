"""Test Audit Skill"""

import pytest
from helix.skills.audit import AuditSkill


class TestAuditSkill:
    """Test AuditSkill"""

    @pytest.fixture
    def skill(self):
        return AuditSkill()

    def test_skill_init(self, skill):
        """Test skill initialization"""
        assert skill.name == "audit"

    def test_skill_examples(self, skill):
        """Test skill examples"""
        assert len(skill.examples) > 0