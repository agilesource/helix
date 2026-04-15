"""Test Ship Skill"""

import pytest
from helix.skills.ship import ShipSkill, ShipMode, ShipConfig, ShipResult
from helix.skills.base import SkillConfig, SkillCategory


class TestShipSkill:
    """Test ShipSkill"""

    @pytest.fixture
    def skill(self):
        return ShipSkill()

    def test_skill_init(self, skill):
        """Test skill initialization"""
        assert skill.name == "ship"
        assert skill.category == SkillCategory.EXECUTION

    def test_skill_examples(self, skill):
        """Test skill examples"""
        assert len(skill.examples) > 0

    def test_skill_description(self, skill):
        """Test skill description"""
        assert len(skill.description) > 0

    def test_skill_with_config(self, skill):
        """Test skill with config"""
        config = SkillConfig()
        skill2 = ShipSkill(config)
        assert skill2.config is config


class TestShipMode:
    """Test ShipMode"""

    def test_ship_mode_values(self):
        """Test ship mode enum values"""
        assert ShipMode.CREATE_PR.value == "create_pr"
        assert ShipMode.MERGE.value == "merge"
        assert ShipMode.DEPLOY.value == "deploy"
        assert ShipMode.DRY_RUN.value == "dry_run"

    def test_ship_mode_all(self):
        """Test all ship modes"""
        modes = list(ShipMode)
        assert len(modes) >= 4


class TestShipConfig:
    """Test ShipConfig"""

    def test_config_defaults(self):
        """Test config default values"""
        config = ShipConfig()
        assert config.mode == ShipMode.CREATE_PR
        assert config.base_branch == "main"
        assert config.auto_merge is False
        assert config.delete_branch is True

    def test_config_custom(self):
        """Test config with custom values"""
        config = ShipConfig(
            mode=ShipMode.DEPLOY,
            base_branch="develop",
            auto_merge=True,
            delete_branch=False
        )
        assert config.mode == ShipMode.DEPLOY
        assert config.base_branch == "develop"
        assert config.auto_merge is True
        assert config.delete_branch is False


class TestShipResult:
    """Test ShipResult"""

    def test_result_creation(self):
        """Test creating a ship result"""
        result = ShipResult(
            success=True,
            message="Shipped successfully",
            pr_url="https://github.com/test/pr/1"
        )
        assert result.success is True
        assert result.pr_url == "https://github.com/test/pr/1"

    def test_result_failure(self):
        """Test failure result"""
        result = ShipResult(
            success=False,
            message="Build failed",
            pr_url=""
        )
        assert result.success is False
        assert "failed" in result.message.lower()

    def test_result_with_deploy_url(self):
        """Test result with deploy URL"""
        result = ShipResult(
            success=True,
            message="Deployed",
            pr_url="",
            deploy_url="https://example.com"
        )
        assert result.deploy_url == "https://example.com"