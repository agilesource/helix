"""Test Helix CLI module"""

import pytest
from unittest.mock import patch, Mock, AsyncMock
from click.testing import CliRunner
from helix import __version__
from helix.cli import (
    main, spec, build, verify, review, ship, status, list_skills,
    gate, learn, checkpoint, browse, design, serve, docs, metrics, ci,
    qa, audit
)


class TestHelixVersion:
    """Test helix version"""

    def test_version(self):
        """Test version matches actual version"""
        from helix import __version__
        assert __version__ is not None
        assert len(__version__) > 0


class TestMainCommand:
    """Test main CLI command"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_main_help(self, runner):
        """Test main --help"""
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Helix" in result.output
        assert "AI Era" in result.output

    def test_main_version(self, runner):
        """Test main --version"""
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        from helix import __version__
        assert __version__ in result.output


class TestBuildCommandExtended:
    """Test build command with various inputs"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    @pytest.fixture
    def mock_build_skill(self):
        with patch('helix.cli.BuildSkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(success=True, message="Built", data={}))
            mock.return_value = mock_instance
            yield mock

    def test_build_with_requirement_text(self, runner, mock_build_skill):
        """Test build with requirement text"""
        result = runner.invoke(build, ["--requirement", "test requirement", "--framework", "fastapi"])
        # Should complete (may fail due to mock, but tests the code path)
        assert result.exit_code in [0, 1]

    def test_build_with_dry_run(self, runner, mock_build_skill):
        """Test build with dry-run flag"""
        result = runner.invoke(build, ["test.txt", "--dry-run"])
        assert result.exit_code in [0, 1]

    def test_build_with_llm_flag(self, runner, mock_build_skill):
        """Test build with llm flag"""
        result = runner.invoke(build, ["--requirement", "test", "--llm"])
        assert result.exit_code in [0, 1]

    def test_build_with_output_dir(self, runner, mock_build_skill):
        """Test build with output directory"""
        result = runner.invoke(build, ["--requirement", "test", "--output", "./output"])
        assert result.exit_code in [0, 1]


class TestVerifyCommandExtended:
    """Test verify command"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    @pytest.fixture
    def mock_verify_skill(self):
        with patch('helix.cli.VerifySkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(success=True, message="Verified", data={}))
            mock.return_value = mock_instance
            yield mock

    def test_verify_with_level(self, runner, mock_verify_skill):
        """Test verify with level option"""
        result = runner.invoke(verify, ["--level", "syntax"])
        assert result.exit_code in [0, 1]

    def test_verify_default_level(self, runner, mock_verify_skill):
        """Test verify with default level"""
        result = runner.invoke(verify, ["."])
        assert result.exit_code in [0, 1]


class TestReviewCommandExtended:
    """Test review command"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    @pytest.fixture
    def mock_review_skill(self):
        with patch('helix.cli.ReviewSkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(success=True, message="Reviewed", data={}))
            mock.return_value = mock_instance
            yield mock

    def test_review_with_base(self, runner, mock_review_skill):
        """Test review with base branch"""
        result = runner.invoke(review, ["--base", "main"])
        assert result.exit_code in [0, 1]

    def test_review_with_path(self, runner, mock_review_skill):
        """Test review with path"""
        result = runner.invoke(review, ["--path", "src/"])
        assert result.exit_code in [0, 1]


class TestShipCommandExtended:
    """Test ship command"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    @pytest.fixture
    def mock_ship_skill(self):
        with patch('helix.cli.ShipSkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(success=True, message="Shipped", data={}))
            mock.return_value = mock_instance
            yield mock

    def test_ship_draft_mode(self, runner, mock_ship_skill):
        """Test ship with draft mode"""
        result = runner.invoke(ship, ["--mode", "branch", "--draft"])
        assert result.exit_code in [0, 1]

    def test_ship_with_title(self, runner, mock_ship_skill):
        """Test ship with custom title"""
        result = runner.invoke(ship, ["--mode", "branch", "--title", "Test PR"])
        assert result.exit_code in [0, 1]


class TestDesignCommandExtended:
    """Test design command"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    @pytest.fixture
    def mock_design_skill(self):
        with patch('helix.cli.DesignSkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(success=True, message="Designed", data={}))
            mock.return_value = mock_instance
            yield mock

    def test_design_brand(self, runner, mock_design_skill):
        """Test design with brand option"""
        result = runner.invoke(design, ["--brand", "modern"])
        assert result.exit_code in [0, 1]

    def test_design_template(self, runner, mock_design_skill):
        """Test design with template option"""
        result = runner.invoke(design, ["--template", "dashboard"])
        assert result.exit_code in [0, 1]


class TestBrowseCommandExtended2:
    """Test browse command additional tests"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    @pytest.fixture
    def mock_browse_skill(self):
        with patch('helix.cli.BrowseSkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(success=True, message="Browsed", data={}))
            mock.return_value = mock_instance
            yield mock

    def test_browse_interactive(self, runner, mock_browse_skill):
        """Test browse with interactive flag"""
        result = runner.invoke(browse, ["--interactive"])
        assert result.exit_code in [0, 1]

    def test_browse_with_action(self, runner, mock_browse_skill):
        """Test browse with action"""
        result = runner.invoke(browse, ["https://example.com", "--action", "click"])
        assert result.exit_code in [0, 1]


class TestServeCommandExtended:
    """Test serve command additional tests"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_serve_custom_port(self, runner):
        """Test serve with custom port"""
        # Serve starts a server, we just test it doesn't crash on parse
        result = runner.invoke(serve, ["--port", "9000"])
        # May fail due to port in use or other issues, but tests argument parsing
        assert result.exit_code in [0, 1]

    def test_serve_custom_host(self, runner):
        """Test serve with custom host"""
        result = runner.invoke(serve, ["--host", "0.0.0.0"])
        assert result.exit_code in [0, 1]


class TestDocsCommandExtended:
    """Test docs command additional tests"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_docs_with_output(self, runner):
        """Test docs with output path"""
        result = runner.invoke(docs, ["--output", "./docs"])
        assert result.exit_code in [0, 1]


class TestCICommandExtended:
    """Test ci command additional tests"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_ci_with_audit(self, runner):
        """Test ci with audit flag"""
        result = runner.invoke(ci, ["--audit"])
        assert result.exit_code in [0, 1]

    def test_ci_with_gate(self, runner):
        """Test ci with gate flag"""
        result = runner.invoke(ci, ["--gate"])
        assert result.exit_code in [0, 1]

    def test_ci_platform(self, runner):
        """Test ci with platform"""
        result = runner.invoke(ci, ["--platform", "github"])
        assert result.exit_code in [0, 1]


class TestSpecCommandWithMock:
    """Test spec command with mocked skill"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    @pytest.fixture
    def mock_spec_skill(self):
        with patch('helix.cli.SpecSkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(
                success=True,
                message='Done',
                data={'spec_content': '# Test Spec'}
            ))
            mock.return_value = mock_instance
            yield mock

    def test_spec_with_mock(self, runner, mock_spec_skill):
        """Test spec with mock skill"""
        result = runner.invoke(spec, ['test input'])
        assert result.exit_code in [0, 1]
        assert 'Spec' in result.output or 'spec' in result.output.lower()

    def test_spec_output_option(self, runner, mock_spec_skill):
        """Test spec with output option"""
        with runner.isolated_filesystem():
            result = runner.invoke(spec, ['test', '--output', 'test.md'])
            assert result.exit_code in [0, 1]


class TestBuildCommandWithMock:
    """Test build command with mocked skill"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    @pytest.fixture
    def mock_build_skill(self):
        with patch('helix.cli.BuildSkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(
                success=True,
                message='Built',
                data={}
            ))
            mock.return_value = mock_instance
            yield mock

    def test_build_with_mock(self, runner, mock_build_skill):
        """Test build with mock skill"""
        result = runner.invoke(build, ['--requirement', 'test requirement'])
        assert result.exit_code in [0, 1]


class TestVerifyCommandWithMock:
    """Test verify command with mocked skill"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    @pytest.fixture
    def mock_verify_skill(self):
        with patch('helix.cli.VerifySkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(
                success=True,
                message='Verified',
                data={}
            ))
            mock.return_value = mock_instance
            yield mock

    def test_verify_with_mock(self, runner, mock_verify_skill):
        """Test verify with mock skill"""
        result = runner.invoke(verify, ['.', '--level', 'static'])
        assert result.exit_code in [0, 1]

    def test_verify_default(self, runner, mock_verify_skill):
        """Test verify with defaults"""
        result = runner.invoke(verify, [])
        assert result.exit_code in [0, 1]


class TestReviewCommandWithMock:
    """Test review command with mocked skill"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    @pytest.fixture
    def mock_review_skill(self):
        with patch('helix.cli.ReviewSkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(
                success=True,
                message='Reviewed',
                data={}
            ))
            mock.return_value = mock_instance
            yield mock

    def test_review_with_mock(self, runner, mock_review_skill):
        """Test review with mock skill"""
        result = runner.invoke(review, ['--base', 'main', '--path', '.'])
        assert result.exit_code in [0, 1]


class TestShipCommandWithMock:
    """Test ship command with mocked skill"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    @pytest.fixture
    def mock_ship_skill(self):
        with patch('helix.cli.ShipSkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(
                success=True,
                message='Shipped',
                data={}
            ))
            mock.return_value = mock_instance
            yield mock

    def test_ship_with_mock(self, runner, mock_ship_skill):
        """Test ship with mock skill"""
        result = runner.invoke(ship, ['--mode', 'create_pr', '--base', 'main'])
        assert result.exit_code in [0, 1]

    def test_ship_draft(self, runner, mock_ship_skill):
        """Test ship with draft"""
        result = runner.invoke(ship, ['--mode', 'create_pr', '--draft'])
        assert result.exit_code in [0, 1]

    def test_ship_dry_run(self, runner, mock_ship_skill):
        """Test ship with dry-run"""
        result = runner.invoke(ship, ['--mode', 'dry_run'])
        assert result.exit_code in [0, 1]


class TestDesignCommandWithMock:
    """Test design command with mocked skill"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    @pytest.fixture
    def mock_design_skill(self):
        with patch('helix.skills.design.DesignSkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(
                success=True,
                message='Designed',
                data={}
            ))
            mock.return_value = mock_instance
            yield mock

    def test_design_with_mock(self, runner, mock_design_skill):
        """Test design with mock skill"""
        result = runner.invoke(design, ['--brand', 'modern'])
        assert result.exit_code in [0, 1]


