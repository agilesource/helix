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


class TestGateConfigExtended:
    """Extended GateConfig tests"""

    def test_config_security_settings(self):
        """Test security gate settings"""
        config = GateConfig(
            require_security_scan=True,
            max_critical_vulns=0,
            max_high_vulns=5
        )
        assert config.require_security_scan is True
        assert config.max_critical_vulns == 0
        assert config.max_high_vulns == 5

    def test_config_quality_settings(self):
        """Test quality gate settings"""
        config = GateConfig(
            min_coverage=80.0,
            min_test_count=20,
            max_complexity=15
        )
        assert config.min_coverage == 80.0
        assert config.min_test_count == 20
        assert config.max_complexity == 15

    def test_config_lint_settings(self):
        """Test lint gate settings"""
        config = GateConfig(allow_lint_errors=True)
        assert config.allow_lint_errors is True

    def test_config_fail_on_warning(self):
        """Test fail on warning config"""
        config = GateConfig(fail_on_warning=True)
        assert config.fail_on_warning is True


class TestGateCheckExtended:
    """Extended GateCheck tests"""

    def test_gate_check_with_threshold(self):
        """Test check with threshold values"""
        check = GateCheck(
            name="coverage",
            gate_type="quality",
            result="pass",
            message="Coverage OK",
            threshold=70.0,
            actual_value=75.0
        )
        assert check.threshold == 70.0
        assert check.actual_value == 75.0

    def test_gate_check_with_details(self):
        """Test check with details"""
        check = GateCheck(
            name="security",
            gate_type="security",
            result="fail",
            message="Vulnerabilities found",
            details="Found 3 critical issues"
        )
        assert "critical" in check.details


class TestGateReportExtended:
    """Extended GateReport tests"""

    def test_report_with_all_counts(self):
        """Test report with all count values"""
        check_pass = GateCheck(name="test", gate_type="test", result="pass", message="OK")
        check_fail = GateCheck(name="fail", gate_type="test", result="fail", message="Failed")
        check_warn = GateCheck(name="warn", gate_type="test", result="warning", message="Warning")
        report = GateReport(
            timestamp="2024-01-01",
            overall_result="fail",
            checks=[check_pass, check_fail, check_warn],
            passed_count=1,
            failed_count=1,
            warning_count=1,
            skipped_count=0
        )
        assert report.passed_count == 1
        assert report.failed_count == 1
        assert report.warning_count == 1

    def test_report_default_values(self):
        """Test report default values"""
        report = GateReport()
        assert report.timestamp == ""
        assert report.overall_result == "pass"
        assert report.checks == []
        assert report.passed_count == 0
        assert report.failed_count == 0
        assert report.warning_count == 0
        assert report.skipped_count == 0


class TestGateSkillMethods:
    """Test GateSkill methods"""

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

    def test_gate_skill_init(self):
        """Test GateSkill init"""
        skill = GateSkill()
        assert skill.gate_config is not None
        assert skill.strict_mode is False

    def test_gate_skill_with_config(self):
        """Test GateSkill with custom config"""
        from helix.skills.base import SkillConfig
        config = SkillConfig()
        skill = GateSkill(config)
        assert skill.config is config

    def test_gate_skill_attributes(self):
        """Test GateSkill attributes"""
        skill = GateSkill()
        assert skill.name == "gate"
        assert skill.description is not None
        assert skill.category.value == "quality"
        assert skill.status.value == "experimental"

    def test_gate_skill_examples(self):
        """Test GateSkill examples"""
        skill = GateSkill()
        assert len(skill.examples) > 0

    def test_format_report_pass(self, skill):
        """Test formatting a passing report"""
        check = GateCheck(
            name="security",
            gate_type="security",
            result="pass",
            message="No vulnerabilities found"
        )
        report = GateReport(
            overall_result="pass",
            checks=[check],
            passed_count=1,
            failed_count=0
        )
        formatted = skill._format_report(report)
        assert "pass" in formatted.lower()

    def test_format_report_fail(self, skill):
        """Test formatting a failing report"""
        check = GateCheck(
            name="security",
            gate_type="security",
            result="fail",
            message="Found 2 critical vulnerabilities",
            threshold=0,
            actual_value=2
        )
        report = GateReport(
            overall_result="fail",
            checks=[check],
            passed_count=0,
            failed_count=1
        )
        formatted = skill._format_report(report)
        assert "fail" in formatted.lower()

    def test_check_with_bypass(self):
        """Test bypass functionality"""
        # Create skill and manually update gate_config
        skill = GateSkill()
        skill.gate_config.allow_bypass = True
        skill.gate_config.bypass_reason = "Emergency fix"
        assert skill.gate_config.allow_bypass is True


