"""
/verify 技能 - 自动化验证

运行静态检查、单元测试、验收测试
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


# ============ 数据模型 ============

@dataclass
class CheckResult:
    """检查结果"""
    name: str
    status: str  # pass, fail, skip, error
    message: str = ""
    duration_ms: int = 0
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VerifyReport:
    """验证报告"""
    timestamp: str
    duration_seconds: float
    project_path: str

    # 各层级结果
    static: CheckResult
    test: CheckResult
    acceptance: CheckResult

    # 总体状态
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


# ============ 验证器 ============

class StaticChecker:
    """静态检查"""

    TOOLS = ["ruff", "black", "mypy"]

    def __init__(self, project_path: Path):
        self.project_path = project_path

    async def run(self) -> CheckResult:
        """运行静态检查"""
        start = datetime.now()
        issues = []
        passed = True

        # 检查 ruff 可用
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

        # 检查 mypy 可用
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
    """测试运行器"""

    def __init__(self, project_path: Path):
        self.project_path = project_path

    async def run(self) -> CheckResult:
        """运行测试"""
        start = datetime.now()
        issues = []
        passed = True
        test_details = {}

        # 检查 pytest 可用
        try:
            result = subprocess.run(
                ["pytest", "--tb=short", "-v", "--json-report", "--json-report-file=/tmp/pytest-report.json"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=120
            )

            # 解析输出
            output = result.stdout + result.stderr

            # 提取测试统计
            if "passed" in output:
                import re
                match = re.search(r'(\d+) passed', output)
                if match:
                    test_details["passed"] = int(match.group(1))

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
    """验收测试检查器"""

    def __init__(self, project_path: Path):
        self.project_path = project_path

    async def run(self) -> CheckResult:
        """检查验收标准"""
        start = datetime.now()
        issues = []

        # 查找 SPEC.md
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

        # 读取第一个 SPEC
        spec_content = spec_files[0].read_text()

        # 提取验收标准
        ac_items = []
        for line in spec_content.split('\n'):
            if '- [ ]' in line:
                ac_items.append(line.replace('- [ ]', '').strip())

        # 检查测试覆盖
        # 简化：检查是否有测试文件
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
                "ac_items": ac_items[:5]  # 前5个
            }
        )


# ============ VerifySkill ============

class VerifySkill(Skill):
    """自动化验证技能"""

    name = "verify"
    description = "运行静态检查、单元测试、验收测试"
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

        # 解析参数
        project_path = intent.parameters.get('path', '.')
        level = intent.parameters.get('level', 'full')  # static, test, acceptance, full

        project = Path(project_path)
        if not project.exists():
            return SkillResult(
                success=False,
                message=f"项目路径不存在: {project_path}",
                skill_name=self.name
            )

        # 运行各层级检查
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

        # 计算总体状态
        statuses = [r.status for r in results.values() if r.status != "skip"]
        if all(s == "pass" for s in statuses):
            overall = "pass"
        elif any(s == "fail" for s in statuses):
            overall = "fail"
        else:
            overall = "partial"

        execution_time = int((asyncio.get_event_loop().time() - start_time) * 1000)

        # 生成报告
        report = VerifyReport(
            timestamp=datetime.now().isoformat(),
            duration_seconds=execution_time / 1000,
            project_path=str(project),
            static=results.get("static", CheckResult("static", "skip")),
            test=results.get("test", CheckResult("test", "skip")),
            acceptance=results.get("acceptance", CheckResult("acceptance", "skip")),
            overall=overall
        )

        # 输出人类可读报告
        report_text = self._format_report(report)

        return SkillResult(
            success=overall != "fail",
            message=report_text,
            data=report.to_dict(),
            skill_name=self.name,
            execution_time_ms=execution_time,
        )

    def _format_report(self, report: VerifyReport) -> str:
        """格式化报告为人类可读"""
        lines = [
            "╭───────────────────────── 验证报告 ──────────────────────────╮",
            f"│ 项目: {report.project_path}",
            f"│ 耗时: {report.duration_seconds:.2f}s",
            "├──────────────────────────────────────────────────────────────┤",
        ]

        # 静态检查
        static = report.static
        status_icon = "✓" if static.status == "pass" else "✗" if static.status == "fail" else "-"
        lines.append(f"│ 静态检查    {status_icon} {static.status.upper()} ({static.duration_ms}ms)")

        # 测试
        test = report.test
        status_icon = "✓" if test.status == "pass" else "✗" if test.status == "fail" else "-"
        cov = test.details.get("coverage", "N/A")
        lines.append(f"│ 单元测试    {status_icon} {test.status.upper()} (覆盖率: {cov})")

        # 验收
        acc = report.acceptance
        status_icon = "✓" if acc.status == "pass" else "⚠" if acc.status == "partial" else "-"
        lines.append(f"│ 验收测试    {status_icon} {acc.status.upper()}")

        # 总体
        overall_icon = "✓" if report.overall == "pass" else "⚠" if report.overall == "partial" else "✗"
        lines.append("├──────────────────────────────────────────────────────────────┤")
        lines.append(f"│ 总体状态: {overall_icon} {report.overall.upper()}")
        lines.append("╰──────────────────────────────────────────────────────────────╯")

        return "\n".join(lines)