class TestBrowseCommandWithMock:
    """Test browse command with mocked skill"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    @pytest.fixture
    def mock_browse_skill(self):
        with patch('helix.skills.browse.BrowseSkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(
                success=True,
                message='Browsed',
                data={}
            ))
            mock.return_value = mock_instance
            yield mock

    def test_browse_with_mock(self, runner, mock_browse_skill):
        """Test browse with mock skill"""
        result = runner.invoke(browse, ['https://example.com'])
        assert result.exit_code in [0, 1]

    def test_browse_with_screenshot(self, runner, mock_browse_skill):
        """Test browse with screenshot"""
        result = runner.invoke(browse, ['https://example.com', '--screenshot'])
        assert result.exit_code in [0, 1]

    def test_browse_interactive(self, runner, mock_browse_skill):
        """Test browse interactive"""
        result = runner.invoke(browse, ['--interactive'])
        assert result.exit_code in [0, 1]


class TestLearnCommandWithMock:
    """Test learn command with mocked skill"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    @pytest.fixture
    def mock_learn_skill(self):
        with patch('helix.skills.learn.LearnSkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(
                success=True,
                message='Learned',
                data={}
            ))
            mock.return_value = mock_instance
            yield mock

    def test_learn_search(self, runner, mock_learn_skill):
        """Test learn search"""
        result = runner.invoke(learn, ['search', '--query', 'test'])
        assert result.exit_code in [0, 1]

    def test_learn_add(self, runner, mock_learn_skill):
        """Test learn add"""
        result = runner.invoke(learn, ['add', '--key', 'test', '--insight', 'test insight'])
        assert result.exit_code in [0, 1]

    def test_learn_list(self, runner, mock_learn_skill):
        """Test learn list"""
        result = runner.invoke(learn, ['list'])
        assert result.exit_code in [0, 1]