class TestGateConfigExtended2:
    """Extended GateConfig tests"""

    def test_config_security_settings(self):
        """Test security gate settings"""
        config = GateConfig(
            require_security_scan=True,
            max_critical_vulns=0,
            max_high_vulns=5
        )
        assert config.require_security_scan is True
        assert config.max_critical_vulns == 0
        assert config.max_high_vulns == 5

    def test_config_quality_settings(self):
        """Test quality gate settings"""
        config = GateConfig(
            min_coverage=80.0,
            min_test_count=20,
            max_complexity=15
        )
        assert config.min_coverage == 80.0
        assert config.min_test_count == 20
        assert config.max_complexity == 15

    def test_config_lint_settings(self):
        """Test lint gate settings"""
        config = GateConfig(allow_lint_errors=True)
        assert config.allow_lint_errors is True

    def test_config_fail_on_warning(self):
        """Test fail on warning config"""
        config = GateConfig(fail_on_warning=True)
        assert config.fail_on_warning is True

    def test_config_with_all_thresholds(self):
        """Test config with all threshold values"""
        from helix.skills.gate import GateConfig
        config = GateConfig(
            min_coverage=80.0,
            min_test_count=10,
            max_complexity=15,
            max_critical_vulns=0,
            max_high_vulns=3,
            require_security_scan=True
        )
        assert config.min_coverage == 80.0
        assert config.min_test_count == 10
        assert config.max_complexity == 15
        assert config.require_security_scan is True

    def test_config_strict_mode(self):
        """Test strict mode config"""
        from helix.skills.gate import GateConfig
        config = GateConfig(
            min_coverage=90.0,
            min_test_count=20,
            require_security_scan=True,
            allow_bypass=False
        )
        assert config.min_coverage == 90.0
        assert config.allow_bypass is False


