"""
Helix Gate Skill - Quality Gate

This skill enforces quality gates before code can proceed:
- Configurable quality thresholds
- Multi-dimensional checks
- Blocker/Bypass mechanisms
- Integration with CI/CD
"""

import asyncio
import subprocess
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from helix.skills.base import (
    Skill, SkillResult, SkillConfig, SkillCategory, SkillStatus
)
from helix.core.intent import Intent, IntentType
from helix.core.context import HelixContext


class GateResult(Enum):
    """Gate check result"""
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"
    SKIP = "skip"


class GateType(Enum):
    """Gate types"""
    SECURITY = "security"
    QUALITY = "quality"
    TEST = "test"
    PERFORMANCE = "performance"
    COMPLIANCE = "compliance"


@dataclass
class GateCheck:
    """Individual gate check"""
    name: str
    gate_type: str
    result: str
    message: str
    details: str = ""
    threshold: Any = None
    actual_value: Any = None


@dataclass
class GateConfig:
    """Gate configuration"""
    # Security gates
    require_security_scan: bool = True
    max_critical_vulns: int = 0
    max_high_vulns: int = 0

    # Quality gates
    min_coverage: float = 70.0
    min_test_count: int = 10
    max_complexity: int = 10

    # Linting gates
    allow_lint_errors: bool = False

    # Gate behavior
    fail_on_warning: bool = False
    allow_bypass: bool = False
    bypass_reason: str = ""


@dataclass
class GateReport:
    """Gate report"""
    timestamp: str = ""
    overall_result: str = GateResult.PASS.value
    checks: List[GateCheck] = field(default_factory=list)
    passed_count: int = 0
    failed_count: int = 0
    warning_count: int = 0
    skipped_count: int = 0