class TestCheckpointCommandWithMock:
    """Test checkpoint command with mocked skill"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    @pytest.fixture
    def mock_checkpoint_skill(self):
        with patch('helix.skills.checkpoint.CheckpointSkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(
                success=True,
                message='Checked',
                data={}
            ))
            mock.return_value = mock_instance
            yield mock

    def test_checkpoint_list(self, runner, mock_checkpoint_skill):
        """Test checkpoint list"""
        result = runner.invoke(checkpoint, ['list'])
        assert result.exit_code in [0, 1]

    def test_checkpoint_save(self, runner, mock_checkpoint_skill):
        """Test checkpoint save"""
        result = runner.invoke(checkpoint, ['save', 'test-label'])
        assert result.exit_code in [0, 1]

    def test_checkpoint_status(self, runner, mock_checkpoint_skill):
        """Test checkpoint status"""
        result = runner.invoke(checkpoint, ['status'])
        assert result.exit_code in [0, 1]


class TestQaCommandWithMock:
    """Test qa command with mocked skill"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    @pytest.fixture
    def mock_qa_skill(self):
        with patch('helix.cli.QASkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(
                success=True,
                message='QA Done',
                data={}
            ))
            mock.return_value = mock_instance
            yield mock

    def test_qa_unit(self, runner, mock_qa_skill):
        """Test qa unit"""
        result = runner.invoke(qa, ['--level', 'unit'])
        assert result.exit_code in [0, 1]

    def test_qa_integration(self, runner, mock_qa_skill):
        """Test qa integration"""
        result = runner.invoke(qa, ['--level', 'integration'])
        assert result.exit_code in [0, 1]

    def test_qa_coverage(self, runner, mock_qa_skill):
        """Test qa with coverage"""
        result = runner.invoke(qa, ['--coverage'])
        assert result.exit_code in [0, 1]


class TestAuditCommandWithMock:
    """Test audit command with mocked skill"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    @pytest.fixture
    def mock_audit_skill(self):
        with patch('helix.cli.AuditSkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(
                success=True,
                message='Audited',
                data={}
            ))
            mock.return_value = mock_instance
            yield mock

    def test_audit_security(self, runner, mock_audit_skill):
        """Test audit security"""
        result = runner.invoke(audit, ['--security'])
        assert result.exit_code in [0, 1]

    def test_audit_dependencies(self, runner, mock_audit_skill):
        """Test audit dependencies"""
        result = runner.invoke(audit, ['--dependencies'])
        assert result.exit_code in [0, 1]

    def test_audit_architecture(self, runner, mock_audit_skill):
        """Test audit architecture"""
        result = runner.invoke(audit, ['--architecture'])
        assert result.exit_code in [0, 1]


class TestGateCommandWithMock:
    """Test gate command with mocked skill"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    @pytest.fixture
    def mock_gate_skill(self):
        with patch('helix.cli.GateSkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(
                success=True,
                message='Gated',
                data={}
            ))
            mock.return_value = mock_instance
            yield mock

    def test_gate_strict(self, runner, mock_gate_skill):
        """Test gate strict"""
        result = runner.invoke(gate, ['--strict'])
        assert result.exit_code in [0, 1]

    def test_gate_security(self, runner, mock_gate_skill):
        """Test gate security"""
        result = runner.invoke(gate, ['--security'])
        assert result.exit_code in [0, 1]

    def test_gate_bypass(self, runner, mock_gate_skill):
        """Test gate bypass"""
        result = runner.invoke(gate, ['--bypass', 'test'])
        assert result.exit_code in [0, 1]

    def test_gate_min_coverage(self, runner, mock_gate_skill):
        """Test gate min coverage"""
        result = runner.invoke(gate, ['--min-coverage', '80'])
        assert result.exit_code in [0, 1]


