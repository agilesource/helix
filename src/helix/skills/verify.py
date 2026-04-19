"""
/verify Skill - Automated Verification

Run static checks, unit tests, and acceptance tests.
"""

import asyncio
import json
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

from helix.skills.base import Skill, SkillResult, SkillConfig, SkillCategory, SkillStatus
from helix.core.intent import Intent, IntentType
from helix.core.context import HelixContext


# ============ Data Models ============

@dataclass
class CheckResult:
    """Check result"""
    name: str
    status: str  # pass, fail, skip, error
    message: str = ""
    duration_ms: int = 0
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VerifyReport:
    """Verification report"""
    timestamp: str
    duration_seconds: float
    project_path: str

    # Results for each level
    static: CheckResult
    test: CheckResult
    acceptance: CheckResult

    # Overall status
    overall: str  # pass, fail, partial

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "duration_seconds": self.duration_seconds,
            "project_path": self.project_path,
            "levels": {
                "static": {
                    "status": self.static.status,
                    "message": self.static.message,
                    "details": self.static.details,
                },
                "test": {
                    "status": self.test.status,
                    "message": self.test.message,
                    "details": self.test.details,
                },
                "acceptance": {
                    "status": self.acceptance.status,
                    "message": self.acceptance.message,
                    "details": self.acceptance.details,
                },
            },
            "overall": self.overall,
        }


# ============ Verifiers ============

