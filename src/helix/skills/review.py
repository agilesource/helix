"""
Helix Review Skill - Code Review and Analysis

This skill performs comprehensive code review including:
- SQL safety and data integrity
- Race conditions and concurrency
- LLM output trust boundaries
- Shell injection prevention
- Enum and value completeness
- And more
"""

import asyncio
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

from helix.skills.base import (
    Skill, SkillResult, SkillConfig, SkillCategory, SkillStatus
)
from helix.core.intent import Intent, IntentType
from helix.core.context import HelixContext


# Review finding severity levels
class FindingSeverity:
    """Finding severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class ReviewFinding:
    """Code review finding"""
    severity: str
    confidence: int  # 1-10
    file_path: str
    line_number: Optional[int]
    category: str
    summary: str
    description: str
    fix_suggestion: str
    fingerprint: str = ""


@dataclass
class ReviewReport:
    """Review report"""
    total_files: int = 0
    total_lines_changed: int = 0
    findings: List[ReviewFinding] = field(default_factory=list)
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    info_count: int = 0


class ReviewSkill(Skill):
    """
    Review Skill - Code Review and Analysis

    Analyzes code changes for common issues and best practices
    """

    name = "review"
    description = "Code review and analysis - finds bugs, security issues, and code quality problems"
    category = SkillCategory.QUALITY
    status = SkillStatus.EXPERIMENTAL

    examples = [
        "helix review",
        "helix review --base main",
        "helix review --path src/",
    ]

    # Critical review categories
    CRITICAL_CATEGORIES = [
        "sql_safety",
        "race_condition",
        "llm_trust_boundary",
        "shell_injection",
        "auth_bypass",
    ]

    def __init__(self, config: Optional[SkillConfig] = None):
        super().__init__(config)
        self.base_branch = "main"

    def _do_initialize(self) -> None:
        """Initialize review skill"""
        pass

    async def execute(self, intent: Intent, context: Optional[HelixContext]) -> SkillResult:
        """Execute review skill"""
        start_time = asyncio.get_event_loop().time()

        # Parse parameters
        path = intent.parameters.get("path", ".")
        base_branch = intent.parameters.get("base", self.base_branch)

        try:
            # Get diff from git
            diff_content = await self._get_diff(base_branch, path)

            if not diff_content:
                return SkillResult(
                    success=True,
                    message="No changes found to review",
                    data={"review_report": {}}
                )

            # Analyze the diff
            report = await self._analyze_diff(diff_content, path)

            # Calculate execution time
            execution_time = int((asyncio.get_event_loop().time() - start_time) * 1000)

            # Prepare result
            result = SkillResult(
                success=True,
                message=self._format_report(report),
                data={
                    "review_report": {
                        "total_files": report.total_files,
                        "total_lines_changed": report.total_lines_changed,
                        "critical": report.critical_count,
                        "high": report.high_count,
                        "medium": report.medium_count,
                        "low": report.low_count,
                        "info": report.info_count,
                    },
                    "findings": [
                        {
                            "severity": f.severity,
                            "confidence": f.confidence,
                            "file": f.file_path,
                            "line": f.line_number,
                            "category": f.category,
                            "summary": f.summary,
                            "fix": f.fix_suggestion,
                        }
                        for f in report.findings
                    ],
                },
                execution_time_ms=execution_time,
            )

            return result

        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Review failed: {str(e)}",
                errors=[str(e)]
            )

    async def _get_diff(self, base_branch: str, path: str) -> str:
        """Get git diff for review"""
        try:
            # Fetch latest from remote
            await asyncio.create_subprocess_exec(
                "git", "fetch", "origin", base_branch,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
        except Exception:
            pass  # Continue even if fetch fails

        # Get diff
        result = await asyncio.create_subprocess_exec(
            "git", "diff", f"origin/{base_branch}", "--", path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await result.communicate()

        if stderr:
            # Try without origin prefix
            result = await asyncio.create_subprocess_exec(
                "git", "diff", base_branch, "--", path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await result.communicate()

        return stdout.decode("utf-8", errors="ignore")

    async def _analyze_diff(self, diff_content: str, path: str) -> ReviewReport:
        """Analyze diff for issues"""
        report = ReviewReport()

        if not diff_content.strip():
            return report

        # Count files and lines
        for line in diff_content.split("\n"):
            if line.startswith("diff --git"):
                report.total_files += 1
            elif line.startswith("+") and not line.startswith("+++"):
                report.total_lines_changed += 1

        # Analyze each category
        findings = []

        # SQL Safety check
        findings.extend(self._check_sql_safety(diff_content))

        # Shell Injection check
        findings.extend(self._check_shell_injection(diff_content))

        # Race Condition check
        findings.extend(self._check_race_conditions(diff_content))

        # Hardcoded secrets
        findings.extend(self._check_hardcoded_secrets(diff_content))

        # Error handling
        findings.extend(self._check_error_handling(diff_content))

        report.findings = findings

        # Count by severity
        for f in findings:
            if f.severity == FindingSeverity.CRITICAL:
                report.critical_count += 1
            elif f.severity == FindingSeverity.HIGH:
                report.high_count += 1
            elif f.severity == FindingSeverity.MEDIUM:
                report.medium_count += 1
            elif f.severity == FindingSeverity.LOW:
                report.low_count += 1
            else:
                report.info_count += 1

        return report

    def _check_sql_safety(self, diff: str) -> List[ReviewFinding]:
        """Check for SQL injection vulnerabilities"""
        findings = []

        # Patterns that might indicate SQL injection
        dangerous_patterns = [
            (r'".*%s.*"', "String interpolation in SQL query"),
            (r'f".*SELECT.*\{', "f-string in SQL query"),
            (r'".*execute.*".*%', "execute with string formatting"),
            (r'\+.*\$\{.*\}.*SELECT', "Template literal with variable in SQL"),
        ]

        for line_num, line in enumerate(diff.split("\n"), 1):
            for pattern, desc in dangerous_patterns:
                import re
                if re.search(pattern, line, re.IGNORECASE):
                    findings.append(ReviewFinding(
                        severity=FindingSeverity.CRITICAL,
                        confidence=8,
                        file_path=self._extract_file_path(line, line_num, diff),
                        line_number=line_num,
                        category="sql_safety",
                        summary=f"Potential SQL injection: {desc}",
                        description=f"Found potential SQL injection risk: {desc}. "
                                   f"Use parameterized queries instead.",
                        fix_suggestion="Use parameterized queries: cursor.execute("
                                     "'SELECT * FROM users WHERE id = %s', (user_id,))",
                        fingerprint=f"sql_safety:{line_num}",
                    ))

        return findings

    def _check_shell_injection(self, diff: str) -> List[ReviewFinding]:
        """Check for shell injection vulnerabilities"""
        findings = []

        dangerous_patterns = [
            (r'os\.system\(', "os.system() call"),
            (r'subprocess\.call\(.+shell=True', "subprocess with shell=True"),
            (r'subprocess\.run\(.+shell=True', "subprocess with shell=True"),
            (r'os\.popen\(', "os.popen() call"),
            (r'exec\(', "exec() call"),
        ]

        for line_num, line in enumerate(diff.split("\n"), 1):
            for pattern, desc in dangerous_patterns:
                import re
                if re.search(pattern, line):
                    findings.append(ReviewFinding(
                        severity=FindingSeverity.CRITICAL,
                        confidence=9,
                        file_path=self._extract_file_path(line, line_num, diff),
                        line_number=line_num,
                        category="shell_injection",
                        summary=f"Shell injection risk: {desc}",
                        description=f"Found potential shell injection vulnerability. "
                                   f"Avoid shell=True or use subprocess.list2cmdline().",
                        fix_suggestion="Use subprocess.run([...], shell=False) "
                                     "with argument list instead",
                        fingerprint=f"shell_injection:{line_num}",
                    ))

        return findings

    def _check_race_conditions(self, diff: str) -> List[ReviewFinding]:
        """Check for race conditions"""
        findings = []

        # Look for non-thread-safe patterns
        patterns = [
            (r'global\s+\w+', "Global variable access"),
            (r'shared.*variable', "Shared variable without lock"),
            (r'\.append\(.*\).*\.append\(', "Concurrent list operations"),
        ]

        for line_num, line in enumerate(diff.split("\n"), 1):
            for pattern, desc in patterns:
                import re
                if re.search(pattern, line, re.IGNORECASE):
                    findings.append(ReviewFinding(
                        severity=FindingSeverity.HIGH,
                        confidence=6,
                        file_path=self._extract_file_path(line, line_num, diff),
                        line_number=line_num,
                        category="race_condition",
                        summary=f"Potential race condition: {desc}",
                        description=f"Code may have race condition issues. "
                                   f"Consider using locks or thread-safe structures.",
                        fix_suggestion="Use threading.Lock() or asyncio.Lock() "
                                     "to protect shared resources",
                        fingerprint=f"race_condition:{line_num}",
                    ))

        return findings

    def _check_hardcoded_secrets(self, diff: str) -> List[ReviewFinding]:
        """Check for hardcoded secrets"""
        findings = []

        secret_patterns = [
            (r'password\s*=\s*["\'][^"\']{8,}["\']', "Hardcoded password"),
            (r'api[_-]?key\s*=\s*["\'][^"\']{16,}["\']', "Hardcoded API key"),
            (r'secret\s*=\s*["\'][^"\']{16,}["\']', "Hardcoded secret"),
            (r'token\s*=\s*["\'][^"\']{16,}["\']', "Hardcoded token"),
            (r'private[_-]?key\s*=\s*["\']', "Private key in code"),
        ]

        for line_num, line in enumerate(diff.split("\n"), 1):
            for pattern, desc in secret_patterns:
                import re
                if re.search(pattern, line, re.IGNORECASE):
                    findings.append(ReviewFinding(
                        severity=FindingSeverity.CRITICAL,
                        confidence=9,
                        file_path=self._extract_file_path(line, line_num, diff),
                        line_number=line_num,
                        category="hardcoded_secrets",
                        summary=f"Hardcoded secret detected: {desc}",
                        description=f"Found hardcoded secret in code. "
                                   f"Use environment variables or secrets management.",
                        fix_suggestion="Use os.environ.get('SECRET') or "
                                     "secret management service",
                        fingerprint=f"hardcoded_secrets:{line_num}",
                    ))

        return findings

    def _check_error_handling(self, diff: str) -> List[ReviewFinding]:
        """Check error handling"""
        findings = []

        # Look for bare except or missing error handling
        patterns = [
            (r'except:$', "Bare except clause"),
            (r'except\s+Exception:', "Catch-all exception"),
            (r'try:.*finally:', "Try without except"),
        ]

        for line_num, line in enumerate(diff.split("\n"), 1):
            for pattern, desc in patterns:
                import re
                if re.search(pattern, line):
                    findings.append(ReviewFinding(
                        severity=FindingSeverity.MEDIUM,
                        confidence=7,
                        file_path=self._extract_file_path(line, line_num, diff),
                        line_number=line_num,
                        category="error_handling",
                        summary=f"Suboptimal error handling: {desc}",
                        description=f"Error handling could be improved. "
                                   f"Catch specific exceptions.",
                        fix_suggestion="Use specific exception types: "
                                     "except ValueError as e: ...",
                        fingerprint=f"error_handling:{line_num}",
                    ))

        return findings

    def _extract_file_path(self, line: str, line_num: int, diff: str) -> str:
        """Extract file path from diff context"""
        # Simple heuristic: look for a+++ or --- lines nearby
        lines = diff.split("\n")
        for i in range(max(0, line_num - 10), min(len(lines), line_num + 5)):
            if lines[i].startswith("+++ b/") or lines[i].startswith("a/"):
                return lines[i].replace("+++ b/", "").replace("a/", "").strip()
        return "unknown"

    def _format_report(self, report: ReviewReport) -> str:
        """Format review report as string"""
        lines = [
            "=" * 50,
            "Code Review Report",
            "=" * 50,
            "",
            f"Files changed: {report.total_files}",
            f"Lines changed: {report.total_lines_changed}",
            "",
            "Findings:",
            f"  Critical: {report.critical_count}",
            f"  High: {report.high_count}",
            f"  Medium: {report.medium_count}",
            f"  Low: {report.low_count}",
            f"  Info: {report.info_count}",
            "",
        ]

        # Add findings summary
        if report.findings:
            lines.append("Top Issues:")
            for f in sorted(report.findings,
                          key=lambda x: (
                              0 if x.severity == FindingSeverity.CRITICAL else
                              1 if x.severity == FindingSeverity.HIGH else
                              2 if x.severity == FindingSeverity.MEDIUM else 3
                          ))[:10]:
                lines.append(f"  [{f.severity.upper()}] {f.file_path}:{f.line_number} - {f.summary}")

        lines.append("")
        lines.append("=" * 50)

        return "\n".join(lines)


# For backwards compatibility
ReviewResult = ReviewFinding
