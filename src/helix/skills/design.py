"""
Helix Design Skill - Design Generation

Helix-native design system generation:
- Spec-driven design generation
- Design system from specification
- Typography, color, layout system
- DESIGN.md creation
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from helix.skills.base import Skill, SkillResult, SkillConfig, SkillCategory, SkillStatus
from helix.core.intent import Intent, IntentType
from helix.core.context import HelixContext


@dataclass
class DesignSystem:
    """Design system specification"""
    brand_name: str = "Helix Project"
    primary_color: str = "#0066CC"
    secondary_color: str = "#6B7280"
    accent_color: str = "#14B8A6"
    background_color: str = "#FFFFFF"
    text_color: str = "#1F2937"
    font_family: str = "Inter, system-ui, sans-serif"
    heading_font: str = "Inter, system-ui, sans-serif"
    base_font_size: int = 16
    spacing_unit: int = 4
    border_radius_small: int = 4
    border_radius_medium: int = 8
    border_radius_large: int = 16


class DesignSkill(Skill):
    """
    Design Skill - Design Generation

    Helix-native design system generation
    """

    name = "design"
    description = "Design generation - design system, typography, color, layout"
    category = SkillCategory.INFRASTRUCTURE
    status = SkillStatus.STABLE

    examples = [
        "helix design --brand 'My Brand'",
        "helix design --template minimal",
        "helix design --output DESIGN.md",
        "helix design --spec spec.json",
    ]

    def __init__(self, config: Optional[SkillConfig] = None):
        super().__init__(config)
        self.design_system = DesignSystem()

    def _do_initialize(self) -> None:
        """Initialize design skill"""
        pass

    async def execute(self, intent: Intent, context: Optional[HelixContext]) -> SkillResult:
        """Execute design skill"""
        import time
        start_time = time.time()

        params = intent.parameters
        brand = params.get("brand", "")
        template = params.get("template", "default")
        output = params.get("output", "DESIGN.md")
        spec_file = params.get("spec", "")
        color_scheme = params.get("color_scheme", "")

        try:
            # Load from spec if provided
            if spec_file and Path(spec_file).exists():
                self._load_from_spec(spec_file)

            # Apply brand override
            if brand:
                self.design_system.brand_name = brand

            # Apply color scheme
            if color_scheme:
                self._apply_color_scheme(color_scheme)

            # Generate design system
            result = self._generate_design_system(template, output)

            execution_time = int((time.time() - start_time) * 1000)

            return SkillResult(
                success=result["success"],
                message=result["message"],
                data=result.get("data", {}),
                execution_time_ms=execution_time,
            )

        except Exception as e:
            return SkillResult(
                success=False,
                message=f"Design failed: {str(e)}",
                errors=[str(e)]
            )

    def _load_from_spec(self, spec_file: str) -> None:
        """Load design preferences from spec file"""
        spec = json.loads(Path(spec_file).read_text())

        # Extract design preferences from spec
        if "design" in spec:
            design = spec["design"]
            if "brand" in design:
                self.design_system.brand_name = design["brand"]
            if "colors" in design:
                colors = design["colors"]
                self.design_system.primary_color = colors.get("primary", self.design_system.primary_color)
                self.design_system.secondary_color = colors.get("secondary", self.design_system.secondary_color)
                self.design_system.accent_color = colors.get("accent", self.design_system.accent_color)
            if "typography" in design:
                typo = design["typography"]
                self.design_system.font_family = typo.get("font", self.design_system.font_family)

    def _apply_color_scheme(self, scheme: str) -> None:
        """Apply predefined color scheme"""
        schemes = {
            "ocean": {
                "primary": "#0EA5E9",
                "secondary": "#64748B",
                "accent": "#06B6D4",
            },
            "forest": {
                "primary": "#059669",
                "secondary": "#6B7280",
                "accent": "#10B981",
            },
            "sunset": {
                "primary": "#EA580C",
                "secondary": "#78716C",
                "accent": "#F59E0B",
            },
            "royal": {
                "primary": "#7C3AED",
                "secondary": "#6B7280",
                "accent": "#8B5CF6",
            },
            "minimal": {
                "primary": "#000000",
                "secondary": "#6B7280",
                "accent": "#2563EB",
            },
        }

        if scheme in schemes:
            colors = schemes[scheme]
            self.design_system.primary_color = colors["primary"]
            self.design_system.secondary_color = colors["secondary"]
            self.design_system.accent_color = colors["accent"]

    def _generate_design_system(self, template: str, output: str) -> Dict[str, Any]:
        """Generate design system based on template"""

        if template == "minimal":
            content = self._generate_minimal_template()
        elif template == "dark":
            content = self._generate_dark_template()
        else:
            content = self._generate_default_template()

        # Write to file
        output_path = Path(output)
        output_path.write_text(content)

        return {
            "success": True,
            "message": f"Design system written to {output}",
            "data": {
                "file": output,
                "path": str(output_path.absolute()),
                "brand": self.design_system.brand_name,
                "template": template
            }
        }

    def _generate_default_template(self) -> str:
        """Generate default design system template"""
        ds = self.design_system

        return f"""# Design System - {ds.brand_name}

> Generated by Project Helix v0.6.0
> Date: {__import__('datetime').datetime.now().isoformat()}

---

## Brand Identity

| Property | Value |
|----------|-------|
| Brand Name | {ds.brand_name} |
| Version | 1.0.0 |

---

## Color Palette

### Primary Colors

| Color Name | Hex | Usage |
|------------|-----|-------|
| Primary | {ds.primary_color} | Main actions, links, highlights |
| Secondary | {ds.secondary_color} | Secondary elements, body text |
| Accent | {ds.accent_color} | CTAs, notifications, focus states |