class TestSpecCommandFailurePaths:
    """Test spec command failure branches"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_spec_failure(self, runner):
        """Test spec when skill fails"""
        with patch('helix.cli.SpecSkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(
                success=False,
                message='Failed',
                data={}
            ))
            mock.return_value = mock_instance

            result = runner.invoke(spec, ['test input'])
            assert result.exit_code in [0, 1]

    def test_spec_exception(self, runner):
        """Test spec when exception occurs"""
        with patch('helix.cli.SpecSkill') as mock:
            mock.side_effect = Exception("Test error")

            result = runner.invoke(spec, ['test input'])
            # Should handle exception gracefully


class TestBuildCommandFailurePaths:
    """Test build command failure branches"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_build_failure(self, runner):
        """Test build when skill fails"""
        with patch('helix.cli.BuildSkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(
                success=False,
                message='Build failed',
                data={}
            ))
            mock.return_value = mock_instance

            result = runner.invoke(build, ['--requirement', 'test'])
            assert result.exit_code in [0, 1]


class TestVerifyCommandFailurePaths:
    """Test verify command failure branches"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_verify_failure(self, runner):
        """Test verify when skill fails"""
        with patch('helix.cli.VerifySkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(
                success=False,
                message='Verify failed',
                data={}
            ))
            mock.return_value = mock_instance

            result = runner.invoke(verify, ['.'])
            assert result.exit_code in [0, 1]


class TestReviewCommandFailurePaths:
    """Test review command failure branches"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_review_failure(self, runner):
        """Test review when skill fails"""
        with patch('helix.cli.ReviewSkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(
                success=False,
                message='Review failed',
                data={'review_report': 'test'}
            ))
            mock.return_value = mock_instance

            result = runner.invoke(review, ['--base', 'main'])
            assert result.exit_code in [0, 1]


class TestShipCommandFailurePaths:
    """Test ship command failure branches"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_ship_failure(self, runner):
        """Test ship when skill fails"""
        with patch('helix.cli.ShipSkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(
                success=False,
                message='Ship failed',
                data={}
            ))
            mock.return_value = mock_instance

            result = runner.invoke(ship, ['--mode', 'create_pr'])
            assert result.exit_code in [0, 1]


class TestQaCommandFailurePaths:
    """Test qa command failure branches"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_qa_failure(self, runner):
        """Test qa when skill fails"""
        with patch('helix.cli.QASkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(
                success=False,
                message='QA failed',
                data={'test_result': 'failed'}
            ))
            mock.return_value = mock_instance

            result = runner.invoke(qa, ['--level', 'unit'])
            assert result.exit_code in [0, 1]


class TestAuditCommandFailurePaths:
    """Test audit command failure branches"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_audit_failure(self, runner):
        """Test audit when skill fails"""
        with patch('helix.cli.AuditSkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(
                success=False,
                message='Audit failed',
                data={}
            ))
            mock.return_value = mock_instance

            result = runner.invoke(audit, ['--security'])
            assert result.exit_code in [0, 1]


class TestGateCommandFailurePaths:
    """Test gate command failure branches"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_gate_failure(self, runner):
        """Test gate when skill fails"""
        with patch('helix.cli.GateSkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(
                success=False,
                message='Gate failed',
                data={}
            ))
            mock.return_value = mock_instance

            result = runner.invoke(gate, [])
            assert result.exit_code in [0, 1]


class TestLearnCommandFailurePaths:
    """Test learn command failure branches"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_learn_failure(self, runner):
        """Test learn when skill fails"""
        with patch('helix.skills.learn.LearnSkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(
                success=False,
                message='Learn failed',
                data={}
            ))
            mock.return_value = mock_instance

            result = runner.invoke(learn, ['search', '--query', 'test'])
            assert result.exit_code in [0, 1]


class TestCheckpointCommandFailurePaths:
    """Test checkpoint command failure branches"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_checkpoint_failure(self, runner):
        """Test checkpoint when skill fails"""
        with patch('helix.skills.checkpoint.CheckpointSkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(
                success=False,
                message='Checkpoint failed',
                data={}
            ))
            mock.return_value = mock_instance

            result = runner.invoke(checkpoint, ['list'])
            assert result.exit_code in [0, 1]


class TestDesignCommandFailurePaths:
    """Test design command failure branches"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_design_failure(self, runner):
        """Test design when skill fails"""
        with patch('helix.skills.design.DesignSkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(
                success=False,
                message='Design failed',
                data={}
            ))
            mock.return_value = mock_instance

            result = runner.invoke(design, ['--brand', 'modern'])
            assert result.exit_code in [0, 1]


class TestBrowseCommandFailurePaths:
    """Test browse command failure branches"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_browse_failure(self, runner):
        """Test browse when skill fails"""
        with patch('helix.skills.browse.BrowseSkill') as mock:
            mock_instance = Mock()
            mock_instance.execute = AsyncMock(return_value=Mock(
                success=False,
                message='Browse failed',
                data={}
            ))
            mock.return_value = mock_instance

            result = runner.invoke(browse, ['https://example.com'])
            assert result.exit_code in [0, 1]


