"""Test Browse Skill"""

import pytest
from helix.skills.browse import BrowseConfig, BrowseSkill
from helix.skills.base import SkillConfig


class TestBrowseSkill:
    """Test BrowseSkill"""

    @pytest.fixture
    def skill(self):
        return BrowseSkill()

    def test_skill_init(self, skill):
        """Test skill initialization"""
        assert skill.name == "browse"

    def test_skill_category(self, skill):
        """Test skill category"""
        assert skill.category.value == "infrastructure"

    def test_skill_status(self, skill):
        """Test skill status"""
        assert skill.status.value == "stable"

    def test_skill_examples(self, skill):
        """Test skill examples"""
        assert len(skill.examples) > 0

    def test_skill_description(self, skill):
        """Test skill description"""
        assert len(skill.description) > 0

    def test_skill_with_custom_config(self, skill):
        """Test skill with custom config"""
        config = SkillConfig()
        skill2 = BrowseSkill(config)
        assert skill2.config is config


class TestBrowseConfig:
    """Test BrowseConfig dataclass"""

    def test_browse_config_defaults(self):
        """Test default configuration"""
        config = BrowseConfig()
        assert config.headless is True
        assert config.timeout == 30
        assert config.viewport == (1280, 720)
        assert config.screenshot_dir == ".helix/screenshots"

    def test_browse_config_custom(self):
        """Test custom configuration"""
        config = BrowseConfig(
            headless=False,
            timeout=60,
            viewport=(1920, 1080),
            screenshot_dir="/tmp/shots"
        )
        assert config.headless is False
        assert config.timeout == 60
        assert config.viewport == (1920, 1080)
        assert config.screenshot_dir == "/tmp/shots"

    def test_browse_config_viewport(self):
        """Test viewport configuration"""
        config = BrowseConfig(viewport=(3840, 2160))
        assert config.viewport == (3840, 2160)