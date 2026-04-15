"""Test Audit Skill"""

import pytest
import asyncio
from pathlib import Path
from helix.skills.audit import (
    AuditSkill, AuditCategory, AuditSeverity,
    AuditFinding, AuditReport
)
from helix.core.intent import Intent, IntentType
from helix.core.context import HelixContext


class TestAuditCategory:
    """Test AuditCategory"""

    def test_category_values(self):
        """Test audit category values"""
        assert AuditCategory.SECURITY == "security"
        assert AuditCategory.DEPENDENCY == "dependency"
        assert AuditCategory.ARCHITECTURE == "architecture"
        assert AuditCategory.COMPLIANCE == "compliance"
        assert AuditCategory.PERFORMANCE == "performance"


class TestAuditSeverity:
    """Test AuditSeverity"""

    def test_severity_values(self):
        """Test severity values"""
        assert AuditSeverity.CRITICAL == "critical"
        assert AuditSeverity.HIGH == "high"
        assert AuditSeverity.MEDIUM == "medium"
        assert AuditSeverity.LOW == "low"
        assert AuditSeverity.INFO == "info"


class TestAuditFinding:
    """Test AuditFinding"""

    def test_finding_creation(self):
        """Test AuditFinding creation"""
        finding = AuditFinding(
            severity=AuditSeverity.CRITICAL,
            category=AuditCategory.SECURITY,
            title="Test finding",
            description="Test description",
            file_path="test.py",
            line_number=10,
            recommendation="Fix this",
            cwe_id="CWE-123",
            cve_id="CVE-2021-12345",
            evidence="code snippet"
        )
        assert finding.severity == AuditSeverity.CRITICAL
        assert finding.category == AuditCategory.SECURITY
        assert finding.title == "Test finding"
        assert finding.file_path == "test.py"
        assert finding.line_number == 10
        assert finding.cwe_id == "CWE-123"
        assert finding.cve_id == "CVE-2021-12345"

    def test_finding_defaults(self):
        """Test AuditFinding default values"""
        finding = AuditFinding(
            severity=AuditSeverity.INFO,
            category=AuditCategory.ARCHITECTURE,
            title="Test",
            description="Test"
        )
        assert finding.file_path == ""
        assert finding.line_number == 0
        assert finding.recommendation == ""
        assert finding.cwe_id == ""
        assert finding.cve_id == ""
        assert finding.evidence == ""


class TestAuditReport:
    """Test AuditReport"""

    def test_report_defaults(self):
        """Test AuditReport default values"""
        report = AuditReport()
        assert report.timestamp == ""
        assert report.files_scanned == 0
        assert report.vulnerabilities_found == 0
        assert report.findings == []
        assert report.critical_count == 0
        assert report.high_count == 0
        assert report.medium_count == 0
        assert report.low_count == 0
        assert report.info_count == 0
        assert report.security_count == 0
        assert report.dependency_count == 0
        assert report.architecture_count == 0
        assert report.compliance_count == 0

    def test_report_custom_values(self):
        """Test AuditReport with custom values"""
        finding = AuditFinding(
            severity=AuditSeverity.HIGH,
            category=AuditCategory.SECURITY,
            title="Test",
            description="Test"
        )
        report = AuditReport(
            timestamp="2024-01-01",
            files_scanned=100,
            findings=[finding]
        )
        assert report.timestamp == "2024-01-01"
        assert report.files_scanned == 100
        assert len(report.findings) == 1


class TestAuditSkill:
    """Test AuditSkill"""

    @pytest.fixture
    def skill(self):
        return AuditSkill()

    def test_skill_init(self, skill):
        """Test skill initialization"""
        assert skill.name == "audit"
        assert skill.category.value == "quality"
        assert skill.status.value == "experimental"

    def test_skill_examples(self, skill):
        """Test skill examples"""
        assert len(skill.examples) > 0
        assert "helix audit" in skill.examples

    def test_skill_scan_defaults(self, skill):
        """Test default scan settings"""
        assert skill.scan_security is True
        assert skill.scan_dependencies is True
        assert skill.scan_architecture is True
        assert skill.scan_compliance is False

    @pytest.mark.asyncio
    async def test_execute_with_params(self, skill):
        """Test execute with parameters"""
        intent = Intent(
            type=IntentType.AUDIT,
            raw_input="audit test",
            confidence=0.9,
            parameters={
                "security": True,
                "dependencies": False,
                "architecture": False,
                "compliance": False,
                "path": "tests"  # Scan tests dir to avoid self-scan issues
            }
        )
        result = await skill.execute(intent, None)
        assert result is not None
        assert "Audit" in result.message
        assert "files_scanned" in result.data["report"]

    @pytest.mark.asyncio
    async def test_execute_empty_path(self, skill):
        """Test execute with non-existent path"""
        intent = Intent(
            type=IntentType.AUDIT,
            raw_input="audit test",
            confidence=0.9,
            parameters={"path": "/nonexistent/path"}
        )
        result = await skill.execute(intent, None)
        # Should handle gracefully
        assert result is not None

    def test_format_report(self, skill):
        """Test report formatting"""
        report = AuditReport(
            timestamp="2024-01-01T00:00:00",
            files_scanned=10,
            critical_count=0,
            high_count=0,
            medium_count=0,
            low_count=0,
            info_count=0
        )
        formatted = skill._format_report(report)
        assert "Audit Report" in formatted
        assert "2024-01-01" in formatted
        assert "PASSED" in formatted

    def test_format_report_with_critical(self, skill):
        """Test report formatting with critical findings"""
        report = AuditReport(
            timestamp="2024-01-01T00:00:00",
            files_scanned=10,
            critical_count=1,
            high_count=0,
            medium_count=0,
            low_count=0,
            info_count=0,
            findings=[
                AuditFinding(
                    severity=AuditSeverity.CRITICAL,
                    category=AuditCategory.SECURITY,
                    title="Test critical",
                    description="Test"
                )
            ]
        )
        formatted = skill._format_report(report)
        assert "FAILED" in formatted

    def test_format_report_with_high(self, skill):
        """Test report formatting with high findings"""
        report = AuditReport(
            timestamp="2024-01-01T00:00:00",
            files_scanned=10,
            critical_count=0,
            high_count=1,
            medium_count=0,
            low_count=0,
            info_count=0,
            findings=[
                AuditFinding(
                    severity=AuditSeverity.HIGH,
                    category=AuditCategory.SECURITY,
                    title="Test high",
                    description="Test"
                )
            ]
        )
        formatted = skill._format_report(report)
        assert "WARNING" in formatted