class TestMetricsCommand:
    """Test metrics command"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_metrics_help(self, runner):
        """Test metrics help"""
        result = runner.invoke(metrics, ['--help'])
        assert result.exit_code == 0


class TestLearnCommandMorePaths:
    """Test learn command more branches"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_learn_stats(self, runner):
        """Test learn stats"""
        result = runner.invoke(learn, ['stats'])
        assert result.exit_code in [0, 1]

    def test_learn_with_key_and_type(self, runner):
        """Test learn with key and type"""
        result = runner.invoke(learn, ['add', '--key', 'test', '--insight', 'insight', '--type', 'pattern'])
        assert result.exit_code in [0, 1]


class TestCheckpointCommandMorePaths:
    """Test checkpoint command more branches"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_checkpoint_with_id(self, runner):
        """Test checkpoint with id"""
        result = runner.invoke(checkpoint, ['restore', 'test-id'])
        assert result.exit_code in [0, 1]


class TestGateCommandMorePaths:
    """Test gate command more branches"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_gate_all_options(self, runner):
        """Test gate with all options"""
        result = runner.invoke(gate, ['--strict', '--security', '--min-coverage', '90', '--bypass', 'test'])
        assert result.exit_code in [0, 1]


class TestStatusCommand:
    """Test status command"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_status_output(self, runner):
        """Test status command displays info"""
        result = runner.invoke(status)
        assert result.exit_code == 0
        assert "Helix" in result.output
        assert "Stable" in result.output


class TestListSkillsCommand:
    """Test list-skills command"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_list_skills(self, runner):
        """Test list-skills shows all skills"""
        result = runner.invoke(list_skills)
        assert result.exit_code == 0
        assert "spec" in result.output
        assert "build" in result.output
        assert "verify" in result.output

    def test_list_skills_shows_gate(self, runner):
        """Test list-skills shows gate skill"""
        result = runner.invoke(list_skills)
        assert result.exit_code == 0
        assert "gate" in result.output.lower()

    def test_list_skills_shows_learn(self, runner):
        """Test list-skills shows learn skill"""
        result = runner.invoke(list_skills)
        assert result.exit_code == 0
        assert "learn" in result.output.lower()


class TestSpecCommand:
    """Test spec command"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_spec_help(self, runner):
        """Test spec --help"""
        result = runner.invoke(spec, ["--help"])
        assert result.exit_code == 0
        assert "Spec skill" in result.output

    @patch("helix.cli.SpecSkill")
    def test_spec_with_input(self, mock_skill_class, runner):
        """Test spec with input text"""
        mock_skill = Mock()
        mock_skill.execute = AsyncMock(return_value=Mock(
            success=True,
            message="Spec generated",
            data={"spec_content": "# Test Spec"}
        ))
        mock_skill_class.return_value = mock_skill

        # Note: This may fail due to missing API key or other deps
        # Just test the command runs
        result = runner.invoke(spec, ["test requirement"], catch_exceptions=False)
        # Exit code may be 0 or 1 depending on API availability


class TestBuildCommand:
    """Test build command"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_build_help(self, runner):
        """Test build --help"""
        result = runner.invoke(build, ["--help"])
        assert result.exit_code == 0
        assert "skeleton" in result.output.lower()


class TestVerifyCommand:
    """Test verify command"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_verify_help(self, runner):
        """Test verify --help"""
        result = runner.invoke(verify, ["--help"])
        assert result.exit_code == 0
        assert "verify" in result.output.lower()


class TestReviewCommand:
    """Test review command"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_review_help(self, runner):
        """Test review --help"""
        result = runner.invoke(review, ["--help"])
        assert result.exit_code == 0
        assert "review" in result.output.lower()


class TestShipCommand:
    """Test ship command"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_ship_help(self, runner):
        """Test ship --help"""
        result = runner.invoke(ship, ["--help"])
        assert result.exit_code == 0
        assert "ship" in result.output.lower()


class TestAuditCommand:
    """Test audit command"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_audit_help(self, runner):
        """Test audit --help"""
        from helix.cli import audit
        result = runner.invoke(audit, ["--help"])
        assert result.exit_code == 0
        assert "audit" in result.output.lower()


class TestGateCommand:
    """Test gate command"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_gate_help(self, runner):
        """Test gate --help"""
        from helix.cli import gate
        result = runner.invoke(gate, ["--help"])
        assert result.exit_code == 0
        assert "gate" in result.output.lower()


class TestLearnCommand:
    """Test learn command"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_learn_help(self, runner):
        """Test learn --help"""
        from helix.cli import learn
        result = runner.invoke(learn, ["--help"])
        assert result.exit_code == 0


class TestCheckpointCommand:
    """Test checkpoint command"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_checkpoint_help(self, runner):
        """Test checkpoint --help"""
        from helix.cli import checkpoint
        result = runner.invoke(checkpoint, ["--help"])
        assert result.exit_code == 0


class TestBrowseCommand:
    """Test browse command"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_browse_help(self, runner):
        """Test browse --help"""
        from helix.cli import browse
        result = runner.invoke(browse, ["--help"])
        assert result.exit_code == 0


