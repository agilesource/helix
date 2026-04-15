"""Test Spec Skill"""

import pytest
from helix.skills.spec import (
    SpecSkill,
    RequirementType,
    ExtractedEntities,
    SPEC_SYSTEM_PROMPT,
    SPEC_GENERATION_PROMPT,
)


class TestRequirementType:
    """Test RequirementType enum"""

    def test_requirement_type_values(self):
        """Test all requirement type values"""
        assert RequirementType.CRUD.value == "crud"
        assert RequirementType.API.value == "api"
        assert RequirementType.ALGORITHM.value == "algorithm"
        assert RequirementType.INTEGRATION.value == "integration"
        assert RequirementType.UI.value == "ui"
        assert RequirementType.SCRIPT.value == "script"
        assert RequirementType.INFRASTRUCTURE.value == "infrastructure"
        assert RequirementType.GENERAL.value == "general"


class TestExtractedEntities:
    """Test ExtractedEntities dataclass"""

    def test_extracted_entities_defaults(self):
        """Test default values"""
        entities = ExtractedEntities()
        assert entities.domain == ""
        assert entities.action == ""
        assert entities.entities == []
        assert entities.integrations == []
        assert entities.constraints == []

    def test_extracted_entities_custom(self):
        """Test with custom values"""
        entities = ExtractedEntities(
            domain="e-commerce",
            action="create_order",
            entities=["User", "Product", "Order"],
            integrations=["Payment Gateway", "Email Service"],
            constraints=["max 1000 orders/day"],
            target_users=["customer", "admin"],
            value_proposition="Fast checkout",
            features=["cart", "checkout", "payment"],
            project_context="Online store"
        )
        assert entities.domain == "e-commerce"
        assert entities.action == "create_order"
        assert len(entities.entities) == 3
        assert len(entities.integrations) == 2


class TestSpecSkill:
    """Test SpecSkill"""

    def test_skill_init(self):
        """Test skill initialization"""
        skill = SpecSkill()
        assert skill.name == "spec"
        assert skill.description != ""
        assert skill.category.value == "execution"

    def test_skill_examples(self):
        """Test skill examples"""
        skill = SpecSkill()
        assert len(skill.examples) > 0

    def test_spec_prompts_exist(self):
        """Test that prompt templates exist"""
        assert SPEC_SYSTEM_PROMPT != ""
        assert SPEC_GENERATION_PROMPT != ""
        assert "{requirement}" in SPEC_GENERATION_PROMPT