"""Test Verify Skill"""

import pytest
from pathlib import Path
from helix.skills.verify import (
    VerifySkill,
    CheckResult,
    VerifyReport,
    StaticChecker,
    TestRunner,
    AcceptanceChecker,
)


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


class TestCheckResult:
    """Test CheckResult dataclass"""

    def test_check_result_creation(self):
        """Test creating a check result"""
        result = CheckResult(name="test", status="pass", message="OK", duration_ms=100)
        assert result.name == "test"
        assert result.status == "pass"
        assert result.message == "OK"
        assert result.duration_ms == 100

    def test_check_result_defaults(self):
        """Test default values"""
        result = CheckResult(name="test", status="pass")
        assert result.message == ""
        assert result.duration_ms == 0
        assert result.details == {}


class TestVerifyReport:
    """Test VerifyReport dataclass"""

    def test_verify_report_creation(self):
        """Test creating a verify report"""
        static = CheckResult(name="static", status="pass")
        test = CheckResult(name="test", status="pass")
        acceptance = CheckResult(name="acceptance", status="pass")

        report = VerifyReport(
            timestamp="2024-01-01",
            duration_seconds=10.0,
            project_path="/test",
            static=static,
            test=test,
            acceptance=acceptance,
            overall="pass"
        )
        assert report.timestamp == "2024-01-01"
        assert report.overall == "pass"

    def test_verify_report_to_dict(self):
        """Test converting to dictionary"""
        static = CheckResult(name="static", status="pass")
        test = CheckResult(name="test", status="fail")
        acceptance = CheckResult(name="acceptance", status="skip")

        report = VerifyReport(
            timestamp="2024-01-01",
            duration_seconds=10.0,
            project_path="/test",
            static=static,
            test=test,
            acceptance=acceptance,
            overall="partial"
        )

        result = report.to_dict()
        assert result["timestamp"] == "2024-01-01"
        assert result["overall"] == "partial"
        assert result["levels"]["static"]["status"] == "pass"
        assert result["levels"]["test"]["status"] == "fail"


class TestStaticChecker:
    """Test StaticChecker class"""

    def test_static_checker_init(self):
        """Test initialization"""
        checker = StaticChecker(Path("/test"))
        assert checker.project_path == Path("/test")

    def test_static_checker_tools(self):
        """Test available tools"""
        assert "ruff" in StaticChecker.TOOLS
        assert "black" in StaticChecker.TOOLS
        assert "mypy" in StaticChecker.TOOLS


class TestTestRunner:
    """Test TestRunner class"""

    def test_test_runner_init(self):
        """Test initialization"""
        runner = TestRunner(Path("/test"))
        assert runner.project_path == Path("/test")


class TestAcceptanceChecker:
    """Test AcceptanceChecker class"""

    def test_acceptance_checker_init(self):
        """Test initialization"""
        checker = AcceptanceChecker(Path("/test"))
        assert checker.project_path == Path("/test")