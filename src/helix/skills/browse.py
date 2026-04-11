"""
Helix Browse Skill - Browser Control

Helix-native browser automation for:
- E2E testing
- Visual regression
- Site verification
- Bug evidence capture
"""

import asyncio
import json
import base64
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from helix.skills.base import Skill, SkillResult, SkillConfig, SkillCategory, SkillStatus
from helix.core.intent import Intent, IntentType
from helix.core.context import HelixContext


@dataclass
class BrowseConfig:
    """Browse configuration"""
    headless: bool = True
    screenshot_dir: str = ".helix/screenshots"
    timeout: int = 30
    viewport: tuple = (1280, 720)


class BrowseSkill(Skill):
    """
    Browse Skill - Browser Control

    Helix-native browser automation for testing and verification
    """

    name = "browse"
    description = "Browser control - E2E testing, visual regression, site verification"
    category = SkillCategory.INFRASTRUCTURE
    status = SkillStatus.STABLE

    examples = [
        "helix browse https://example.com",
        "helix browse https://example.com --screenshot",
        "helix browse --interactive",
    ]

    def __init__(self, config: Optional[SkillConfig] = None):
        super().__init__(config)
        self.browse_config = BrowseConfig()
        self._playwright_available = None
        self._selenium_available = None

    def _do_initialize(self) -> None:
        """Initialize browse skill"""
        # Check available browser automation tools
        try:
            import playwright
            self._playwright_available = True
        except ImportError:
            self._playwright_available = False

        try:
            import selenium
            self._selenium_available = True
        except ImportError:
            self._selenium_available = False

        # Create screenshot directory
        Path(self.browse_config.screenshot_dir).mkdir(parents=True, exist_ok=True)

    async def execute(self, intent: Intent, context: Optional[HelixContext]) -> SkillResult:
        """Execute browse skill"""
        start_time = asyncio.get_event_loop().time()

        params = intent.parameters
        url = params.get("url", "")
        action = params.get("action", "navigate")
        screenshot = params.get("screenshot", False)
        headless = params.get("headless", True)

        if not url:
            return SkillResult(
                success=False,
                message="URL is required for browse skill",
                errors=["Missing URL parameter"]
            )

        try:
            if self._playwright_available:
                result = await self._execute_playwright(url, action, screenshot, headless)
            elif self._selenium_available:
                result = await self._execute_selenium(url, action, screenshot, headless)
            else:
                result = await self._execute_http_fallback(url)

            execution_time = int((asyncio.get_event_loop().time() - start_time) * 1000)

            return SkillResult(
                success=result["success"],
                message=result["message"],
                data=result.get("data", {}),
                execution_time_ms=execution_time,
            )

        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Browse failed: {str(e)}",
                errors=[str(e)]
            )

    async def _execute_playwright(
        self, url: str, action: str, screenshot: bool, headless: bool
    ) -> Dict[str, Any]:
        """Execute via Playwright"""
        try:
            from playwright.async_api import async_playwright

            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=headless)
                page = await browser.new_page(
                    viewport={"width": self.browse_config.viewport[0],
                             "height": self.browse_config.viewport[1]}
                )

                # Navigate to URL
                response = await page.goto(url, timeout=self.browse_config.timeout * 1000)

                data = {
                    "url": url,
                    "status": response.status if response else None,
                    "title": await page.title(),
                }

                # Take screenshot if requested
                if screenshot:
                    screenshot_path = Path(self.browse_config.screenshot_dir) / f"screenshot_{int(asyncio.get_event_loop().time()*1000)}.png"
                    await page.screenshot(path=str(screenshot_path), full_page=True)
                    data["screenshot"] = str(screenshot_path)

                await browser.close()

                return {
                    "success": True,
                    "message": f"Successfully browsed {url}" + (", screenshot saved" if screenshot else ""),
                    "data": data
                }

        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "data": {"error": str(e)}
            }

    async def _execute_selenium(
        self, url: str, action: str, screenshot: bool, headless: bool
    ) -> Dict[str, Any]:
        """Execute via Selenium"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options

            options = Options()
            if headless:
                options.add_argument("--headless")
            options.add_argument(f"--window-size={self.browse_config.viewport[0]},{self.browse_config.viewport[1]}")

            driver = webdriver.Chrome(options=options)
            driver.get(url)

            data = {
                "url": url,
                "title": driver.title,
            }

            if screenshot:
                screenshot_path = Path(self.browse_config.screenshot_dir) / f"screenshot_{int(asyncio.get_event_loop().time()*1000)}.png"
                driver.save_screenshot(str(screenshot_path))
                data["screenshot"] = str(screenshot_path)

            driver.quit()

            return {
                "success": True,
                "message": f"Successfully browsed {url}",
                "data": data
            }

        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "data": {"error": str(e)}
            }

    async def _execute_http_fallback(self, url: str) -> Dict[str, Any]:
        """Fallback: basic HTTP request"""
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    content = await response.text()
                    return {
                        "success": True,
                        "message": f"Fetched {url} - Status: {response.status}",
                        "data": {
                            "url": url,
                            "status": response.status,
                            "content_length": len(content),
                            "content_type": response.content_type,
                            "title": "N/A (install playwright or selenium for full browser)"
                        }
                    }
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "data": {"error": str(e)}
            }
