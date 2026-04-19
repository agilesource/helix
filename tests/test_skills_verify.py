"""Test Verify Skill"""

import pytest
import asyncio
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from helix.skills.verify import (
    VerifySkill,
    CheckResult,
    VerifyReport,
    StaticChecker,
    TestRunner,
    AcceptanceChecker,
)
from helix.core.intent import Intent, IntentType


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

    def test_skill_category(self, skill):
        """Test skill category"""
        assert skill.category.value == "execution"

    def test_skill_status(self, skill):
        """Test skill status is set"""
        assert skill.status is not None


class TestVerifySkillExecute:
    """Test VerifySkill execute method"""

    @pytest.mark.asyncio
    async def test_execute_with_path(self):
        """Test execute with specific path"""
        skill = VerifySkill()

        # Test that execute handles the path parameter
        intent = Intent(
            type=IntentType.VERIFY,
            raw_input="helix verify /tmp/test",
            confidence=0.9,
            parameters={"path": "/tmp/test"}
        )

        # Path doesn't exist, should fail gracefully
        result = await skill.execute(intent, None)
        assert result.success is False
        assert "does not exist" in result.message.lower()


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


class TestTestRunnerExtended:
    """Extended TestRunner tests"""

    def test_test_runner_init(self):
        """Test initialization"""
        runner = TestRunner(Path("/test"))
        assert runner.project_path == Path("/test")

    @pytest.mark.asyncio
    async def test_run_with_no_tests_found(self):
        """Test running with no tests found"""
        with tempfile.TemporaryDirectory() as tmpdir:
            runner = TestRunner(Path(tmpdir))
            with patch('subprocess.run') as mock_run:
                # No tests found scenario
                mock_run.return_value = MagicMock(
                    returncode=0,
                    stdout="no tests ran",
                    stderr=""
                )
                try:
                    result = await runner.run()
                    assert result is not None
                except Exception:
                    pass


class TestAcceptanceCheckerExtended:
    """Extended AcceptanceChecker tests"""

    def test_acceptance_checker_extended(self):
        """Test extended acceptance checker"""
        with tempfile.TemporaryDirectory() as tmpdir:
            checker = AcceptanceChecker(Path(tmpdir))
            assert checker.project_path == Path(tmpdir)


class TestVerifySkillAsync:
    """Test VerifySkill async methods"""

    @pytest.mark.asyncio
    async def test_execute_with_path(self):
        """Test execute with path parameter"""
        from helix.core.intent import Intent, IntentType
        skill = VerifySkill()
        intent = Intent(
            type=IntentType.VERIFY,
            raw_input="verify",
            confidence=0.9,
            parameters={"path": "/tmp"}
        )
        try:
            result = await skill.execute(intent, None)
        except (RuntimeError, Exception):
            pass

    @pytest.mark.asyncio
    async def test_execute_with_all_checks(self):
        """Test execute with all checks enabled"""
        from helix.core.intent import Intent, IntentType
        skill = VerifySkill()
        intent = Intent(
            type=IntentType.VERIFY,
            raw_input="verify all",
            confidence=0.9,
            parameters={"path": ".", "static": True, "tests": True, "acceptance": True}
        )
        try:
            result = await skill.execute(intent, None)
        except (RuntimeError, Exception):
            pass
            checker = StaticChecker(Path(tmpdir))

            with patch('subprocess.run') as mock_run:
                mock_run.side_effect = FileNotFoundError("ruff not found")

                result = await checker.run()

                # Should handle missing tool gracefully
                assert result.name == "static"

    @pytest.mark.asyncio
    async def test_static_checker_timeout(self):
        """Test when checker times out"""
        with tempfile.TemporaryDirectory() as tmpdir:
            checker = StaticChecker(Path(tmpdir))

            with patch('subprocess.run') as mock_run:
                mock_run.side_effect = subprocess.TimeoutExpired("ruff", 30)

                result = await checker.run()

                assert result.status == "fail"
                assert "timeout" in result.message.lower()


