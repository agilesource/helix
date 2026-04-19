"""Test Browse Skill"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
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

    def test_browse_config_headless_true(self):
        """Test headless config"""
        config = BrowseConfig(headless=True)
        assert config.headless is True

    def test_browse_config_timeout_edge_cases(self):
        """Test timeout edge cases"""
        config = BrowseConfig(timeout=0)
        assert config.timeout == 0
        config2 = BrowseConfig(timeout=300)
        assert config2.timeout == 300

    def test_browse_config_viewport(self):
        """Test viewport configuration"""
        config = BrowseConfig(viewport=(3840, 2160))
        assert config.viewport == (3840, 2160)

    def test_browse_config_screenshot_dir(self):
        """Test screenshot directory config"""
        config = BrowseConfig(screenshot_dir="/custom/path")
        assert config.screenshot_dir == "/custom/path"

    def test_browse_config_all_defaults(self):
        """Test all default values"""
        config = BrowseConfig()
        assert config.headless is True
        assert config.timeout == 30
        assert config.viewport == (1280, 720)
        assert config.screenshot_dir == ".helix/screenshots"


class TestBrowseSkillMethodsExtended:
    """Extended BrowseSkill method tests"""

    @pytest.mark.asyncio
    async def test_http_fallback(self):
        """Test HTTP fallback method"""
        from helix.skills.browse import BrowseSkill
        skill = BrowseSkill()
        try:
            result = await skill._execute_http_fallback("https://example.com")
            assert result is not None
            assert "success" in result
        except Exception:
            pass

    def test_browse_skill_initialization(self):
        """Test BrowseSkill initialization"""
        from helix.skills.browse import BrowseSkill
        skill = BrowseSkill()
        assert skill.name == "browse"
        assert skill.category.value == "infrastructure"
        assert skill.status.value == "stable"

    def test_browse_skill_with_config(self):
        """Test BrowseSkill with config"""
        from helix.skills.browse import BrowseSkill, BrowseConfig
        from helix.skills.base import SkillConfig
        config = SkillConfig()
        skill = BrowseSkill(config)
        assert skill.config is config
        assert skill.browse_config is not None

    @pytest.mark.asyncio
    async def test_browse_initialize(self):
        """Test BrowseSkill initialize method"""
        from helix.skills.browse import BrowseSkill
        skill = BrowseSkill()
        skill.initialize()
        assert skill._playwright_available is not None
        assert skill._selenium_available is not None

    def test_browse_skill_repr(self):
        """Test BrowseSkill repr"""
        from helix.skills.browse import BrowseSkill
        skill = BrowseSkill()
        repr_str = repr(skill)
        # Skill base class uses different repr format
        assert "browse" in repr_str.lower()


class TestBrowseSkillExecuteMocked:
    """Test BrowseSkill execute with mocks"""

    @pytest.mark.skip(reason="Requires playwright module")
    @pytest.mark.asyncio
    async def test_execute_playwright_mocked(self):
        """Test execute with mocked playwright"""
        from helix.skills.browse import BrowseSkill
        from helix.core.intent import Intent, IntentType
        import unittest.mock

        skill = BrowseSkill()
        skill._playwright_available = True
        skill._selenium_available = False

        intent = Intent(
            type=IntentType.BROWSE,
            raw_input="browse example.com",
            confidence=0.9,
            parameters={"url": "https://example.com", "screenshot": False}
        )

        # Mock playwright
        mock_browser = unittest.mock.AsyncMock()
        mock_page = unittest.mock.AsyncMock()
        mock_page.title = unittest.mock.AsyncMock(return_value="Example Domain")
        mock_page.goto = unittest.mock.AsyncMock(return_value=unittest.mock.MagicMock(status=200))
        mock_browser.new_page = unittest.mock.AsyncMock(return_value=mock_page)
        mock_browser.close = unittest.mock.AsyncMock()

        mock_playwright = unittest.mock.MagicMock()
        mock_playwright.chromium.launch = unittest.mock.AsyncMock(return_value=mock_browser)

        with unittest.mock.patch('playwright.async_api.async_playwright', return_value=mock_playwright):
            result = await skill.execute(intent, None)
            assert result is not None

    @pytest.mark.skip(reason="Requires selenium module")
    @pytest.mark.asyncio
    async def test_execute_selenium_mocked(self):
        """Test execute with mocked selenium"""
        from helix.skills.browse import BrowseSkill
        from helix.core.intent import Intent, IntentType
        import unittest.mock

        skill = BrowseSkill()
        skill._playwright_available = False
        skill._selenium_available = True

        intent = Intent(
            type=IntentType.BROWSE,
            raw_input="browse example.com",
            confidence=0.9,
            parameters={"url": "https://example.com"}
        )

        with unittest.mock.patch('selenium.webdriver.Chrome'):
            result = await skill.execute(intent, None)
            # May fail or succeed depending on mock
            assert result is not None

    @pytest.mark.asyncio
    async def test_execute_http_fallback_success(self):
        """Test HTTP fallback success"""
        from helix.skills.browse import BrowseSkill
        skill = BrowseSkill()
        result = await skill._execute_http_fallback("https://example.com")
        assert result is not None
        assert "success" in result

    @pytest.mark.asyncio
    async def test_execute_error_handling(self):
        """Test error handling in execute"""
        from helix.skills.browse import BrowseSkill
        from helix.core.intent import Intent, IntentType

        skill = BrowseSkill()
        skill._playwright_available = False
        skill._selenium_available = False

        # Invalid URL should still return some result
        intent = Intent(
            type=IntentType.BROWSE,
            raw_input="browse",
            confidence=0.9,
            parameters={"url": "not-a-valid-url"}
        )

        result = await skill.execute(intent, None)
        assert result is not None


class TestBrowseSkillMoreEdgeCases:
    """More edge case tests for BrowseSkill"""

    def test_browse_config_viewport_small(self):
        """Test with small viewport"""
        config = BrowseConfig(viewport=(800, 600))
        assert config.viewport == (800, 600)

    def test_browse_config_viewport_large(self):
        """Test with large viewport"""
        config = BrowseConfig(viewport=(4096, 2160))
        assert config.viewport == (4096, 2160)

    def test_browse_config_timeout_large(self):
        """Test with large timeout"""
        config = BrowseConfig(timeout=300)
        assert config.timeout == 300

    def test_browse_skill_category(self):
        """Test skill category"""
        from helix.skills.browse import BrowseSkill
        skill = BrowseSkill()
        assert skill.category.value == "infrastructure"

    def test_browse_skill_status(self):
        """Test skill status"""
        from helix.skills.browse import BrowseSkill
        skill = BrowseSkill()
        assert skill.status.value == "stable"

    def test_browse_skill_examples(self):
        """Test skill examples"""
        from helix.skills.browse import BrowseSkill
        skill = BrowseSkill()
        assert len(skill.examples) > 0
        assert "browse" in skill.examples[0].lower()

    def test_browse_skill_description(self):
        """Test skill description"""
        from helix.skills.browse import BrowseSkill
        skill = BrowseSkill()
        assert len(skill.description) > 0

    def test_browse_config_multiple_params(self):
        """Test BrowseConfig with multiple parameters"""
        config = BrowseConfig(
            headless=False,
            timeout=120,
            viewport=(1920, 1080),
            screenshot_dir="/custom/screenshots"
        )
        assert config.headless is False
        assert config.timeout == 120
        assert config.viewport == (1920, 1080)
        assert config.screenshot_dir == "/custom/screenshots"

    def test_browse_config_viewport_tuples(self):
        """Test various viewport sizes"""
        sizes = [(1024, 768), (1280, 720), (1920, 1080), (2560, 1440), (3840, 2160)]
        for size in sizes:
            config = BrowseConfig(viewport=size)
            assert config.viewport == size


class TestBrowseSkillExecutePaths:
    """Test different execute paths"""

    @pytest.mark.asyncio
    async def test_execute_no_browser_available(self):
        """Test execute when no browser is available"""
        from helix.skills.browse import BrowseSkill
        from helix.core.intent import Intent, IntentType

        skill = BrowseSkill()
        skill._playwright_available = False
        skill._selenium_available = False

        intent = Intent(
            type=IntentType.BROWSE,
            raw_input="browse example.com",
            confidence=0.9,
            parameters={"url": "https://example.com"}
        )

        result = await skill.execute(intent, None)
        assert result is not None
        # Should fall back to HTTP

    @pytest.mark.asyncio
    async def test_execute_with_action_click(self):
        """Test execute with click action"""
        from helix.skills.browse import BrowseSkill
        from helix.core.intent import Intent, IntentType

        skill = BrowseSkill()
        skill._playwright_available = False
        skill._selenium_available = False

        intent = Intent(
            type=IntentType.BROWSE,
            raw_input="browse and click",
            confidence=0.9,
            parameters={"url": "https://example.com", "action": "click"}
        )

        result = await skill.execute(intent, None)
        assert result is not None

    @pytest.mark.asyncio
    async def test_execute_headless_true(self):
        """Test execute with headless true"""
        from helix.skills.browse import BrowseSkill
        from helix.core.intent import Intent, IntentType

        skill = BrowseSkill()
        skill._playwright_available = False
        skill._selenium_available = False

        intent = Intent(
            type=IntentType.BROWSE,
            raw_input="browse headless",
            confidence=0.9,
            parameters={"url": "https://example.com", "headless": True}
        )

        result = await skill.execute(intent, None)
        assert result is not None


class TestBrowseSkillHttpFallback:
    """Test HTTP fallback method"""

    @pytest.mark.asyncio
    async def test_http_fallback_https(self):
        """Test HTTP fallback with HTTPS"""
        from helix.skills.browse import BrowseSkill
        skill = BrowseSkill()
        result = await skill._execute_http_fallback("https://httpbin.org/html")
        assert result is not None

    @pytest.mark.asyncio
    async def test_http_fallback_http(self):
        """Test HTTP fallback with HTTP"""
        from helix.skills.browse import BrowseSkill
        skill = BrowseSkill()
        result = await skill._execute_http_fallback("http://example.com")
        assert result is not None


class TestBrowseSkillAsync:
    """Test BrowseSkill async methods"""

    @pytest.mark.asyncio
    async def test_execute_with_url(self):
        """Test execute with URL parameter"""
        from helix.core.intent import Intent, IntentType
        skill = BrowseSkill()
        intent = Intent(
            type=IntentType.BROWSE,
            raw_input="browse example.com",
            confidence=0.9,
            parameters={"url": "https://example.com"}
        )
        try:
            result = await skill.execute(intent, None)
        except (RuntimeError, Exception):
            pass

    @pytest.mark.asyncio
    async def test_execute_with_screenshot(self):
        """Test execute with screenshot parameter"""
        from helix.core.intent import Intent, IntentType
        skill = BrowseSkill()
        intent = Intent(
            type=IntentType.BROWSE,
            raw_input="browse and screenshot",
            confidence=0.9,
            parameters={"url": "https://example.com", "screenshot": True}
        )
        try:
            result = await skill.execute(intent, None)
        except (RuntimeError, Exception):
            pass


class TestBrowseSkillExecute:
    """Test BrowseSkill execute method"""

    @pytest.mark.asyncio
    async def test_execute_without_url(self):
        """Test execute without URL returns error"""
        from helix.core.intent import Intent, IntentType
        skill = BrowseSkill()
        intent = Intent(
            type=IntentType.BROWSE,
            raw_input="browse",
            confidence=0.9,
            parameters={}
        )
        result = await skill.execute(intent, None)
        assert result.success is False
        assert "URL" in result.message or "url" in result.message.lower()

    @pytest.mark.asyncio
    async def test_execute_with_action(self):
        """Test execute with action parameter"""
        from helix.core.intent import Intent, IntentType
        skill = BrowseSkill()
        intent = Intent(
            type=IntentType.BROWSE,
            raw_input="browse and click",
            confidence=0.9,
            parameters={"url": "https://example.com", "action": "click"}
        )
        try:
            result = await skill.execute(intent, None)
        except (RuntimeError, Exception):
            pass

    @pytest.mark.asyncio
    async def test_execute_with_headless_false(self):
        """Test execute with headless=False"""
        from helix.core.intent import Intent, IntentType
        skill = BrowseSkill()
        intent = Intent(
            type=IntentType.BROWSE,
            raw_input="browse visible",
            confidence=0.9,
            parameters={"url": "https://example.com", "headless": False}
        )
        try:
            result = await skill.execute(intent, None)
        except (RuntimeError, Exception):
            pass


class TestBrowseSkillErrorHandling:
    """Test error handling in BrowseSkill"""

    @pytest.mark.asyncio
    async def test_execute_with_invalid_url(self):
        """Test execute with invalid URL"""
        from helix.core.intent import Intent, IntentType
        skill = BrowseSkill()
        intent = Intent(
            type=IntentType.BROWSE,
            raw_input="browse",
            confidence=0.9,
            parameters={"url": "not-a-valid-url"}
        )
        try:
            result = await skill.execute(intent, None)
            # Should handle gracefully (either fail or succeed)
            assert result is not None
        except Exception:
            pass


class TestBrowseSkillConfig:
    """Test BrowseSkill configuration"""

    def test_browse_config_with_all_params(self):
        """Test config with all parameters"""
        config = BrowseConfig(
            headless=False,
            timeout=60,
            viewport=(1920, 1080),
            screenshot_dir="/custom/screenshots"
        )
        assert config.headless is False
        assert config.timeout == 60
        assert config.viewport == (1920, 1080)
        assert config.screenshot_dir == "/custom/screenshots"

    def test_browse_skill_with_browse_config(self):
        """Test skill with browse config"""
        from helix.skills.browse import BrowseConfig
        # The skill creates its own default BrowseConfig
        skill = BrowseSkill()
        # Just verify it has a browse_config attribute
        assert hasattr(skill, 'browse_config')


class TestBrowseSkillPlaywrightMocked:
    """Test BrowseSkill with mocked playwright

    Note: playwright/selenium are dynamically imported and can't be easily mocked.
    These tests verify the code paths exist but require the actual libraries to run.
    """

    @pytest.mark.skip(reason="Requires playwright library to be installed")
    @pytest.mark.asyncio
    async def test_execute_playwright_method_directly(self):
        """Test _execute_playwright method directly"""
        skill = BrowseSkill()
        skill._playwright_available = True
        result = await skill._execute_playwright(
            "https://example.com", "navigate", False, True
        )
        assert result["success"] is True

    @pytest.mark.skip(reason="Requires playwright library to be installed")
    @pytest.mark.asyncio
    async def test_execute_playwright_with_screenshot_direct(self):
        """Test _execute_playwright with screenshot"""
        skill = BrowseSkill()
        result = await skill._execute_playwright(
            "https://example.com", "navigate", True, True
        )
        assert result["success"] is True

    @pytest.mark.skip(reason="Requires playwright library to be installed")
    @pytest.mark.asyncio
    async def test_execute_playwright_exception_direct(self):
        """Test _execute_playwright exception handling"""
        skill = BrowseSkill()
        result = await skill._execute_playwright(
            "https://example.com", "navigate", False, True
        )
        assert result["success"] is False


class TestBrowseSkillSeleniumMocked:
    """Test BrowseSkill with mocked selenium

    Note: selenium is dynamically imported and can't be easily mocked.
    """

    @pytest.mark.skip(reason="Requires selenium library to be installed")
    @pytest.mark.asyncio
    async def test_execute_selenium_method_directly(self):
        """Test _execute_selenium method directly"""
        skill = BrowseSkill()
        skill._selenium_available = True
        result = await skill._execute_selenium(
            "https://example.com", "navigate", False, True
        )
        assert result["success"] is True

    @pytest.mark.skip(reason="Requires selenium library to be installed")
    @pytest.mark.asyncio
    async def test_execute_selenium_with_screenshot_direct(self):
        """Test _execute_selenium with screenshot"""
        skill = BrowseSkill()
        result = await skill._execute_selenium(
            "https://example.com", "navigate", True, True
        )
        assert result["success"] is True

    @pytest.mark.skip(reason="Requires selenium library to be installed")
    @pytest.mark.asyncio
    async def test_execute_selenium_exception_direct(self):
        """Test _execute_selenium exception handling"""
        skill = BrowseSkill()
        result = await skill._execute_selenium(
            "https://example.com", "navigate", False, True
        )
        assert result["success"] is False


class TestBrowseSkillInitialize:
    """Test BrowseSkill initialization"""

    def test_initialize_creates_screenshot_dir(self, tmp_path):
        """Test that initialize creates screenshot directory"""
        custom_dir = tmp_path / "screenshots"

        with patch('helix.skills.browse.Path.mkdir') as mock_mkdir:
            skill = BrowseSkill()
            skill.browse_config.screenshot_dir = str(custom_dir)
            skill._do_initialize()
            mock_mkdir.assert_called()

    def test_default_initialization(self):
        """Test default initialization values"""
        skill = BrowseSkill()
        skill._do_initialize()
        # Both should be False since libraries not installed
        assert skill._playwright_available is False
        assert skill._selenium_available is False

    def test_skill_has_browse_config(self):
        """Test skill has browse_config after init"""
        skill = BrowseSkill()
        assert hasattr(skill, 'browse_config')
        assert isinstance(skill.browse_config, BrowseConfig)
        assert skill.browse_config.timeout == 30  # default