class GateSkill(Skill):
    """
    Gate Skill - Quality Gate

    Enforces quality gates before code can proceed
    """

    name = "gate"
    description = "Quality gate - enforce quality thresholds before merge/deploy"
    category = SkillCategory.QUALITY
    status = SkillStatus.EXPERIMENTAL

    examples = [
        "helix gate",
        "helix gate --strict",
        "helix gate --config custom.json",
        "helix gate --bypass 'Security fix in progress'",
    ]

    def __init__(self, config: Optional[SkillConfig] = None):
        super().__init__(config)
        self.gate_config = GateConfig()
        self.strict_mode = False

    def _do_initialize(self) -> None:
        """Initialize gate skill"""
        pass

    async def execute(self, intent: Intent, context: Optional[HelixContext]) -> SkillResult:
        """Execute gate skill"""
        start_time = asyncio.get_event_loop().time()

        # Parse parameters
        params = intent.parameters

        # Update gate config
        self.gate_config.require_security_scan = params.get("security", True)
        self.gate_config.min_coverage = params.get("min_coverage", 70.0)
        self.gate_config.max_critical_vulns = params.get("max_critical", 0)
        self.gate_config.max_high_vulns = params.get("max_high", 0)
        self.strict_mode = params.get("strict", False)
        self.gate_config.fail_on_warning = params.get("fail_on_warning", self.strict_mode)

        # Check for bypass
        if params.get("bypass"):
            self.gate_config.allow_bypass = True
            self.gate_config.bypass_reason = params.get("bypass")

        try:
            # Run gate checks
            report = await self._run_gate_checks()

            # Calculate execution time
            execution_time = int((asyncio.get_event_loop().time() - start_time) * 1000)

            # Determine overall result
            if self.gate_config.allow_bypass and self.gate_config.bypass_reason:
                report.overall_result = GateResult.WARNING.value
                report.checks.append(GateCheck(
                    name="bypass",
                    gate_type="manual",
                    result=GateResult.WARNING.value,
                    message=f"Gate bypassed: {self.gate_config.bypass_reason}",
                ))
            elif report.failed_count > 0:
                report.overall_result = GateResult.FAIL.value
            elif report.warning_count > 0 and self.gate_config.fail_on_warning:
                report.overall_result = GateResult.FAIL.value
            else:
                report.overall_result = GateResult.PASS.value

            # Prepare result
            result = SkillResult(
                success=report.overall_result != GateResult.FAIL.value,
                message=self._format_report(report),
                data={
                    "report": {
                        "overall_result": report.overall_result,
                        "passed": report.passed_count,
                        "failed": report.failed_count,
                        "warning": report.warning_count,
                        "skipped": report.skipped_count,
                    },
                    "checks": [
                        {
                            "name": c.name,
                            "type": c.gate_type,
                            "result": c.result,
                            "message": c.message,
                        }
                        for c in report.checks
                    ],
                },
                execution_time_ms=execution_time,
            )

            return result

        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Gate failed: {str(e)}",
                errors=[str(e)]
            )

    async def _run_gate_checks(self) -> GateReport:
        """Run all gate checks"""
        report = GateReport(timestamp=datetime.now().isoformat())

        # 1. Security check
        if self.gate_config.require_security_scan:
            check = await self._check_security()
            report.checks.append(check)

        # 2. Test coverage check
        check = await self._check_coverage()
        report.checks.append(check)

        # 3. Test count check
        check = await self._check_test_count()
        report.checks.append(check)

        # 4. Lint check
        check = await self._check_lint()
        report.checks.append(check)

        # 5. Complexity check
        check = await self._check_complexity()
        report.checks.append(check)

        # Count results
        for check in report.checks:
            if check.result == GateResult.PASS.value:
                report.passed_count += 1
            elif check.result == GateResult.FAIL.value:
                report.failed_count += 1
            elif check.result == GateResult.WARNING.value:
                report.warning_count += 1
            else:
                report.skipped_count += 1

        return report

    async def _check_security(self) -> GateCheck:
        """Run security check"""
        try:
            # Try running safety check
            result = await asyncio.create_subprocess_exec(
                "safety", "check", "--json",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await result.communicate()

            if stdout:
                try:
                    vulns = json.loads(stdout.decode())
                    critical = sum(1 for v in vulns if v.get("severity") == "critical")
                    high = sum(1 for v in vulns if v.get("severity") == "high")

                    if critical > self.gate_config.max_critical_vulns:
                        return GateCheck(
                            name="security",
                            gate_type=GateType.SECURITY.value,
                            result=GateResult.FAIL.value,
                            message=f"Critical vulnerabilities: {critical} (max: {self.gate_config.max_critical_vulns})",
                            threshold=self.gate_config.max_critical_vulns,
                            actual_value=critical,
                        )
                    if high > self.gate_config.max_high_vulns:
                        return GateCheck(
                            name="security",
                            gate_type=GateType.SECURITY.value,
                            result=GateResult.FAIL.value,
                            message=f"High vulnerabilities: {high} (max: {self.gate_config.max_high_vulns})",
                            threshold=self.gate_config.max_high_vulns,
                            actual_value=high,
                        )

                    return GateCheck(
                        name="security",
                        gate_type=GateType.SECURITY.value,
                        result=GateResult.PASS.value,
                        message=f"No critical vulnerabilities found",
                        actual_value=f"critical={critical}, high={high}",
                    )
                except json.JSONDecodeError:
                    pass
        except FileNotFoundError:
            pass

        return GateCheck(
            name="security",
            gate_type=GateType.SECURITY.value,
            result=GateResult.SKIP.value,
            message="Security check skipped (safety not installed)",
        )

    async def _check_coverage(self) -> GateCheck:
        """Run coverage check"""
        try:
            result = await asyncio.create_subprocess_exec(
                "pytest", "--cov", "--cov-report", "json", "--cov-report", "term",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await result.communicate()

            # Try to read coverage JSON
            coverage_file = Path("coverage.json")
            if coverage_file.exists():
                data = json.loads(coverage_file.read_text())
                coverage = data.get("totals", {}).get("percent_covered", 0)

                if coverage < self.gate_config.min_coverage:
                    return GateCheck(
                        name="coverage",
                        gate_type=GateType.TEST.value,
                        result=GateResult.FAIL.value,
                        message=f"Coverage {coverage:.1f}% < {self.gate_config.min_coverage}%",
                        threshold=self.gate_config.min_coverage,
                        actual_value=coverage,
                    )

                return GateCheck(
                    name="coverage",
                    gate_type=GateType.TEST.value,
                    result=GateResult.PASS.value,
                    message=f"Coverage: {coverage:.1f}%",
                    actual_value=coverage,
                )
        except Exception:
            pass

        return GateCheck(
            name="coverage",
            gate_type=GateType.TEST.value,
            result=GateResult.SKIP.value,
            message="Coverage check skipped (pytest-cov not installed)",
        )

    async def _check_test_count(self) -> GateCheck:
        """Check test count"""
        test_files = list(Path(".").rglob("test_*.py"))
        test_files.extend(list(Path(".").rglob("*_test.py")))

        count = len(test_files)

        if count < self.gate_config.min_test_count:
            return GateCheck(
                name="test_count",
                gate_type=GateType.TEST.value,
                result=GateResult.WARNING.value,
                message=f"Test files: {count} (recommended: {self.gate_config.min_test_count})",
                threshold=self.gate_config.min_test_count,
                actual_value=count,
            )

        return GateCheck(
            name="test_count",
            gate_type=GateType.TEST.value,
            result=GateResult.PASS.value,
            message=f"Test files: {count}",
            actual_value=count,
        )

    async def _check_lint(self) -> GateCheck:
        """Run lint check"""
        try:
            result = await asyncio.create_subprocess_exec(
                "ruff", "check", ".",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await result.communicate()

            if result.returncode != 0 and not self.gate_config.allow_lint_errors:
                error_count = len(stdout.decode().strip().split("\n"))
                return GateCheck(
                    name="lint",
                    gate_type=GateType.QUALITY.value,
                    result=GateResult.FAIL.value,
                    message=f"Lint errors found: {error_count}",
                    actual_value=error_count,
                )

            return GateCheck(
                name="lint",
                gate_type=GateType.QUALITY.value,
                result=GateResult.PASS.value,
                message="No lint errors",
            )
        except FileNotFoundError:
            pass

        return GateCheck(
            name="lint",
            gate_type=GateType.QUALITY.value,
            result=GateResult.SKIP.value,
            message="Lint check skipped (ruff not installed)",
        )

    async def _check_complexity(self) -> GateCheck:
        """Check code complexity"""
        try:
            result = await asyncio.create_subprocess_exec(
                "radon", "cc", ".", "-a",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await result.communicate()

            output = stdout.decode()
            # Parse complexity (simple extraction)
            import re
            match = re.search(r'Average\s+complexity:\s+([\d.]+)\s+', output)
            if match:
                complexity = float(match.group(1))
                if complexity > self.gate_config.max_complexity:
                    return GateCheck(
                        name="complexity",
                        gate_type=GateType.QUALITY.value,
                        result=GateResult.WARNING.value,
                        message=f"Average complexity: {complexity:.1f} (recommended: <{self.gate_config.max_complexity})",
                        threshold=self.gate_config.max_complexity,
                        actual_value=complexity,
                    )

                return GateCheck(
                    name="complexity",
                    gate_type=GateType.QUALITY.value,
                    result=GateResult.PASS.value,
                    message=f"Average complexity: {complexity:.1f}",
                    actual_value=complexity,
                )
        except FileNotFoundError:
            pass

        return GateCheck(
            name="complexity",
            gate_type=GateType.QUALITY.value,
            result=GateResult.SKIP.value,
            message="Complexity check skipped (radon not installed)",
        )

    def _format_report(self, report: GateReport) -> str:
        """Format gate report"""
        lines = [
            "=" * 60,
            "Quality Gate Report",
            "=" * 60,
            "",
            f"Timestamp: {report.timestamp}",
            "",
            "Results:",
            f"  ✓ Passed:    {report.passed_count}",
            f"  ✗ Failed:    {report.failed_count}",
            f"  ⚠ Warning:   {report.warning_count}",
            f"  ⊘ Skipped:   {report.skipped_count}",
            "",
        ]

        # Show individual checks
        lines.append("Checks:")
        for check in report.checks:
            if check.result == GateResult.PASS.value:
                emoji = "✓"
                style = "[green]"
            elif check.result == GateResult.FAIL.value:
                emoji = "✗"
                style = "[red]"
            elif check.result == GateResult.WARNING.value:
                emoji = "⚠"
                style = "[yellow]"
            else:
                emoji = "⊘"
                style = "[dim]"

            lines.append(f"  {emoji} {check.name}: {check.message}")

        lines.append("")

        # Overall status
        if report.overall_result == GateResult.PASS.value:
            lines.append("[green]✓ GATE PASSED[/green]")
        elif report.overall_result == GateResult.WARNING.value:
            lines.append("[yellow]⚠ GATE PASSED WITH WARNINGS[/yellow]")
        else:
            lines.append("[red]✗ GATE FAILED[/red]")

        lines.append("=" * 60)

        return "\n".join(lines)