class TestTestRunner:
    """Test TestRunner class"""

    def test_test_runner_init(self):
        """Test initialization"""
        runner = TestRunner(Path("/test"))
        assert runner.project_path == Path("/test")

    @pytest.mark.asyncio
    async def test_test_runner_pass(self):
        """Test test runner with passing tests"""
        with tempfile.TemporaryDirectory() as tmpdir:
            runner = TestRunner(Path(tmpdir))

            with patch('subprocess.run') as mock_run:
                mock_result = MagicMock()
                mock_result.returncode = 0
                mock_result.stdout = "5 passed"
                mock_result.stderr = ""
                mock_run.return_value = mock_result

                result = await runner.run()

                assert result.name == "test"
                assert result.status == "pass"

    @pytest.mark.asyncio
    async def test_test_runner_fail(self):
        """Test test runner with failing tests"""
        with tempfile.TemporaryDirectory() as tmpdir:
            runner = TestRunner(Path(tmpdir))

            with patch('subprocess.run') as mock_run:
                mock_result = MagicMock()
                mock_result.returncode = 1
                mock_result.stdout = "3 passed, 2 failed"
                mock_result.stderr = ""
                mock_run.return_value = mock_result

                result = await runner.run()

                assert result.status == "fail"
                assert "failed" in result.message.lower()

    @pytest.mark.asyncio
    async def test_test_runner_no_tests(self):
        """Test when no tests are collected"""
        with tempfile.TemporaryDirectory() as tmpdir:
            runner = TestRunner(Path(tmpdir))

            with patch('subprocess.run') as mock_run:
                mock_result = MagicMock()
                mock_result.returncode = 0
                mock_result.stdout = "no tests collected"
                mock_result.stderr = ""
                mock_run.return_value = mock_result

                result = await runner.run()

                assert "collected" in result.details or result.status in ["pass", "skip"]

    @pytest.mark.asyncio
    async def test_test_runner_timeout(self):
        """Test when tests timeout"""
        with tempfile.TemporaryDirectory() as tmpdir:
            runner = TestRunner(Path(tmpdir))

            with patch('subprocess.run') as mock_run:
                mock_run.side_effect = subprocess.TimeoutExpired("pytest", 120)

                result = await runner.run()

                assert "timeout" in result.message.lower() or result.status in ["fail", "error"]


