"""Test Review Skill"""

import pytest
from helix.skills.review import ReviewSkill, FindingSeverity, ReviewFinding, ReviewReport
from helix.skills.base import SkillCategory


class TestReviewSkill:
    """Test ReviewSkill"""

    @pytest.fixture
    def skill(self):
        return ReviewSkill()

    def test_skill_init(self, skill):
        """Test skill initialization"""
        assert skill.name == "review"
        assert skill.category == SkillCategory.QUALITY

    def test_skill_examples(self, skill):
        """Test skill examples"""
        assert len(skill.examples) > 0

    def test_skill_description(self, skill):
        """Test skill description"""
        assert len(skill.description) > 0


class TestFindingSeverity:
    """Test FindingSeverity"""

    def test_severity_values(self):
        """Test severity values"""
        assert FindingSeverity.CRITICAL == "critical"
        assert FindingSeverity.HIGH == "high"
        assert FindingSeverity.MEDIUM == "medium"
        assert FindingSeverity.LOW == "low"
        assert FindingSeverity.INFO == "info"


class TestReviewFinding:
    """Test ReviewFinding dataclass"""

    def test_review_finding_creation(self):
        """Test creating a review finding"""
        finding = ReviewFinding(
            severity="high",
            confidence=8,
            file_path="src/db.py",
            line_number=42,
            category="security",
            summary="SQL Injection Risk",
            description="Potential SQL injection",
            fix_suggestion="Use parameterized queries"
        )
        assert finding.severity == "high"
        assert finding.confidence == 8
        assert finding.category == "security"
        assert finding.file_path == "src/db.py"
        assert finding.line_number == 42

    def test_review_finding_with_minimal_args(self):
        """Test with minimal arguments"""
        finding = ReviewFinding(
            severity="info",
            confidence=5,
            file_path="test.py",
            line_number=1,
            category="style",
            summary="Minor issue",
            description="Description",
            fix_suggestion="Suggestion"
        )
        assert finding.severity == "info"
        assert finding.confidence == 5


class TestReviewReport:
    """Test ReviewReport dataclass"""

    def test_review_report_creation(self):
        """Test creating a review report"""
        findings = [
            ReviewFinding(
                severity="high",
                confidence=8,
                file_path="test.py",
                line_number=1,
                category="security",
                summary="Test",
                description="Test",
                fix_suggestion="Fix it"
            )
        ]
        report = ReviewReport(
            total_files=1,
            total_lines_changed=10,
            findings=findings,
            critical_count=0,
            high_count=1,
            medium_count=0,
            low_count=0,
            info_count=0
        )
        assert report.total_files == 1
        assert report.high_count == 1
        assert len(report.findings) == 1

    def test_review_report_empty(self):
        """Test empty report"""
        report = ReviewReport(
            total_files=0,
            total_lines_changed=0,
            findings=[],
            critical_count=0,
            high_count=0,
            medium_count=0,
            low_count=0,
            info_count=0
        )
        assert len(report.findings) == 0