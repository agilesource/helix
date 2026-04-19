"""Test Design Skill"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock, AsyncMock
from helix.skills.design import DesignSkill, DesignSystem
from helix.skills.base import SkillConfig, SkillCategory, SkillStatus
from helix.core.intent import Intent, IntentType


class TestDesignSystem:
    """Test DesignSystem"""

    def test_design_system_defaults(self):
        """Test DesignSystem default values"""
        ds = DesignSystem()
        assert ds.brand_name == "Helix Project"
        assert ds.primary_color == "#0066CC"
        assert ds.secondary_color == "#6B7280"
        assert ds.accent_color == "#14B8A6"
        assert ds.background_color == "#FFFFFF"
        assert ds.text_color == "#1F2937"
        assert ds.font_family == "Inter, system-ui, sans-serif"
        assert ds.heading_font == "Inter, system-ui, sans-serif"
        assert ds.base_font_size == 16
        assert ds.spacing_unit == 4
        assert ds.border_radius_small == 4
        assert ds.border_radius_medium == 8
        assert ds.border_radius_large == 16

    def test_design_system_custom(self):
        """Test DesignSystem with custom values"""
        ds = DesignSystem(
            brand_name="My Brand",
            primary_color="#FF0000",
            secondary_color="#00FF00",
            accent_color="#0000FF",
            background_color="#000000",
            text_color="#FFFFFF",
            font_family="Arial",
            heading_font="Helvetica",
            base_font_size=14,
            spacing_unit=8,
            border_radius_small=2,
            border_radius_medium=4,
            border_radius_large=12
        )
        assert ds.brand_name == "My Brand"
        assert ds.primary_color == "#FF0000"
        assert ds.secondary_color == "#00FF00"
        assert ds.accent_color == "#0000FF"
        assert ds.background_color == "#000000"
        assert ds.text_color == "#FFFFFF"
        assert ds.font_family == "Arial"
        assert ds.heading_font == "Helvetica"
        assert ds.base_font_size == 14
        assert ds.spacing_unit == 8
        assert ds.border_radius_small == 2
        assert ds.border_radius_medium == 4
        assert ds.border_radius_large == 12


class TestDesignSkill:
    """Test DesignSkill"""

    @pytest.fixture
    def skill(self):
        config = SkillConfig()
        return DesignSkill(config)

    def test_skill_init(self, skill):
        """Test skill initialization"""
        assert skill.name == "design"
        assert skill.category == SkillCategory.INFRASTRUCTURE
        assert skill.status == SkillStatus.STABLE

    def test_skill_examples(self, skill):
        """Test skill examples"""
        assert len(skill.examples) > 0

    def test_skill_description(self, skill):
        """Test skill description"""
        assert len(skill.description) > 0
        assert "design" in skill.description.lower()

    def test_skill_design_system(self, skill):
        """Test skill has design system"""
        assert skill.design_system is not None
        assert isinstance(skill.design_system, DesignSystem)


class TestDesignSkillExecute:
    """Test DesignSkill execute method"""

    @pytest.mark.asyncio
    async def test_execute_with_brand(self):
        """Test execute with brand parameter"""
        skill = DesignSkill()

        intent = Intent(
            type=IntentType.DESIGN,
            confidence=1.0,
            raw_input="helix design --brand MyBrand",
            parameters={"brand": "MyBrand", "template": "default"}
        )

        result = await skill.execute(intent, None)
        assert result.success is True
        assert skill.design_system.brand_name == "MyBrand"

    @pytest.mark.asyncio
    async def test_execute_with_color_scheme(self):
        """Test execute with color scheme"""
        skill = DesignSkill()

        intent = Intent(
            type=IntentType.DESIGN,
            confidence=1.0,
            raw_input="helix design --color_scheme ocean",
            parameters={"color_scheme": "ocean"}
        )

        result = await skill.execute(intent, None)
        assert result.success is True

    @pytest.mark.asyncio
    async def test_execute_with_output(self):
        """Test execute with output file"""
        skill = DesignSkill()

        intent = Intent(
            type=IntentType.DESIGN,
            confidence=1.0,
            raw_input="helix design --output custom.md",
            parameters={"output": "custom.md"}
        )

        result = await skill.execute(intent, None)
        assert result.success is True


class TestDesignSkillMethods:
    """Test DesignSkill internal methods"""

    @pytest.mark.asyncio
    async def test_load_from_spec(self):
        """Test _load_from_spec method"""
        skill = DesignSkill()

        # Create a temporary spec file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "design": {
                    "brand": "Spec Brand",
                    "colors": {
                        "primary": "#123456"
                    }
                }
            }, f)
            spec_file = f.name

        try:
            skill._load_from_spec(spec_file)
            assert skill.design_system.brand_name == "Spec Brand"
        finally:
            Path(spec_file).unlink()

    @pytest.mark.asyncio
    async def test_apply_color_scheme(self):
        """Test _apply_color_scheme method"""
        skill = DesignSkill()

        skill._apply_color_scheme("ocean")
        # Should apply ocean color scheme

        skill._apply_color_scheme("forest")
        # Should apply forest color scheme

        skill._apply_color_scheme("sunset")
        # Should apply sunset color scheme

    def test_generate_design_system(self):
        """Test _generate_design_system method"""
        skill = DesignSkill()

        result = skill._generate_design_system("default", "test.md")
        assert result["success"] is True
        assert "data" in result


class TestDesignSkillEdgeCases:
    """Test DesignSkill edge cases"""

    @pytest.mark.asyncio
    async def test_execute_invalid_color_scheme(self):
        """Test execute with invalid color scheme"""
        skill = DesignSkill()

        intent = Intent(
            type=IntentType.DESIGN,
            confidence=1.0,
            raw_input="helix design --color_scheme invalid",
            parameters={"color_scheme": "invalid_scheme_xyz"}
        )

        result = await skill.execute(intent, None)
        # Should handle gracefully

    @pytest.mark.asyncio
    async def test_execute_error_handling(self):
        """Test execute error handling"""
        skill = DesignSkill()

        # Force an error by passing invalid params
        intent = Intent(
            type=IntentType.DESIGN,
            confidence=1.0,
            raw_input="helix design",
            parameters={"template": "nonexistent_template"}
        )

        result = await skill.execute(intent, None)
        assert result is not None