### Semantic Colors

| Color Name | Hex | Usage |
|------------|-----|-------|
| Success | #10B981 | Success states, positive feedback |
| Warning | #F59E0B | Warning states, caution |
| Error | #EF4444 | Error states, destructive actions |
| Info | #3B82F6 | Information states |

### Neutral Colors

| Name | Hex | Usage |
|------|-----|-------|
| White | {ds.background_color} | Background |
| Gray 50 | #F9FAFB | Light backgrounds |
| Gray 100 | #F3F4F6 | Borders, dividers |
| Gray 200 | #E5E7EB | Disabled states |
| Gray 300 | #D1D5DB | Placeholders |
| Gray 400 | #9CA3AF | Secondary text |
| Gray 500 | #6B7280 | Body text |
| Gray 600 | #4B5563 | Headings |
| Gray 700 | #374151 | Primary headings |
| Gray 800 | #1F2937 | Dark text |
| Gray 900 | #111827 | Darkest text |

---

## Typography

### Font Family

| Element | Font | Fallback |
|---------|------|----------|
| Headings | {ds.heading_font} | system-ui, sans-serif |
| Body | {ds.font_family} | system-ui, sans-serif |
| Code | JetBrains Mono, monospace | monospace |

### Font Sizes

| Name | Size | Line Height | Usage |
|------|------|-------------|-------|
| xs | 12px | 1.5 | Captions, labels |
| sm | 14px | 1.5 | Secondary text |
| base | {ds.base_font_size}px | 1.6 | Body text |
| lg | 18px | 1.6 | Lead text |
| xl | 20px | 1.4 | H4 |
| 2xl | 24px | 1.4 | H3 |
| 3xl | 30px | 1.2 | H2 |
| 4xl | 36px | 1.2 | H1 |
| 5xl | 48px | 1.1 | Hero |

### Font Weights

| Weight | Value | Usage |
|--------|-------|-------|
| Regular | 400 | Body text |
| Medium | 500 | Emphasized body |
| Semibold | 600 | Headings |
| Bold | 700 | Hero, emphasis |

---

## Spacing

Base unit: {ds.spacing_unit}px

| Name | Value | Usage |
|------|-------|-------|
| 0 | 0 | No spacing |
| 1 | {ds.spacing_unit}px | Tight spacing |
| 2 | {ds.spacing_unit * 2}px | Default spacing |
| 3 | {ds.spacing_unit * 3}px | Section spacing |
| 4 | {ds.spacing_unit * 4}px | Large gaps |
| 6 | {ds.spacing_unit * 6}px | Section breaks |
| 8 | {ds.spacing_unit * 8}px | Major sections |
| 12 | {ds.spacing_unit * 12}px | Page margins |

---

## Border Radius

| Name | Value | Usage |
|------|-------|-------|
| none | 0 | No radius |
| sm | {ds.border_radius_small}px | Inputs, small buttons |
| md | {ds.border_radius_medium}px | Cards, containers |
| lg | {ds.border_radius_large}px | Modals, large elements |
| full | 9999px | Pills, avatars |

---

## Shadows

| Name | Value | Usage |
|------|-------|-------|
| sm | 0 1px 2px rgba(0,0,0,0.05) | Subtle elevation |
| md | 0 4px 6px rgba(0,0,0,0.1) | Cards |
| lg | 0 10px 15px rgba(0,0,0,0.1) | Modals, dropdowns |
| xl | 0 20px 25px rgba(0,0,0,0.15) | Overlays |

---

## Components

### Buttons

```
Primary:   background: {ds.primary_color}, color: white, border-radius: {ds.border_radius_small}px
Secondary: background: transparent, color: {ds.primary_color}, border: 1px solid {ds.primary_color}
Ghost:     background: transparent, color: {ds.primary_color}
```

### Inputs

```
Background: {ds.background_color}
Border: 1px solid #E5E7EB
Focus: border-color: {ds.primary_color}, box-shadow: 0 0 0 3px {ds.primary_color}20
```

### Cards

```
Background: {ds.background_color}
Border: 1px solid #E5E7EB
Border-radius: {ds.border_radius_medium}px
Shadow: md
Padding: 24px
```

---

## Responsive Breakpoints

| Name | Width | Target |
|------|-------|--------|
| sm | 640px | Mobile landscape |
| md | 768px | Tablets |
| lg | 1024px | Laptops |
| xl | 1280px | Desktops |
| 2xl | 1536px | Large screens |

---

*Generated by Helix Design Skill - AI Era Software Engineering*
"""

    def _generate_minimal_template(self) -> str:
        """Generate minimal design template"""
        ds = self.design_system
        return f"""# Design System - {ds.brand_name} (Minimal)

> Generated by Project Helix v0.6.0

## Colors
- Primary: {ds.primary_color}
- Secondary: {ds.secondary_color}

## Typography
- Font: {ds.font_family}
- Base size: {ds.base_font_size}px

## Spacing
- Unit: {ds.spacing_unit}px

## Radius
- Small: {ds.border_radius_small}px
- Medium: {ds.border_radius_medium}px
"""

    def _generate_dark_template(self) -> str:
        """Generate dark mode design template"""
        ds = self.design_system
        return f"""# Design System - {ds.brand_name} (Dark)

> Generated by Project Helix v0.6.0

## Colors (Dark Mode)
- Background: #0F172A
- Surface: #1E293B
- Primary: {ds.primary_color}
- Text: #F8FAFC
- Muted: #94A3B8
"""