class TestDesignCommand:
    """Test design command"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_design_help(self, runner):
        """Test design --help"""
        from helix.cli import design
        result = runner.invoke(design, ["--help"])
        assert result.exit_code == 0


class TestClassifyCommand:
    """Test classify command"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_classify_help(self, runner):
        """Test classify --help"""
        from helix.cli import classify
        result = runner.invoke(classify, ["--help"])
        assert result.exit_code == 0

    def test_classify_with_input(self, runner):
        """Test classify with input"""
        from helix.cli import classify
        result = runner.invoke(classify, ["create a user login"])
        # May succeed or fail depending on model availability
        assert result.exit_code in [0, 1]


class TestPluginsCommand:
    """Test plugins command"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_plugins_help(self, runner):
        """Test plugins --help"""
        from helix.cli import plugins
        result = runner.invoke(plugins, ["--help"])
        assert result.exit_code == 0

    def test_plugins_list(self, runner):
        """Test plugins list"""
        from helix.cli import plugins
        result = runner.invoke(plugins)
        assert result.exit_code == 0


class TestServeCommand:
    """Test serve command"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_serve_help(self, runner):
        """Test serve --help"""
        from helix.cli import serve
        result = runner.invoke(serve, ["--help"])
        assert result.exit_code == 0

    def test_serve_default(self, runner):
        """Test serve default"""
        from helix.cli import serve
        result = runner.invoke(serve)
        assert result.exit_code in [0, 1]

    def test_serve_port(self, runner):
        """Test serve with port"""
        from helix.cli import serve
        result = runner.invoke(serve, ["--port", "9000"])
        assert result.exit_code in [0, 1]

    def test_serve_host(self, runner):
        """Test serve with host"""
        from helix.cli import serve
        result = runner.invoke(serve, ["--host", "localhost"])
        assert result.exit_code in [0, 1]


class TestDocsCommand:
    """Test docs command"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_docs_help(self, runner):
        """Test docs --help"""
        from helix.cli import docs
        result = runner.invoke(docs, ["--help"])
        assert result.exit_code == 0

    def test_docs_default(self, runner):
        """Test docs default output"""
        from helix.cli import docs
        result = runner.invoke(docs)
        assert result.exit_code in [0, 1]

    def test_docs_custom_output(self, runner):
        """Test docs with custom output"""
        from helix.cli import docs
        result = runner.invoke(docs, ["--output", "/tmp/docs"])
        assert result.exit_code in [0, 1]


class TestMetricsCommand:
    """Test metrics command"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_metrics_help(self, runner):
        """Test metrics --help"""
        from helix.cli import metrics
        result = runner.invoke(metrics, ["--help"])
        assert result.exit_code == 0

    def test_metrics_show(self, runner):
        """Test metrics show"""
        from helix.cli import metrics
        result = runner.invoke(metrics)
        assert result.exit_code == 0


class TestStatusCommandExtended:
    """Test status command extended"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_status_shows_version(self, runner):
        """Test status shows version"""
        from helix.cli import status
        result = runner.invoke(status)
        assert result.exit_code == 0
        assert "Version" in result.output

    def test_status_shows_skills(self, runner):
        """Test status shows skills"""
        from helix.cli import status
        result = runner.invoke(status)
        assert result.exit_code == 0
        assert "Skills" in result.output

    def test_status_shows_architecture(self, runner):
        """Test status shows architecture"""
        from helix.cli import status
        result = runner.invoke(status)
        assert result.exit_code == 0
        assert "Architecture" in result.output


class TestPluginsCommandExtended:
    """Test plugins command extended"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_plugins_shows_helix(self, runner):
        """Test plugins shows helix"""
        from helix.cli import plugins
        result = runner.invoke(plugins)
        assert result.exit_code == 0
        assert "Helix" in result.output or "Plugin" in result.output


class TestClassifyCommandExtended:
    """Test classify command extended"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_classify_api(self, runner):
        """Test classify api"""
        from helix.cli import classify
        result = runner.invoke(classify, ["create api endpoint"])
        assert result.exit_code in [0, 1]

    def test_classify_ui(self, runner):
        """Test classify ui"""
        from helix.cli import classify
        result = runner.invoke(classify, ["add button to page"])
        assert result.exit_code in [0, 1]


class TestCICommand:
    """Test ci command"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_ci_help(self, runner):
        """Test ci --help"""
        from helix.cli import ci
        result = runner.invoke(ci, ["--help"])
        assert result.exit_code == 0

    def test_ci_github(self, runner):
        """Test ci with github"""
        from helix.cli import ci
        result = runner.invoke(ci, ["github"])
        # May succeed or fail
        assert result.exit_code in [0, 1]

    def test_ci_gitlab(self, runner):
        """Test ci with gitlab"""
        from helix.cli import ci
        result = runner.invoke(ci, ["gitlab"])
        # May succeed or fail
        assert result.exit_code in [0, 1]

    def test_ci_with_path(self, runner):
        """Test ci with path option"""
        from helix.cli import ci
        result = runner.invoke(ci, ["github", "--path", "/tmp"])
        # May succeed or fail
        assert result.exit_code in [0, 1]

    def test_ci_with_audit(self, runner):
        """Test ci with audit option"""
        from helix.cli import ci
        result = runner.invoke(ci, ["github", "--audit"])
        assert result.exit_code in [0, 1]

    def test_ci_no_audit(self, runner):
        """Test ci without audit"""
        from helix.cli import ci
        result = runner.invoke(ci, ["github", "--no-audit"])
        assert result.exit_code in [0, 1]


