"""Test Gate Skill"""

import pytest
from helix.skills.gate import (
    GateSkill, GateResult, GateType, GateCheck, GateConfig, GateReport
)


class TestGateResult:
    """Test GateResult"""

    def test_gate_result_values(self):
        """Test gate result values"""
        assert GateResult.PASS.value == "pass"
        assert GateResult.FAIL.value == "fail"
        assert GateResult.WARNING.value == "warning"
        assert GateResult.SKIP.value == "skip"


class TestGateType:
    """Test GateType"""

    def test_gate_type_values(self):
        """Test gate type values"""
        assert GateType.SECURITY.value == "security"
        assert GateType.QUALITY.value == "quality"
        assert GateType.TEST.value == "test"
        assert GateType.PERFORMANCE.value == "performance"
        assert GateType.COMPLIANCE.value == "compliance"


class TestGateCheck:
    """Test GateCheck"""

    def test_gate_check_creation(self):
        """Test GateCheck creation"""
        check = GateCheck(
            name="test_check",
            gate_type="security",
            result="pass",
            message="Check passed",
            details="Details here",
            threshold=0,
            actual_value=0
        )
        assert check.name == "test_check"
        assert check.gate_type == "security"
        assert check.result == "pass"

    def test_gate_check_defaults(self):
        """Test GateCheck defaults"""
        check = GateCheck(
            name="test",
            gate_type="quality",
            result="pass",
            message="OK"
        )
        assert check.details == ""
        assert check.threshold is None
        assert check.actual_value is None


class TestGateConfig:
    """Test GateConfig"""

    def test_config_defaults(self):
        """Test GateConfig defaults"""
        config = GateConfig()
        assert config.require_security_scan is True
        assert config.max_critical_vulns == 0
        assert config.max_high_vulns == 0
        assert config.min_coverage == 70.0
        assert config.min_test_count == 10
        assert config.max_complexity == 10
        assert config.allow_lint_errors is False
        assert config.fail_on_warning is False
        assert config.allow_bypass is False
        assert config.bypass_reason == ""

    def test_config_custom(self):
        """Test GateConfig with custom values"""
        config = GateConfig(
            require_security_scan=False,
            max_critical_vulns=5,
            min_coverage=50.0,
            allow_bypass=True,
            bypass_reason="Emergency"
        )
        assert config.require_security_scan is False
        assert config.max_critical_vulns == 5
        assert config.min_coverage == 50.0
        assert config.allow_bypass is True
        assert config.bypass_reason == "Emergency"


class TestGateReport:
    """Test GateReport"""

    def test_report_defaults(self):
        """Test GateReport defaults"""
        report = GateReport()
        assert report.timestamp == ""
        assert report.overall_result == "pass"
        assert report.checks == []
        assert report.passed_count == 0
        assert report.failed_count == 0
        assert report.warning_count == 0
        assert report.skipped_count == 0

    def test_report_with_checks(self):
        """Test GateReport with checks"""
        check = GateCheck(
            name="test",
            gate_type="quality",
            result="pass",
            message="OK"
        )
        report = GateReport(
            timestamp="2024-01-01",
            overall_result="fail",
            checks=[check],
            passed_count=1,
            failed_count=0
        )
        assert len(report.checks) == 1
        assert report.overall_result == "fail"


class TestGateSkill:
    """Test GateSkill"""

    @pytest.fixture
    def skill(self):
        return GateSkill()

    def test_skill_init(self, skill):
        """Test skill initialization"""
        assert skill.name == "gate"
        assert skill.category.value == "quality"

    def test_skill_examples(self, skill):
        """Test skill examples"""
        assert len(skill.examples) > 0
        assert "helix gate" in skill.examples

    def test_skill_default_config(self, skill):
        """Test skill default config"""
        assert skill.config is not None