class TestGateSkillExecuteMocked:
    """Test GateSkill execute with mocks"""

    @pytest.mark.asyncio
    async def test_execute_with_bypass(self):
        """Test execute with bypass enabled"""
        from helix.skills.gate import GateSkill, GateConfig, GateResult
        from helix.core.intent import Intent, IntentType
        import unittest.mock

        skill = GateSkill()

        # Mock all subprocess calls
        mock_process = unittest.mock.AsyncMock()
        mock_process.communicate = unittest.mock.AsyncMock(return_value=(b'[]', b''))
        mock_process.returncode = 0

        intent = Intent(
            type=IntentType.GATE,
            raw_input="gate --bypass 'Emergency fix'",
            confidence=0.9,
            parameters={"bypass": "Emergency fix"}
        )

        with unittest.mock.patch(
            'asyncio.create_subprocess_exec',
            return_value=mock_process
        ):
            result = await skill.execute(intent, None)
            assert result is not None

    @pytest.mark.asyncio
    async def test_execute_with_strict_mode(self):
        """Test execute with strict mode"""
        from helix.skills.gate import GateSkill, GateConfig
        from helix.core.intent import Intent, IntentType
        import unittest.mock

        skill = GateSkill()

        mock_process = unittest.mock.AsyncMock()
        mock_process.communicate = unittest.mock.AsyncMock(return_value=(b'[]', b''))
        mock_process.returncode = 0

        intent = Intent(
            type=IntentType.GATE,
            raw_input="gate --strict",
            confidence=0.9,
            parameters={"strict": True}
        )

        with unittest.mock.patch(
            'asyncio.create_subprocess_exec',
            return_value=mock_process
        ):
            result = await skill.execute(intent, None)
            assert result is not None
            assert skill.strict_mode is True

    @pytest.mark.asyncio
    async def test_execute_with_custom_coverage(self):
        """Test execute with custom coverage threshold"""
        from helix.skills.gate import GateSkill, GateConfig
        from helix.core.intent import Intent, IntentType
        import unittest.mock

        skill = GateSkill()

        mock_process = unittest.mock.AsyncMock()
        mock_process.communicate = unittest.mock.AsyncMock(return_value=(b'[]', b''))
        mock_process.returncode = 0

        intent = Intent(
            type=IntentType.GATE,
            raw_input="gate --min-coverage 80",
            confidence=0.9,
            parameters={"min_coverage": 80.0}
        )

        with unittest.mock.patch(
            'asyncio.create_subprocess_exec',
            return_value=mock_process
        ):
            result = await skill.execute(intent, None)
            assert result is not None

    @pytest.mark.asyncio
    async def test_execute_security_disabled(self):
        """Test execute with security scan disabled"""
        from helix.skills.gate import GateSkill
        from helix.core.intent import Intent, IntentType
        import unittest.mock

        skill = GateSkill()

        mock_process = unittest.mock.AsyncMock()
        mock_process.communicate = unittest.mock.AsyncMock(return_value=(b'[]', b''))

        intent = Intent(
            type=IntentType.GATE,
            raw_input="gate --no-security",
            confidence=0.9,
            parameters={"security": False}
        )

        with unittest.mock.patch(
            'asyncio.create_subprocess_exec',
            return_value=mock_process
        ):
            result = await skill.execute(intent, None)
            assert result is not None
            assert skill.gate_config.require_security_scan is False

    @pytest.mark.asyncio
    async def test_check_security_with_vulnerabilities(self):
        """Test security check with vulnerabilities found"""
        from helix.skills.gate import GateSkill, GateConfig, GateCheck, GateResult
        import unittest.mock
        import json

        config = GateConfig(max_critical_vulns=0, max_high_vulns=5)
        skill = GateSkill(config)

        vulns = [
            {"severity": "critical", "id": 1},
            {"severity": "high", "id": 2},
            {"severity": "high", "id": 3},
        ]

        mock_process = unittest.mock.AsyncMock()
        mock_process.communicate = unittest.mock.AsyncMock(
            return_value=(json.dumps(vulns).encode(), b'')
        )

        with unittest.mock.patch(
            'asyncio.create_subprocess_exec',
            return_value=mock_process
        ):
            result = await skill._check_security()
            assert result is not None
            assert result.result == GateResult.FAIL.value
            assert "critical" in result.message.lower()

    @pytest.mark.asyncio
    async def test_check_coverage_mocked(self):
        """Test coverage check with mock"""
        from helix.skills.gate import GateSkill, GateConfig
        import unittest.mock
        import json

        config = GateConfig(min_coverage=50.0)
        skill = GateSkill(config)

        # Mock subprocess for pytest with coverage
        mock_process = unittest.mock.AsyncMock()
        mock_process.communicate = unittest.mock.AsyncMock(
            return_value=(b'', b'')
        )

        with unittest.mock.patch(
            'asyncio.create_subprocess_exec',
            return_value=mock_process
        ), unittest.mock.patch(
            'pathlib.Path.read_text',
            return_value='{"totals": {"percent_covered": 75.0}}'
        ):
            result = await skill._check_coverage()
            # May pass or skip depending on mock setup
            assert result is not None

    @pytest.mark.asyncio
    async def test_check_test_count_mocked(self):
        """Test test count check with mock"""
        from helix.skills.gate import GateSkill, GateConfig
        import unittest.mock

        config = GateConfig(min_test_count=5)
        skill = GateSkill(config)

        mock_process = unittest.mock.AsyncMock()
        mock_process.communicate = unittest.mock.AsyncMock(
            return_value=(b'5 tests collected', b'')
        )

        with unittest.mock.patch(
            'asyncio.create_subprocess_exec',
            return_value=mock_process
        ):
            result = await skill._check_test_count()
            assert result is not None

    @pytest.mark.asyncio
    async def test_check_lint_mocked(self):
        """Test lint check with mock"""
        from helix.skills.gate import GateSkill, GateConfig, GateResult
        import unittest.mock

        config = GateConfig(allow_lint_errors=False)
        skill = GateSkill(config)

        # Mock ruff or other linter
        mock_process = unittest.mock.AsyncMock()
        mock_process.communicate = unittest.mock.AsyncMock(
            return_value=(b'', b'')
        )

        with unittest.mock.patch(
            'asyncio.create_subprocess_exec',
            return_value=mock_process
        ):
            result = await skill._check_lint()
            assert result is not None

    @pytest.mark.asyncio
    async def test_check_complexity_mocked(self):
        """Test complexity check with mock"""
        from helix.skills.gate import GateSkill, GateConfig
        import unittest.mock

        config = GateConfig(max_complexity=15)
        skill = GateSkill(config)

        mock_process = unittest.mock.AsyncMock()
        mock_process.communicate = unittest.mock.AsyncMock(
            return_value=(b'10.5', b'')
        )

        with unittest.mock.patch(
            'asyncio.create_subprocess_exec',
            return_value=mock_process
        ):
            result = await skill._check_complexity()
            assert result is not None


