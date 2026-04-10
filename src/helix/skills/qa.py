"""
Helix QA Skill - Testing Automation

This skill handles automated testing:
- Run unit tests
- Run integration tests
- Generate test reports
- Coverage analysis
- Test result tracking
"""

import asyncio
import subprocess
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime

from helix.skills.base import (
    Skill, SkillResult, SkillConfig, SkillCategory, SkillStatus
)
from helix.core.intent import Intent, IntentType
from helix.core.context import HelixContext


class TestLevel:
    """Test levels"""
    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"
    ALL = "all"


class TestFramework:
    """Supported test frameworks"""
    PYTEST = "pytest"
    UNITTEST = "unittest"
    PYTEST_JSON = "pytest-json-report"


@dataclass
class TestResult:
    """Test execution result"""
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    errors: int = 0
    total: int = 0
    duration_seconds: float = 0.0
    coverage_percent: Optional[float] = None


@dataclass
class QAReport:
    """QA report"""
    test_result: TestResult
    failed_tests: List[Dict[str, str]] = field(default_factory=list)
    slow_tests: List[Dict[str, float]] = field(default_factory=list)
    coverage_report: Optional[str] = None


class QASkill(Skill):
    """
    QA Skill - Testing Automation

    Automated testing with coverage analysis and reporting
    """

    name = "qa"
    description = "Testing automation - run tests, coverage analysis, and reports"
    category = SkillCategory.QUALITY
    status = SkillStatus.EXPERIMENTAL

    examples = [
        "helix qa",
        "helix qa --level unit",
        "helix qa --level all --coverage",
    ]

    def __init__(self, config: Optional[SkillConfig] = None):
        super().__init__(config)
        self.test_level = TestLevel.ALL
        self.run_coverage = False
        self.test_path = "."
        self.fail_fast = False

    def _do_initialize(self) -> None:
        """Initialize QA skill"""
        pass

    async def execute(self, intent: Intent, intent_context: Optional[HelixContext]) -> SkillResult:
        """Execute QA skill"""
        start_time = asyncio.get_event_loop().time()

        # Parse parameters
        params = intent.parameters
        self.test_level = params.get("level", TestLevel.ALL)
        self.run_coverage = params.get("coverage", False)
        self.test_path = params.get("path", ".")
        self.fail_fast = params.get("fail_fast", False)

        try:
            # Run tests
            report = await self._run_tests()

            # Calculate execution time
            execution_time = int((asyncio.get_event_loop().time() - start_time) * 1000)

            # Prepare result
            result = SkillResult(
                success=report.test_result.failed == 0 and report.test_result.errors == 0,
                message=self._format_report(report),
                data={
                    "test_result": {
                        "passed": report.test_result.passed,
                        "failed": report.test_result.failed,
                        "skipped": report.test_result.skipped,
                        "errors": report.test_result.errors,
                        "total": report.test_result.total,
                        "duration": report.test_result.duration_seconds,
                        "coverage": report.test_result.coverage_percent,
                    },
                    "failed_tests": report.failed_tests,
                    "slow_tests": report.slow_tests[:5],  # Top 5 slow
                },
                execution_time_ms=execution_time,
            )

            return result

        except Exception as e:
            return SkillResult(
                success=False,
                message=f"QA failed: {str(e)}",
                errors=[str(e)]
            )

    async def _run_tests(self) -> QAReport:
        """Run tests and generate report"""
        report = QAReport(test_result=TestResult())

        # Detect test framework
        framework = self._detect_framework()

        if framework == TestFramework.PYTEST:
            report = await self._run_pytest()
        else:
            # Fallback to basic test discovery
            report = await self._run_basic_tests()

        return report

    def _detect_framework(self) -> str:
        """Detect test framework"""
        if Path("pytest.ini").exists():
            return TestFramework.PYTEST
        if Path("pyproject.toml").exists():
            content = Path("pyproject.toml").read_text()
            if "[tool.pytest" in content or "pytest" in content:
                return TestFramework.PYTEST
        if Path("tests").exists() or Path("test").exists():
            return TestFramework.PYTEST
        return TestFramework.UNITTEST

    async def _run_pytest(self) -> QAReport:
        """Run pytest tests"""
        report = QAReport(test_result=TestResult())

        # Build pytest command
        cmd = ["python", "-m", "pytest", self.test_path, "-v", "--tb=short"]

        # Add JSON report if available
        json_report_file = "/tmp/qa_report.json"
        cmd.extend(["--json-report", "--json-report-file", json_report_file])

        if self.run_coverage:
            cmd.extend(["--cov", ".", "--cov-report", "term-missing"])

        if self.fail_fast:
            cmd.append("-x")

        # Set environment for JSON report
        env = os.environ.copy()
        env["PYTEST_JSON_REPORT"] = "true"

        # Run tests
        result = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
        )

        stdout, stderr = await result.communicate()
        output = stdout.decode()

        # Parse output
        report = self._parse_pytest_output(output, stderr.decode())

        return report

    def _parse_pytest_output(self, stdout: str, stderr: str) -> QAReport:
        """Parse pytest output"""
        report = QAReport(test_result=TestResult())

        output = stdout + stderr

        # Parse test results
        import re

        # Match: "5 passed, 2 failed, 1 skipped in 2.34s"
        summary_match = re.search(
            r'(\d+)\s+passed[^,]*,\s*(\d+)\s+failed[^,]*,\s*(\d+)\s+skipped.*?(\d+\.?\d*)s',
            output
        )
        if summary_match:
            report.test_result.passed = int(summary_match.group(1))
            report.test_result.failed = int(summary_match.group(2))
            report.test_result.skipped = int(summary_match.group(3))
            report.test_result.duration_seconds = float(summary_match.group(4))
        else:
            # Alternative: "5 passed in 1.23s"
            passed_match = re.search(r'(\d+)\s+passed\s+(?:in\s+)?(\d+\.?\d*)s', output)
            if passed_match:
                report.test_result.passed = int(passed_match.group(1))
                report.test_result.duration_seconds = float(passed_match.group(2))

        report.test_result.total = (
            report.test_result.passed +
            report.test_result.failed +
            report.test_result.skipped +
            report.test_result.errors
        )

        # Parse coverage
        coverage_match = re.search(r'TOTAL\s+\d+\s+\d+\s+(\d+)%', output)
        if coverage_match:
            report.test_result.coverage_percent = float(coverage_match.group(1))

        # Parse failed tests
        failed_section = re.search(r'FAILED.*?(?=====|$)', output, re.DOTALL)
        if failed_section:
            failed_lines = failed_section.group(0).split('\n')
            for line in failed_lines:
                if '::' in line and 'FAILED' in line:
                    test_name = line.split('::')[-1].split(' - ')[0].strip()
                    report.failed_tests.append({
                        "name": test_name,
                        "error": line.split(' - ')[-1].strip() if ' - ' in line else "Test failed"
                    })

        # Parse slow tests
        slow_match = re.search(r'slowest durations.*?(?====|$)', output, re.DOTALL)
        if slow_match:
            duration_lines = slow_match.group(0).split('\n')
            for line in duration_lines:
                if 's' in line and '<' not in line:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        try:
                            duration = float(parts[0].rstrip('s'))
                            test_name = ' '.join(parts[1:])
                            report.slow_tests.append({"name": test_name, "duration": duration})
                        except ValueError:
                            pass

        return report

    async def _run_basic_tests(self) -> QAReport:
        """Run basic tests without pytest"""
        report = QAReport(test_result=TestResult())

        # Try unittest discovery
        result = await asyncio.create_subprocess_exec(
            "python", "-m", "unittest", "discover", "-v",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await result.communicate()
        output = stdout.decode() + stderr.decode()

        # Parse results
        import re
        summary_match = re.search(r'Ran (\d+) tests in ([\d.]+)s', output)
        if summary_match:
            report.test_result.total = int(summary_match.group(1))
            report.test_result.duration_seconds = float(summary_match.group(2))

            if 'OK' in output:
                report.test_result.passed = report.test_result.total
            else:
                failed_match = re.search(r'Failed: (\d+)', output)
                if failed_match:
                    report.test_result.failed = int(failed_match.group(1))
                    report.test_result.passed = report.test_result.total - report.test_result.failed

        return report

    def _format_report(self, report: QAReport) -> str:
        """Format QA report"""
        tr = report.test_result

        lines = [
            "=" * 50,
            "QA Test Report",
            "=" * 50,
            "",
            f"Test Results:",
            f"  Passed:  [green]{tr.passed}[/green]",
            f"  Failed:  [red]{tr.failed}[/red]",
            f"  Skipped: [yellow]{tr.skipped}[/yellow]",
            f"  Errors:  [red]{tr.errors}[/red]",
            f"  Total:   {tr.total}",
            f"  Duration: {tr.duration_seconds:.2f}s",
            "",
        ]

        if tr.coverage_percent is not None:
            lines.append(f"Coverage:  {tr.coverage_percent:.1f}%")
            lines.append("")

        if report.failed_tests:
            lines.append("Failed Tests:")
            for test in report.failed_tests[:5]:
                lines.append(f"  [red]✗[/red] {test['name']}")
                lines.append(f"      {test['error'][:60]}...")
            lines.append("")

        if report.slow_tests:
            lines.append("Slow Tests:")
            for test in report.slow_tests[:3]:
                lines.append(f"  [yellow]⏱[/yellow] {test['name']} ({test['duration']:.2f}s)")
            lines.append("")

        # Status
        if tr.failed == 0 and tr.errors == 0:
            lines.append("[green]✓ All tests passed![/green]")
        else:
            lines.append(f"[red]✗ {tr.failed + tr.errors} tests failed[/red]")

        lines.append("=" * 50)

        return "\n".join(lines)
