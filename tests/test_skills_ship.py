"""Test Ship Skill"""

import pytest
from helix.skills.ship import ShipSkill, ShipMode, ShipConfig, ShipResult
from helix.skills.base import SkillConfig


class TestShipSkill:
    """Test ShipSkill"""

    @pytest.fixture
    def skill(self):
        return ShipSkill()

    def test_skill_init(self, skill):
        """Test skill initialization"""
        assert skill.name == "ship"


class TestShipMode:
    """Test ShipMode"""

    def test_ship_mode_values(self):
        """Test ship mode enum values"""
        assert ShipMode.CREATE_PR.value == "create_pr"
        assert ShipMode.MERGE.value == "merge"
        assert ShipMode.DEPLOY.value == "deploy"


class TestShipConfig:
    """Test ShipConfig"""

    def test_config_defaults(self):
        """Test config default values"""
        config = ShipConfig()
        assert config.mode == ShipMode.CREATE_PR
        assert config.base_branch == "main"


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