class StaticChecker:
    """Static checker"""

    TOOLS = ["ruff", "black", "mypy"]

    def __init__(self, project_path: Path):
        self.project_path = project_path

    async def run(self) -> CheckResult:
        """Run static checks"""
        start = datetime.now()
        issues: list[str] = []
        passed = True

        # Check if ruff is available
        try:
            result = subprocess.run(
                ["ruff", "check", "."],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode != 0:
                issues.append(f"ruff: {result.stdout[:200]}")
                passed = False
        except FileNotFoundError:
            issues.append("ruff not installed, skipping")
        except subprocess.TimeoutExpired:
            issues.append("ruff timeout")
            passed = False

        # Check if mypy is available
        try:
            result = subprocess.run(
                ["mypy", "src", "--ignore-missing-imports"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode != 0:
                issues.append(f"mypy: {result.stdout[:200]}")
                passed = False
        except FileNotFoundError:
            issues.append("mypy not installed, skipping")
        except subprocess.TimeoutExpired:
            issues.append("mypy timeout")
            passed = False

        duration = (datetime.now() - start).total_seconds() * 1000

        return CheckResult(
            name="static",
            status="pass" if passed else "fail",
            message="; ".join(issues) if issues else "All checks passed",
            duration_ms=int(duration),
            details={"issues": issues}
        )


class TestRunner:
    """Test runner"""

    def __init__(self, project_path: Path):
        self.project_path = project_path

    async def run(self) -> CheckResult:
        """Run tests"""
        start = datetime.now()
        issues: list[str] = []
        passed = True
        test_details = {}

        # Check if pytest is available
        try:
            result = subprocess.run(
                ["pytest", "--tb=short", "-v"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=120
            )

            # Parse output
            output = result.stdout + result.stderr

            # Extract test statistics
            import re
            passed_match = re.search(r'(\d+) passed', output)
            failed_match = re.search(r'(\d+) failed', output)

            if passed_match:
                test_details["passed"] = int(passed_match.group(1))
            if failed_match:
                test_details["failed"] = int(failed_match.group(1))
                passed = False

            # Check if tests were collected
            if "no tests ran" in output.lower() or "no tests collected" in output.lower():
                test_details["collected"] = 0

            if result.returncode != 0:
                passed = False
                issues.append(f"pytest: {output[:300]}")

        except FileNotFoundError:
            issues.append("pytest not installed, skipping")
        except subprocess.TimeoutExpired:
            issues.append("pytest timeout")
            passed = False

        duration = (datetime.now() - start).total_seconds() * 1000

        return CheckResult(
            name="test",
            status="pass" if passed else "fail",
            message="; ".join(issues) if issues else "All tests passed",
            duration_ms=int(duration),
            details=test_details
        )


class AcceptanceChecker:
    """Acceptance test checker"""

    def __init__(self, project_path: Path):
        self.project_path = project_path

    async def run(self) -> CheckResult:
        """Check acceptance criteria"""
        start = datetime.now()
        issues: list[str] = []

        # Find SPEC.md
        spec_files = list(self.project_path.glob("SPEC.md"))
        spec_files.extend(self.project_path.glob("**/SPEC.md"))
        spec_files.extend(self.project_path.glob("docs/spec/*.md"))

        if not spec_files:
            return CheckResult(
                name="acceptance",
                status="skip",
                message="No SPEC.md found",
                duration_ms=0,
                details={}
            )

        # Read first SPEC
        spec_content = spec_files[0].read_text()

        # Extract acceptance criteria
        ac_items = []
        for line in spec_content.split('\n'):
            if '- [ ]' in line:
                ac_items.append(line.replace('- [ ]', '').strip())

        # Check test coverage
        # Simplified: check if test files exist
        test_files = list(self.project_path.glob("tests/*.py"))
        test_files.extend(self.project_path.glob("test_*.py"))

        has_tests = len(test_files) > 0

        duration = (datetime.now() - start).total_seconds() * 1000

        if has_tests:
            status = "partial"
            message = f"Found {len(ac_items)} AC, {len(test_files)} test files"
        else:
            status = "skip"
            message = "No tests found, cannot verify AC"

        return CheckResult(
            name="acceptance",
            status=status,
            message=message,
            duration_ms=int(duration),
            details={
                "ac_count": len(ac_items),
                "test_files": len(test_files),
                "ac_items": ac_items[:5]  # first 5
            }
        )


# ============ VerifySkill ============

class VerifySkill(Skill):
    """Automated verification skill"""

    name = "verify"
    description = "Run static checks, unit tests, and acceptance tests"
    category = SkillCategory.EXECUTION
    status = SkillStatus.DRAFT

    examples = [
        "helix verify",
        "helix verify ./src",
        "helix verify --level static",
    ]

    async def execute(self, intent: Intent, context: HelixContext) -> SkillResult:
        self.initialize()
        start_time = asyncio.get_event_loop().time()

        # Parse parameters
        project_path = intent.parameters.get('path', '.')
        level = intent.parameters.get('level', 'full')  # static, test, acceptance, full

        project = Path(project_path)
        if not project.exists():
            return SkillResult(
                success=False,
                message=f"Project path does not exist: {project_path}",
                skill_name=self.name
            )

        # Run checks for each level
        results = {}

        if level in ["static", "full"]:
            checker = StaticChecker(project)
            results["static"] = await checker.run()
        else:
            results["static"] = CheckResult(name="static", status="skip")

        if level in ["test", "full"]:
            runner = TestRunner(project)
            results["test"] = await runner.run()
        else:
            results["test"] = CheckResult(name="test", status="skip")

        if level in ["acceptance", "full"]:
            acceptor = AcceptanceChecker(project)
            results["acceptance"] = await acceptor.run()
        else:
            results["acceptance"] = CheckResult(name="acceptance", status="skip")

        # Calculate overall status
        statuses = [r.status for r in results.values() if r.status != "skip"]
        if all(s == "pass" for s in statuses):
            overall = "pass"
        elif any(s == "fail" for s in statuses):
            overall = "fail"
        else:
            overall = "partial"

        execution_time = int((asyncio.get_event_loop().time() - start_time) * 1000)

        # Generate report
        report = VerifyReport(
            timestamp=datetime.now().isoformat(),
            duration_seconds=execution_time / 1000,
            project_path=str(project),
            static=results.get("static", CheckResult("static", "skip")),
            test=results.get("test", CheckResult("test", "skip")),
            acceptance=results.get("acceptance", CheckResult("acceptance", "skip")),
            overall=overall
        )

        # Output human-readable report
        report_text = self._format_report(report)

        return SkillResult(
            success=overall != "fail",
            message=report_text,
            data=report.to_dict(),
            skill_name=self.name,
            execution_time_ms=execution_time,
        )

    def _format_report(self, report: VerifyReport) -> str:
        """Format report for human readability"""
        lines = [
            "╭───────────────────────── Verification Report ──────────────────────────╮",
            f"│ Project: {report.project_path}",
            f"│ Duration: {report.duration_seconds:.2f}s",
            "├──────────────────────────────────────────────────────────────┤",
        ]

        # Static check
        static = report.static
        status_icon = "✓" if static.status == "pass" else "✗" if static.status == "fail" else "-"
        lines.append(f"│ Static       {status_icon} {static.status.upper()} ({static.duration_ms}ms)")

        # Test
        test = report.test
        status_icon = "✓" if test.status == "pass" else "✗" if test.status == "fail" else "-"
        cov = test.details.get("coverage", "N/A")
        lines.append(f"│ Unit Test    {status_icon} {test.status.upper()} (coverage: {cov})")

        # Acceptance
        acc = report.acceptance
        status_icon = "✓" if acc.status == "pass" else "⚠" if acc.status == "partial" else "-"
        lines.append(f"│ Acceptance   {status_icon} {acc.status.upper()}")

        # Overall
        overall_icon = "✓" if report.overall == "pass" else "⚠" if report.overall == "partial" else "✗"
        lines.append("├──────────────────────────────────────────────────────────────┤")
        lines.append(f"│ Overall:     {overall_icon} {report.overall.upper()}")
        lines.append("╰──────────────────────────────────────────────────────────────╯")

        return "\n".join(lines)
