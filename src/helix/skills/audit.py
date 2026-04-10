"""
Helix Audit Skill - Security and Architecture Audit

This skill performs comprehensive security and architecture audits:
- Dependency vulnerability scanning
- Security vulnerability detection
- Architecture quality assessment
- Compliance checking
"""

import asyncio
import subprocess
import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
import os

from helix.skills.base import (
    Skill, SkillResult, SkillConfig, SkillCategory, SkillStatus
)
from helix.core.intent import Intent, IntentType
from helix.core.context import HelixContext


# Audit categories
class AuditCategory:
    """Audit categories"""
    SECURITY = "security"
    DEPENDENCY = "dependency"
    ARCHITECTURE = "architecture"
    COMPLIANCE = "compliance"
    PERFORMANCE = "performance"


# Severity levels
class AuditSeverity:
    """Finding severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class AuditFinding:
    """Audit finding"""
    severity: str
    category: str
    title: str
    description: str
    file_path: str = ""
    line_number: int = 0
    recommendation: str = ""
    cwe_id: str = ""  # Common Weakness Enumeration
    cve_id: str = ""  # Common Vulnerabilities and Exposures
    evidence: str = ""


@dataclass
class AuditReport:
    """Audit report"""
    timestamp: str = ""
    files_scanned: int = 0
    vulnerabilities_found: int = 0
    findings: List[AuditFinding] = field(default_factory=list)

    # Summary counts
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    info_count: int = 0

    # Category counts
    security_count: int = 0
    dependency_count: int = 0
    architecture_count: int = 0
    compliance_count: int = 0


class AuditSkill(Skill):
    """
    Audit Skill - Security and Architecture Audit

    Performs comprehensive security and quality audits
    """

    name = "audit"
    description = "Security and architecture audit - vulnerability scanning, dependency check, compliance"
    category = SkillCategory.QUALITY
    status = SkillStatus.EXPERIMENTAL

    examples = [
        "helix audit",
        "helix audit --security",
        "helix audit --dependencies",
        "helix audit --full",
    ]

    def __init__(self, config: Optional[SkillConfig] = None):
        super().__init__(config)
        self.scan_security = True
        self.scan_dependencies = True
        self.scan_architecture = True
        self.scan_compliance = False

    def _do_initialize(self) -> None:
        """Initialize audit skill"""
        pass

    async def execute(self, intent: Intent, context: Optional[HelixContext]) -> SkillResult:
        """Execute audit skill"""
        start_time = asyncio.get_event_loop().time()

        # Parse parameters
        params = intent.parameters
        self.scan_security = params.get("security", True)
        self.scan_dependencies = params.get("dependencies", True)
        self.scan_architecture = params.get("architecture", True)
        self.scan_compliance = params.get("compliance", False)
        scan_path = params.get("path", ".")

        try:
            # Run audits
            report = await self._run_audit(scan_path)

            # Calculate execution time
            execution_time = int((asyncio.get_event_loop().time() - start_time) * 1000)

            # Prepare result
            result = SkillResult(
                success=report.critical_count == 0,
                message=self._format_report(report),
                data={
                    "report": {
                        "files_scanned": report.files_scanned,
                        "vulnerabilities_found": report.vulnerabilities_found,
                        "critical": report.critical_count,
                        "high": report.high_count,
                        "medium": report.medium_count,
                        "low": report.low_count,
                        "info": report.info_count,
                    },
                    "findings": [
                        {
                            "severity": f.severity,
                            "category": f.category,
                            "title": f.title,
                            "file": f.file_path,
                            "line": f.line_number,
                            "recommendation": f.recommendation,
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
                message=f"Audit failed: {str(e)}",
                errors=[str(e)]
            )

    async def _run_audit(self, scan_path: str) -> AuditReport:
        """Run complete audit"""
        report = AuditReport(timestamp=datetime.now().isoformat())

        # Count files
        path = Path(scan_path)
        if path.exists():
            report.files_scanned = len(list(path.rglob("*.py")))

        # Run security audit
        if self.scan_security:
            report.findings.extend(await self._audit_security(scan_path))

        # Run dependency audit
        if self.scan_dependencies:
            report.findings.extend(await self._audit_dependencies(scan_path))

        # Run architecture audit
        if self.scan_architecture:
            report.findings.extend(await self._audit_architecture(scan_path))

        # Run compliance audit
        if self.scan_compliance:
            report.findings.extend(await self._audit_compliance(scan_path))

        # Count findings by severity
        for f in report.findings:
            if f.severity == AuditSeverity.CRITICAL:
                report.critical_count += 1
            elif f.severity == AuditSeverity.HIGH:
                report.high_count += 1
            elif f.severity == AuditSeverity.MEDIUM:
                report.medium_count += 1
            elif f.severity == AuditSeverity.LOW:
                report.low_count += 1
            else:
                report.info_count += 1

            # Count by category
            if f.category == AuditCategory.SECURITY:
                report.security_count += 1
            elif f.category == AuditCategory.DEPENDENCY:
                report.dependency_count += 1
            elif f.category == AuditCategory.ARCHITECTURE:
                report.architecture_count += 1
            elif f.category == AuditCategory.COMPLIANCE:
                report.compliance_count += 1

        report.vulnerabilities_found = (
            report.critical_count + report.high_count + report.medium_count
        )

        return report

    async def _audit_security(self, scan_path: str) -> List[AuditFinding]:
        """Run security audit"""
        findings = []
        path = Path(scan_path)

        # Common vulnerability patterns
        vulnerable_patterns = [
            # Hardcoded secrets
            (r'password\s*=\s*["\'][^"\']{8,}["\']', "Hardcoded password",
             AuditSeverity.CRITICAL, "CWE-259"),
            (r'api[_-]?key\s*=\s*["\'][a-zA-Z0-9]{20,}["\']', "Hardcoded API key",
             AuditSeverity.CRITICAL, "CWE-798"),
            (r'secret\s*=\s*["\'][a-zA-Z0-9]{20,}["\']', "Hardcoded secret",
             AuditSeverity.CRITICAL, "CWE-798"),
            (r'token\s*=\s*["\'][a-zA-Z0-9]{20,}["\']', "Hardcoded token",
             AuditSeverity.CRITICAL, "CWE-798"),
            (r'private[_-]?key\s*=\s*["\']', "Private key in code",
             AuditSeverity.CRITICAL, "CWE-798"),

            # SQL Injection
            (r'execute\s*\(\s*["\'].*%s', "SQL injection risk (string formatting)",
             AuditSeverity.CRITICAL, "CWE-89"),
            (r'".*SELECT.*{', "SQL injection risk (f-string)",
             AuditSeverity.CRITICAL, "CWE-89"),

            # Command Injection
            (r'os\.system\s*\(', "Command injection (os.system)",
             AuditSeverity.CRITICAL, "CWE-78"),
            (r'subprocess.*shell\s*=\s*True', "Command injection (shell=True)",
             AuditSeverity.CRITICAL, "CWE-78"),
            (r'eval\s*\(', "Use of eval()",
             AuditSeverity.HIGH, "CWE-95"),
            (r'exec\s*\(', "Use of exec()",
             AuditSeverity.HIGH, "CWE-95"),

            # Path Traversal
            (r'open\s*\([^,)]*\+', "Path traversal risk",
             AuditSeverity.HIGH, "CWE-22"),
            (r'os\.path\.join\s*\([^,)]*\+', "Path traversal risk",
             AuditSeverity.HIGH, "CWE-22"),

            # Weak Cryptography
            (r'hashlib\.md5\s*\(', "Weak hashing (MD5)",
             AuditSeverity.MEDIUM, "CWE-327"),
            (r'hashlib\.sha1\s*\(', "Weak hashing (SHA1)",
             AuditSeverity.MEDIUM, "CWE-327"),
            (r'Crypto\.Cipher.*RC4', "Weak encryption (RC4)",
             AuditSeverity.MEDIUM, "CWE-327"),

            # Insecure Random
            (r'random\.random\s*\(', "Insecure random (random module)",
             AuditSeverity.LOW, "CWE-338"),

            # Unvalidated Redirect
            (r'redirect\s*\([^,)]*\+', "Unvalidated redirect",
             AuditSeverity.MEDIUM, "CWE-601"),

            # Disable SSL verification
            (r'verify\s*=\s*False', "SSL verification disabled",
             AuditSeverity.HIGH, "CWE-295"),
        ]

        # Scan Python files
        for py_file in path.rglob("*.py"):
            if "test" in str(py_file).lower():
                continue

            try:
                content = py_file.read_text()
                lines = content.split("\n")

                for line_num, line in enumerate(lines, 1):
                    # Skip comments
                    if line.strip().startswith("#"):
                        continue

                    for pattern, title, severity, cwe in vulnerable_patterns:
                        if re.search(pattern, line, re.IGNORECASE):
                            findings.append(AuditFinding(
                                severity=severity,
                                category=AuditCategory.SECURITY,
                                title=title,
                                description=f"Found potential {title.lower()} at line {line_num}",
                                file_path=str(py_file),
                                line_number=line_num,
                                recommendation=f"Use secure alternative or parameterized queries",
                                cwe_id=cwe,
                                evidence=line.strip()[:80],
                            ))

            except Exception:
                continue

        return findings

    async def _audit_dependencies(self, scan_path: str) -> List[AuditFinding]:
        """Run dependency audit"""
        findings = []
        path = Path(scan_path)

        # Check for requirements.txt or pyproject.toml
        requirements_file = path / "requirements.txt"
        pyproject_file = path / "pyproject.toml"

        if not requirements_file.exists() and not pyproject_file.exists():
            return findings

        # Try to run safety check
        try:
            result = await asyncio.create_subprocess_exec(
                "safety", "check", "--json",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(path),
            )
            stdout, _ = await result.communicate()

            if stdout:
                try:
                    vulnerabilities = json.loads(stdout.decode())
                    for vuln in vulnerabilities:
                        findings.append(AuditFinding(
                            severity=AuditSeverity.CRITICAL,
                            category=AuditCategory.DEPENDENCY,
                            title=f"Vulnerable dependency: {vuln.get('package', 'unknown')}",
                            description=vuln.get('description', 'Vulnerability found'),
                            recommendation=f"Upgrade to version: {vuln.get('fixed_in', 'latest')}",
                            cve_id=vuln.get('id', ''),
                        ))
                except json.JSONDecodeError:
                    pass
        except FileNotFoundError:
            # safety not installed, skip
            pass

        # Check for known vulnerable packages
        vulnerable_packages = {
            "requests": "<2.31.0",
            "urllib3": "<2.0.0",
            "flask": "<2.3.0",
            "django": "<4.2.0",
            "numpy": "<1.22.0",
            "pillow": "<10.0.0",
            "pyyaml": "<6.0.1",
            "jinja2": "<3.1.2",
            "werkzeug": "<2.3.0",
            "cryptography": "<41.0.0",
        }

        if requirements_file.exists():
            content = requirements_file.read_text()
            for line in content.split("\n"):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                # Parse package==version format
                match = re.match(r'^([a-zA-Z0-9_-]+)([<>=!]+.*)?$', line)
                if match:
                    pkg = match.group(1).lower()
                    version = match.group(2) or ""

                    if pkg in vulnerable_packages:
                        findings.append(AuditFinding(
                            severity=AuditSeverity.MEDIUM,
                            category=AuditCategory.DEPENDENCY,
                            title=f"Known vulnerable package: {pkg}",
                            description=f"Package {pkg} has known vulnerabilities in older versions",
                            recommendation=f"Use version {vulnerable_packages[pkg]} or later",
                            file_path=str(requirements_file),
                        ))

        return findings

    async def _audit_architecture(self, scan_path: str) -> List[AuditFinding]:
        """Run architecture audit"""
        findings = []
        path = Path(scan_path)

        # Check for common architectural issues
        issues = [
            # Circular imports (simple check)
            (r'from\s+\.', "Relative import detected", AuditSeverity.INFO, "A001"),
            (r'import\s+typing\s+as\s+t\b', "typing alias recommended", AuditSeverity.INFO, "A002"),
        ]

        # Check for missing error handling
        error_handling_patterns = [
            (r'except\s*:\s*$', "Bare except clause", AuditSeverity.MEDIUM, "A010"),
        ]

        # Check for missing type hints
        type_hint_patterns = [
            (r'def\s+\w+\s*\([^)]*\)\s*->\s*None', "Function returns None implicitly", AuditSeverity.LOW, "A020"),
        ]

        # Scan files
        for py_file in path.rglob("*.py"):
            if "test" in str(py_file).lower():
                continue

            try:
                content = py_file.read_text()
                lines = content.split("\n")

                for line_num, line in enumerate(lines, 1):
                    # Skip comments and strings
                    if line.strip().startswith("#") or '"' in line or "'" in line:
                        continue

                    for pattern, title, severity, code in error_handling_patterns:
                        if re.search(pattern, line):
                            findings.append(AuditFinding(
                                severity=severity,
                                category=AuditCategory.ARCHITECTURE,
                                title=title,
                                description=f"Found {title.lower()} at line {line_num}",
                                file_path=str(py_file),
                                line_number=line_num,
                                recommendation="Use specific exception types",
                            ))

            except Exception:
                continue

        # Check project structure
        required_dirs = ["src", "tests", "docs"]
        missing_dirs = [d for d in required_dirs if not (path / d).exists()]

        if missing_dirs:
            findings.append(AuditFinding(
                severity=AuditSeverity.INFO,
                category=AuditCategory.ARCHITECTURE,
                title="Missing recommended directories",
                description=f"Project is missing: {', '.join(missing_dirs)}",
                recommendation=f"Consider adding: {', '.join(missing_dirs)}",
            ))

        # Check for pyproject.toml
        if not (path / "pyproject.toml").exists():
            findings.append(AuditFinding(
                severity=AuditSeverity.INFO,
                category=AuditCategory.ARCHITECTURE,
                title="Missing pyproject.toml",
                description="Project should use pyproject.toml for modern Python packaging",
                recommendation="Create pyproject.toml for better dependency management",
            ))

        return findings

    async def _audit_compliance(self, scan_path: str) -> List[AuditFinding]:
        """Run compliance audit"""
        findings = []
        path = Path(scan_path)

        # Check for license file
        if not (path / "LICENSE").exists():
            findings.append(AuditFinding(
                severity=AuditSeverity.INFO,
                category=AuditCategory.COMPLIANCE,
                title="Missing LICENSE file",
                description="Project should include a LICENSE file",
                recommendation="Add an appropriate LICENSE file",
            ))

        # Check for README
        if not (path / "README.md").exists():
            findings.append(AuditFinding(
                severity=AuditSeverity.INFO,
                category=AuditCategory.COMPLIANCE,
                title="Missing README.md",
                description="Project should include a README file",
                recommendation="Add README.md with project documentation",
            ))

        # Check for .gitignore
        if not (path / ".gitignore").exists():
            findings.append(AuditFinding(
                severity=AuditSeverity.LOW,
                category=AuditCategory.COMPLIANCE,
                title="Missing .gitignore",
                description="Project should include a .gitignore file",
                recommendation="Add .gitignore for common ignored files",
            ))

        return findings

    def _format_report(self, report: AuditReport) -> str:
        """Format audit report"""
        lines = [
            "=" * 60,
            "Security & Architecture Audit Report",
            "=" * 60,
            "",
            f"Timestamp: {report.timestamp}",
            f"Files Scanned: {report.files_scanned}",
            "",
            "Summary:",
            f"  Critical: [red]{report.critical_count}[/red]",
            f"  High:     [red]{report.high_count}[/red]",
            f"  Medium:   [yellow]{report.medium_count}[/yellow]",
            f"  Low:      [blue]{report.low_count}[/blue]",
            f"  Info:     {report.info_count}",
            "",
            "By Category:",
            f"  Security:    {report.security_count}",
            f"  Dependencies:{report.dependency_count}",
            f"  Architecture:{report.architecture_count}",
            f"  Compliance:  {report.compliance_count}",
            "",
        ]

        # Show top findings
        if report.findings:
            critical_high = [f for f in report.findings
                           if f.severity in [AuditSeverity.CRITICAL, AuditSeverity.HIGH]]

            if critical_high:
                lines.append("Critical & High Findings:")
                for f in critical_high[:10]:
                    emoji = "🔴" if f.severity == AuditSeverity.CRITICAL else "🟠"
                    lines.append(f"  {emoji} [{f.severity.upper()}] {f.title}")
                    if f.file_path:
                        lines.append(f"     → {f.file_path}:{f.line_number}")
                lines.append("")

        # Status
        if report.critical_count > 0:
            lines.append("[red]⚠️  AUDIT FAILED - Critical issues found![/red]")
        elif report.high_count > 0:
            lines.append("[yellow]⚠️  AUDIT WARNING - High issues found[/yellow]")
        else:
            lines.append("[green]✓ AUDIT PASSED - No critical issues[/green]")

        lines.append("=" * 60)

        return "\n".join(lines)