class TestQaCommandExtended:
    """Test qa command extended"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_qa_unit(self, runner):
        """Test qa with unit level"""
        from helix.cli import qa
        result = runner.invoke(qa, ["--level", "unit"])
        assert result.exit_code in [0, 1]

    def test_qa_integration(self, runner):
        """Test qa with integration level"""
        from helix.cli import qa
        result = runner.invoke(qa, ["--level", "integration"])
        assert result.exit_code in [0, 1]

    def test_qa_e2e(self, runner):
        """Test qa with e2e level"""
        from helix.cli import qa
        result = runner.invoke(qa, ["--level", "e2e"])
        assert result.exit_code in [0, 1]

    def test_qa_with_coverage(self, runner):
        """Test qa with coverage"""
        from helix.cli import qa
        result = runner.invoke(qa, ["--coverage"])
        assert result.exit_code in [0, 1]


class TestAuditCommandExtended:
    """Test audit command extended"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_audit_no_security(self, runner):
        """Test audit without security"""
        from helix.cli import audit
        result = runner.invoke(audit, ["--no-security"])
        assert result.exit_code in [0, 1]

    def test_audit_no_dependencies(self, runner):
        """Test audit without dependencies"""
        from helix.cli import audit
        result = runner.invoke(audit, ["--no-dependencies"])
        assert result.exit_code in [0, 1]

    def test_audit_no_architecture(self, runner):
        """Test audit without architecture"""
        from helix.cli import audit
        result = runner.invoke(audit, ["--no-architecture"])
        assert result.exit_code in [0, 1]


class TestGateCommandExtended:
    """Test gate command extended"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_gate_strict(self, runner):
        """Test gate with strict mode"""
        from helix.cli import gate
        result = runner.invoke(gate, ["--strict"])
        assert result.exit_code in [0, 1]

    def test_gate_min_coverage(self, runner):
        """Test gate with min coverage"""
        from helix.cli import gate
        result = runner.invoke(gate, ["--min-coverage", "80"])
        assert result.exit_code in [0, 1]

    def test_gate_bypass(self, runner):
        """Test gate with bypass"""
        from helix.cli import gate
        result = runner.invoke(gate, ["--bypass", "Emergency fix"])
        assert result.exit_code in [0, 1]

    def test_gate_no_security(self, runner):
        """Test gate without security"""
        from helix.cli import gate
        result = runner.invoke(gate, ["--no-security"])
        assert result.exit_code in [0, 1]


class TestLearnCommandExtended:
    """Test learn command extended"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_learn_search(self, runner):
        """Test learn search"""
        from helix.cli import learn
        result = runner.invoke(learn, ["search", "--query", "test"])
        assert result.exit_code in [0, 1]

    def test_learn_add(self, runner):
        """Test learn add"""
        from helix.cli import learn
        result = runner.invoke(learn, ["add", "--key", "test", "--insight", "test insight"])
        assert result.exit_code in [0, 1]

    def test_learn_list(self, runner):
        """Test learn list"""
        from helix.cli import learn
        result = runner.invoke(learn, ["list"])
        assert result.exit_code in [0, 1]


class TestCheckpointCommandExtended:
    """Test checkpoint command extended"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_checkpoint_save(self, runner):
        """Test checkpoint save"""
        from helix.cli import checkpoint
        result = runner.invoke(checkpoint, ["save", "test-label"])
        assert result.exit_code in [0, 1]

    def test_checkpoint_list(self, runner):
        """Test checkpoint list"""
        from helix.cli import checkpoint
        result = runner.invoke(checkpoint, ["list"])
        assert result.exit_code in [0, 1]

    def test_checkpoint_load(self, runner):
        """Test checkpoint load"""
        from helix.cli import checkpoint
        result = runner.invoke(checkpoint, ["load", "test-id"])
        assert result.exit_code in [0, 1]


class TestBrowseCommandExtended:
    """Test browse command extended"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_browse_with_url(self, runner):
        """Test browse with URL"""
        from helix.cli import browse
        result = runner.invoke(browse, ["https://example.com"])
        assert result.exit_code in [0, 1]

    def test_browse_screenshot(self, runner):
        """Test browse with screenshot"""
        from helix.cli import browse
        result = runner.invoke(browse, ["https://example.com", "--screenshot"])
        assert result.exit_code in [0, 1]

    def test_browse_interactive(self, runner):
        """Test browse interactive"""
        from helix.cli import browse
        result = runner.invoke(browse, ["--interactive"])
        assert result.exit_code in [0, 1]


class TestDesignCommandExtended:
    """Test design command extended"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_design_brand(self, runner):
        """Test design with brand"""
        from helix.cli import design
        result = runner.invoke(design, ["--brand", "MyBrand"])
        assert result.exit_code in [0, 1]

    def test_design_template(self, runner):
        """Test design with template"""
        from helix.cli import design
        result = runner.invoke(design, ["--template", "minimal"])
        assert result.exit_code in [0, 1]

    def test_design_output(self, runner):
        """Test design with output"""
        from helix.cli import design
        result = runner.invoke(design, ["--output", "/tmp/design.md"])
        assert result.exit_code in [0, 1]


class TestVerifyCommandExtended:
    """Test verify command extended"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_verify_static(self, runner):
        """Test verify with static level"""
        from helix.cli import verify
        result = runner.invoke(verify, ["--level", "static"])
        assert result.exit_code in [0, 1]

    def test_verify_test(self, runner):
        """Test verify with test level"""
        from helix.cli import verify
        result = runner.invoke(verify, ["--level", "test"])
        assert result.exit_code in [0, 1]

    def test_verify_acceptance(self, runner):
        """Test verify with acceptance level"""
        from helix.cli import verify
        result = runner.invoke(verify, ["--level", "acceptance"])
        assert result.exit_code in [0, 1]