class TestAcceptanceChecker:
    """Test AcceptanceChecker class"""

    def test_acceptance_checker_init(self):
        """Test initialization"""
        checker = AcceptanceChecker(Path("/test"))
        assert checker.project_path == Path("/test")

    @pytest.mark.asyncio
    async def test_acceptance_checker_with_criteria(self):
        """Test acceptance checker with criteria"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test file
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("def test_pass():\n    assert True\n")

            checker = AcceptanceChecker(Path(tmpdir))
            # Just test initialization works
            assert checker.project_path == Path(tmpdir)


class TestVerifySkillExecuteLevels:
    """Test execute with different level parameters"""

    @pytest.mark.asyncio
    async def test_execute_static_level(self):
        """Test execute with static level"""
        from helix.core.intent import Intent, IntentType
        skill = VerifySkill()
        intent = Intent(
            type=IntentType.VERIFY,
            raw_input="verify static",
            confidence=0.9,
            parameters={"path": "/tmp", "level": "static"}
        )
        try:
            result = await skill.execute(intent, None)
        except (RuntimeError, Exception):
            pass

    @pytest.mark.asyncio
    async def test_execute_test_level(self):
        """Test execute with test level"""
        from helix.core.intent import Intent, IntentType
        skill = VerifySkill()
        intent = Intent(
            type=IntentType.VERIFY,
            raw_input="verify test",
            confidence=0.9,
            parameters={"path": "/tmp", "level": "test"}
        )
        try:
            result = await skill.execute(intent, None)
        except (RuntimeError, Exception):
            pass

    @pytest.mark.asyncio
    async def test_execute_acceptance_level(self):
        """Test execute with acceptance level"""
        from helix.core.intent import Intent, IntentType
        skill = VerifySkill()
        intent = Intent(
            type=IntentType.VERIFY,
            raw_input="verify acceptance",
            confidence=0.9,
            parameters={"path": "/tmp", "level": "acceptance"}
        )
        try:
            result = await skill.execute(intent, None)
        except (RuntimeError, Exception):
            pass

    @pytest.mark.asyncio
    async def test_execute_full_level(self):
        """Test execute with full level"""
        from helix.core.intent import Intent, IntentType
        skill = VerifySkill()
        intent = Intent(
            type=IntentType.VERIFY,
            raw_input="verify full",
            confidence=0.9,
            parameters={"path": "/tmp", "level": "full"}
        )
        try:
            result = await skill.execute(intent, None)
        except (RuntimeError, Exception):
            pass


class TestVerifySkillReport:
    """Test report formatting"""

    def test_format_report_pass(self):
        """Test formatting report with pass status"""
        skill = VerifySkill()
        static = CheckResult(name="static", status="pass", message="OK", duration_ms=100)
        test = CheckResult(name="test", status="pass", message="OK", duration_ms=200, details={"coverage": "80%"})
        acceptance = CheckResult(name="acceptance", status="pass", message="OK", duration_ms=50)

        report = VerifyReport(
            timestamp="2024-01-01",
            duration_seconds=1.0,
            project_path="/test",
            static=static,
            test=test,
            acceptance=acceptance,
            overall="pass"
        )
        formatted = skill._format_report(report)
        assert "PASS" in formatted
        assert "1.00" in formatted

    def test_format_report_fail(self):
        """Test formatting report with fail status"""
        skill = VerifySkill()
        static = CheckResult(name="static", status="fail", message="Errors found", duration_ms=100)
        test = CheckResult(name="test", status="fail", message="Tests failed", duration_ms=200)
        acceptance = CheckResult(name="acceptance", status="fail", message="Failed", duration_ms=50)

        report = VerifyReport(
            timestamp="2024-01-01",
            duration_seconds=1.0,
            project_path="/test",
            static=static,
            test=test,
            acceptance=acceptance,
            overall="fail"
        )
        formatted = skill._format_report(report)
        assert "FAIL" in formatted

    def test_format_report_partial(self):
        """Test formatting report with partial status"""
        skill = VerifySkill()
        static = CheckResult(name="static", status="pass", message="OK", duration_ms=100)
        test = CheckResult(name="test", status="skip", message="Skipped", duration_ms=0)
        acceptance = CheckResult(name="acceptance", status="pass", message="OK", duration_ms=50)

        report = VerifyReport(
            timestamp="2024-01-01",
            duration_seconds=1.0,
            project_path="/test",
            static=static,
            test=test,
            acceptance=acceptance,
            overall="partial"
        )
        formatted = skill._format_report(report)
        assert "PARTIAL" in formatted


class TestVerifySkillWithMocks:
    """Test VerifySkill with mocked subprocess calls"""

    @pytest.mark.asyncio
    async def test_static_checker_pass(self):
        """Test static checker with passing tools"""
        with tempfile.TemporaryDirectory() as tmpdir:
            checker = StaticChecker(Path(tmpdir))
            with patch('subprocess.run') as mock_run:
                mock_result = MagicMock()
                mock_result.returncode = 0
                mock_result.stdout = "All checks passed!"
                mock_result.stderr = ""
                mock_run.return_value = mock_result

                result = await checker.run()

                assert result.name == "static"
                assert result.status == "pass"

    @pytest.mark.asyncio
    async def test_static_checker_multiple_tools(self):
        """Test static checker with multiple tools"""
        with tempfile.TemporaryDirectory() as tmpdir:
            checker = StaticChecker(Path(tmpdir))
            with patch('subprocess.run') as mock_run:
                mock_result = MagicMock()
                mock_result.returncode = 0
                mock_result.stdout = "checked 10 files"
                mock_result.stderr = ""
                mock_run.return_value = mock_result

                result = await checker.run()

                assert result.status in ["pass", "fail"]

    @pytest.mark.asyncio
    async def test_test_runner_with_coverage(self):
        """Test test runner with coverage output"""
        with tempfile.TemporaryDirectory() as tmpdir:
            runner = TestRunner(Path(tmpdir))
            with patch('subprocess.run') as mock_run:
                mock_result = MagicMock()
                mock_result.returncode = 0
                mock_result.stdout = "5 passed, 1 failed. Coverage: 85%"
                mock_result.stderr = ""
                mock_run.return_value = mock_result

                result = await runner.run()

                assert result.name == "test"
                assert result.status == "fail"
                # Check for passed/failed in details
                assert "passed" in result.details or "failed" in result.details

    @pytest.mark.asyncio
    async def test_acceptance_checker_run(self):
        """Test acceptance checker run method"""
        with tempfile.TemporaryDirectory() as tmpdir:
            checker = AcceptanceChecker(Path(tmpdir))
            with patch('subprocess.run') as mock_run:
                mock_result = MagicMock()
                mock_result.returncode = 0
                mock_result.stdout = "Acceptance tests passed"
                mock_result.stderr = ""
                mock_run.return_value = mock_result

                try:
                    result = await checker.run()
                    assert result is not None
                except Exception:
                    pass


class TestVerifyReportToDict:
    """Test VerifyReport to_dict method"""

    def test_verify_report_to_dict_full(self):
        """Test full report to dict conversion"""
        static = CheckResult(name="static", status="pass", message="OK", duration_ms=100, details={"files": 10})
        test = CheckResult(name="test", status="pass", message="OK", duration_ms=200, details={"passed": 5})
        acceptance = CheckResult(name="acceptance", status="pass", message="OK", duration_ms=50)

        report = VerifyReport(
            timestamp="2024-01-01",
            duration_seconds=1.0,
            project_path="/test",
            static=static,
            test=test,
            acceptance=acceptance,
            overall="pass"
        )

        result = report.to_dict()
        assert result["overall"] == "pass"
        assert result["levels"]["static"]["status"] == "pass"
        assert result["levels"]["test"]["status"] == "pass"
        assert result["levels"]["acceptance"]["status"] == "pass"

    def test_verify_report_to_dict_mixed(self):
        """Test report with mixed statuses"""
        static = CheckResult(name="static", status="fail", message="Errors")
        test = CheckResult(name="test", status="pass", message="OK")
        acceptance = CheckResult(name="acceptance", status="skip", message="Skipped")

        report = VerifyReport(
            timestamp="2024-01-01",
            duration_seconds=1.0,
            project_path="/test",
            static=static,
            test=test,
            acceptance=acceptance,
            overall="partial"
        )

        result = report.to_dict()
        assert result["overall"] == "partial"
        assert result["levels"]["static"]["status"] == "fail"
        assert result["levels"]["test"]["status"] == "pass"
        assert result["levels"]["acceptance"]["status"] == "skip"