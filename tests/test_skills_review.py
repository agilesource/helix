"""Test Review Skill"""

import pytest
from helix.skills.review import ReviewSkill, FindingSeverity


class TestReviewSkill:
    """Test ReviewSkill"""

    @pytest.fixture
    def skill(self):
        return ReviewSkill()

    def test_skill_init(self, skill):
        """Test skill initialization"""
        assert skill.name == "review"

    def test_skill_examples(self, skill):
        """Test skill examples"""
        assert len(skill.examples) > 0


class TestFindingSeverity:
    """Test FindingSeverity"""

    def test_severity_values(self):
        """Test severity values"""
        assert FindingSeverity.CRITICAL == "critical"
        assert FindingSeverity.HIGH == "high"
        assert FindingSeverity.MEDIUM == "medium"
        assert FindingSeverity.LOW == "low"
        assert FindingSeverity.INFO == "info"