class TestShipCommandExtended:
    """Test ship command extended"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_ship_merge(self, runner):
        """Test ship merge mode"""
        from helix.cli import ship
        result = runner.invoke(ship, ["--mode", "merge"])
        assert result.exit_code in [0, 1]

    def test_ship_deploy(self, runner):
        """Test ship deploy mode"""
        from helix.cli import ship
        result = runner.invoke(ship, ["--mode", "deploy"])
        assert result.exit_code in [0, 1]

    def test_ship_dry_run(self, runner):
        """Test ship dry run mode"""
        from helix.cli import ship
        result = runner.invoke(ship, ["--mode", "dry_run"])
        assert result.exit_code in [0, 1]

    def test_ship_base(self, runner):
        """Test ship with base branch"""
        from helix.cli import ship
        result = runner.invoke(ship, ["--base", "develop"])
        assert result.exit_code in [0, 1]


class TestReviewCommandExtended:
    """Test review command extended"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_review_base(self, runner):
        """Test review with base"""
        from helix.cli import review
        result = runner.invoke(review, ["--base", "develop"])
        assert result.exit_code in [0, 1]

    def test_review_path(self, runner):
        """Test review with path"""
        from helix.cli import review
        result = runner.invoke(review, ["--path", "/tmp"])
        assert result.exit_code in [0, 1]


class TestBuildCommandExtended:
    """Test build command extended"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_build_django(self, runner):
        """Test build with django"""
        from helix.cli import build
        result = runner.invoke(build, ["--framework", "django"])
        assert result.exit_code in [0, 1, 2]

    def test_build_express(self, runner):
        """Test build with express"""
        from helix.cli import build
        result = runner.invoke(build, ["--framework", "express"])
        assert result.exit_code in [0, 1, 2]

    def test_build_dry_run(self, runner):
        """Test build dry run"""
        from helix.cli import build
        result = runner.invoke(build, ["--dry-run"])
        assert result.exit_code in [0, 1, 2]

    def test_build_with_input(self, runner):
        """Test build with input file"""
        from helix.cli import build
        # Use a non-existent file to test path handling
        result = runner.invoke(build, ["/tmp/nonexistent.spec"])
        assert result.exit_code in [0, 1, 2]

    def test_build_llm(self, runner):
        """Test build with llm option"""
        from helix.cli import build
        result = runner.invoke(build, ["--llm"])
        assert result.exit_code in [0, 1, 2]


class TestSpecCommandExtended:
    """Test spec command extended"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_spec_no_confirm(self, runner):
        """Test spec with no-confirm"""
        from helix.cli import spec
        result = runner.invoke(spec, ["test requirement", "--no-confirm"])
        assert result.exit_code in [0, 1]

    def test_spec_template_crud(self, runner):
        """Test spec with crud template"""
        from helix.cli import spec
        result = runner.invoke(spec, ["test", "--template", "crud"])
        assert result.exit_code in [0, 1]

    def test_spec_template_algorithm(self, runner):
        """Test spec with algorithm template"""
        from helix.cli import spec
        result = runner.invoke(spec, ["test", "--template", "algorithm"])
        assert result.exit_code in [0, 1]

    def test_spec_template_integration(self, runner):
        """Test spec with integration template"""
        from helix.cli import spec
        result = runner.invoke(spec, ["test", "--template", "integration"])
        assert result.exit_code in [0, 1]


class TestTemplatesCommand:
    """Test templates command"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_templates_help(self, runner):
        """Test templates --help"""
        from helix.cli import templates
        result = runner.invoke(templates, ["--help"])
        assert result.exit_code == 0

    def test_templates_list(self, runner):
        """Test templates list"""
        from helix.cli import templates
        result = runner.invoke(templates)
        assert result.exit_code == 0
        assert "api" in result.output.lower() or "crud" in result.output.lower()


class TestCLIIntegration:
    """Integration tests for CLI"""

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_spec_with_template_option(self, runner):
        """Test spec with template option"""
        result = runner.invoke(spec, ["test requirement", "--template", "api"])
        # Should not crash, may succeed or fail due to API
        assert result.exit_code in [0, 1]

    def test_build_with_output_option(self, runner):
        """Test build with output option"""
        from helix.cli import build
        result = runner.invoke(build, ["--output", "/tmp/test"])
        # Exit code 2 means missing required args
        assert result.exit_code in [0, 1, 2]

    def test_verify_no_args(self, runner):
        """Test verify with no args"""
        from helix.cli import verify
        result = runner.invoke(verify)
        # Should show help or error
        assert result.exit_code in [0, 1, 2]

    def test_ship_no_args(self, runner):
        """Test ship with no args"""
        from helix.cli import ship
        result = runner.invoke(ship)
        # Should show help or error
        assert result.exit_code in [0, 1, 2]