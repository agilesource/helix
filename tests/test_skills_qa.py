"""Test QA Skill"""

import pytest
from helix.skills.qa import QASkill, TestLevel, TestFramework, TestResult, QAReport
from helix.skills.base import SkillConfig, SkillCategory


class TestQASkill:
    """Test QASkill"""

    @pytest.fixture
    def skill(self):
        config = SkillConfig()
        return QASkill(config)

    def test_skill_init(self, skill):
        """Test skill initialization"""
        assert skill.name == "qa"
        assert skill.category == SkillCategory.QUALITY

    def test_skill_examples(self, skill):
        """Test skill examples"""
        assert len(skill.examples) > 0

    def test_skill_description(self, skill):
        """Test skill description"""
        assert len(skill.description) > 0

    def test_skill_with_config(self, skill):
        """Test skill with config"""
        assert skill.config is not None


class TestTestLevel:
    """Test TestLevel class"""

    def test_test_level_values(self):
        """Test all test levels"""
        assert TestLevel.UNIT == "unit"
        assert TestLevel.INTEGRATION == "integration"
        assert TestLevel.E2E == "e2e"

    def test_test_level_count(self):
        """Test number of test levels"""
        assert hasattr(TestLevel, 'UNIT')
        assert hasattr(TestLevel, 'INTEGRATION')
        assert hasattr(TestLevel, 'E2E')


class TestTestFramework:
    """Test TestFramework class"""

    def test_test_framework_values(self):
        """Test all test frameworks"""
        assert TestFramework.PYTEST == "pytest"
        assert TestFramework.UNITTEST == "unittest"

    def test_test_framework_count(self):
        """Test number of frameworks"""
        assert hasattr(TestFramework, 'PYTEST')
        assert hasattr(TestFramework, 'UNITTEST')


class TestTestResult:
    """Test TestResult dataclass"""

    def test_test_result_creation(self):
        """Test creating a test result"""
        result = TestResult(
            passed=5,
            failed=1,
            skipped=0,
            errors=0,
            total=6,
            duration_seconds=10.0,
            coverage_percent=85.0
        )
        assert result.passed == 5
        assert result.failed == 1
        assert result.total == 6
        assert result.errors == 0

    def test_test_result_defaults(self):
        """Test default values"""
        result = TestResult(passed=10, failed=0, total=10)
        assert result.skipped == 0
        assert result.errors == 0
        assert result.duration_seconds == 0.0


class TestQAReport:
    """Test QAReport dataclass"""

    def test_qa_report_creation(self):
        """Test creating a QA report"""
        test_result = TestResult(passed=5, failed=1, total=6)
        report = QAReport(
            test_result=test_result,
            failed_tests=[],
            slow_tests=[]
        )
        assert report.test_result.passed == 5

    def test_qa_report_with_details(self):
        """Test QA report with details"""
        test_result = TestResult(passed=10, failed=2, total=12)
        report = QAReport(
            test_result=test_result,
            failed_tests=["test_login", "test_logout"],
            slow_tests=["test_database", "test_api"]
        )
        assert len(report.failed_tests) == 2
        assert len(report.slow_tests) == 2
        assert report.test_result.failed == 2