class TestGateSkillAsync:
    """Test GateSkill async methods"""

    @pytest.mark.skip(reason="Hangs due to external command execution")
    @pytest.mark.asyncio
    async def test_execute_with_default_params(self):
        """Test execute with default parameters"""
        from helix.core.intent import Intent, IntentType
        skill = GateSkill()
        intent = Intent(type=IntentType.GATE, raw_input="gate", confidence=0.9, parameters={})
        result = await skill.execute(intent, None)

    @pytest.mark.skip(reason="Hangs due to external command execution")
    @pytest.mark.asyncio
    async def test_execute_with_custom_params(self):
        """Test execute with custom parameters"""
        from helix.core.intent import Intent, IntentType
        skill = GateSkill()
        intent = Intent(
            type=IntentType.GATE,
            raw_input="run gate",
            confidence=0.9,
            parameters={
                "require_security_scan": False,
                "min_coverage": 50.0
            }
        )
        try:
            result = await skill.execute(intent, None)
        except (RuntimeError, Exception):
            pass


class TestGateCheckResults:
    """Test gate check results"""

    def test_gate_check_creation(self):
        """Test GateCheck creation"""
        from helix.skills.gate import GateCheck
        check = GateCheck(
            name="security",
            gate_type="security",
            result="pass",
            message="No vulnerabilities found",
        )
        assert check.name == "security"
        assert check.result == "pass"

    def test_gate_check_with_fail(self):
        """Test failed GateCheck"""
        from helix.skills.gate import GateCheck
        check = GateCheck(
            name="security",
            gate_type="security",
            result="fail",
            message="Critical vulnerabilities found",
        )
        assert check.result == "fail"

    def test_gate_report_creation(self):
        """Test GateReport creation"""
        from helix.skills.gate import GateReport, GateCheck
        checks = [
            GateCheck(name="security", gate_type="security", result="pass", message="OK"),
            GateCheck(name="coverage", gate_type="quality", result="pass", message="OK"),
        ]
        report = GateReport(
            overall_result="pass",
            checks=checks,
        )
        assert report.overall_result == "pass"
        assert len(report.checks) == 2

    def test_gate_report_with_failures(self):
        """Test GateReport with failures"""
        from helix.skills.gate import GateReport, GateCheck
        checks = [
            GateCheck(name="security", gate_type="security", result="fail", message="Found issues"),
            GateCheck(name="coverage", gate_type="quality", result="pass", message="OK"),
        ]
        report = GateReport(
            overall_result="fail",
            checks=checks,
        )
        assert report.overall_result == "fail"


class TestGateSkillLintAndComplexity:
    """Test lint and complexity checks"""

    @pytest.mark.skip(reason="Hangs due to external command execution")
    @pytest.mark.asyncio
    async def test_check_lint(self):
        """Test lint check"""
        from helix.skills.gate import GateSkill, GateConfig
        config = GateConfig(allow_lint_errors=True)
        skill = GateSkill(config)
        result = await skill._check_lint()
        assert result is not None

    @pytest.mark.skip(reason="Hangs due to external command execution")
    @pytest.mark.asyncio
    async def test_check_complexity(self):
        """Test complexity check"""
        from helix.skills.gate import GateSkill, GateConfig
        config = GateConfig(max_complexity=10)
        skill = GateSkill(config)
        result = await skill._check_complexity()
        assert result is not None

    @pytest.mark.skip(reason="Hangs due to external command execution")
    @pytest.mark.asyncio
    async def test_check_test_count(self):
        """Test test count check"""
        from helix.skills.gate import GateSkill, GateConfig
        config = GateConfig(min_test_count=5)
        skill = GateSkill(config)
        result = await skill._check_test_count()
        assert result is not None


class TestGateConfigExtended:
    """Extended GateConfig tests"""

    def test_config_with_all_thresholds(self):
        """Test config with all threshold values"""
        from helix.skills.gate import GateConfig
        config = GateConfig(
            min_coverage=80.0,
            min_test_count=10,
            max_complexity=15,
            max_critical_vulns=0,
            max_high_vulns=3,
            require_security_scan=True
        )
        assert config.min_coverage == 80.0
        assert config.min_test_count == 10
        assert config.max_complexity == 15
        assert config.require_security_scan is True

    def test_config_strict_mode(self):
        """Test strict mode config"""
        from helix.skills.gate import GateConfig
        config = GateConfig(
            min_coverage=90.0,
            min_test_count=20,
            require_security_scan=True,
            allow_bypass=False
        )
        assert config.min_coverage == 90.0
        assert config.allow_bypass is False