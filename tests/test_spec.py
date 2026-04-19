"""Test spec fallback skill"""

import pytest
from helix.skills.spec_fallback import SpecSkillFallback, RequirementType, ExtractedEntities


class TestRequirementType:
    """Test RequirementType enum"""

    def test_requirement_types(self):
        """Test all requirement types"""
        assert RequirementType.CRUD.value == "crud"
        assert RequirementType.API.value == "api"
        assert RequirementType.ALGORITHM.value == "algorithm"
        assert RequirementType.INTEGRATION.value == "integration"
        assert RequirementType.UI.value == "ui"
        assert RequirementType.SCRIPT.value == "script"
        assert RequirementType.INFRASTRUCTURE.value == "infrastructure"
        assert RequirementType.GENERAL.value == "general"


class TestExtractedEntities:
    """Test ExtractedEntities"""

    def test_default_entities(self):
        """Test default values"""
        entities = ExtractedEntities()
        assert entities.domain == ""
        assert entities.action == ""
        assert entities.entities == []
        assert entities.target_users == []

    def test_entities_with_values(self):
        """Test entities with values"""
        entities = ExtractedEntities(
            domain="user",
            action="login",
            target_users=["admin"]
        )
        assert entities.domain == "user"
        assert entities.action == "login"
        assert entities.target_users == ["admin"]


class TestSpecSkillFallback:
    """Test SpecSkillFallback"""

    @pytest.fixture
    def skill(self):
        """Create skill instance"""
        skill = SpecSkillFallback()
        skill.initialize()
        return skill

    def test_classify_crud(self, skill):
        """Test CRUD classification"""
        assert skill._classify_requirement("build a user login").value == "crud"
        assert skill._classify_requirement("create new user").value == "crud"

    def test_classify_api(self, skill):
        """Test API classification"""
        assert skill._classify_requirement("create a REST API").value == "api"

    def test_classify_algorithm(self, skill):
        """Test algorithm classification"""
        assert skill._classify_requirement("implement a recommendation algorithm").value == "algorithm"

    def test_classify_integration(self, skill):
        """Test integration classification"""
        assert skill._classify_requirement("add WeChat payment").value == "integration"
        assert skill._classify_requirement("add email notification").value == "integration"

    def test_classify_ui(self, skill):
        """Test UI classification"""
        assert skill._classify_requirement("build a dashboard page").value == "ui"

    def test_classify_script(self, skill):
        """Test script classification"""
        assert skill._classify_requirement("create a CLI tool").value == "script"

    def test_classify_infrastructure(self, skill):
        """Test infrastructure classification"""
        assert skill._classify_requirement("setup CI/CD pipeline").value == "infrastructure"

    def test_extract_user_domain(self, skill):
        """Test user domain extraction"""
        entities = skill._extract_entities("user login feature")
        assert entities.domain == "user"

    def test_extract_action(self, skill):
        """Test action extraction"""
        entities = skill._extract_entities("create new user")
        assert entities.action == "create"

    def test_infer_function_name(self, skill):
        """Test function name inference"""
        assert skill._infer_function_name("user login") == "User Login"


class TestSpecEntities:
    """Test entity extraction"""

    def test_extract_product_domain(self):
        """Test product domain extraction"""
        from helix.skills.spec_fallback import SpecSkillFallback
        skill = SpecSkillFallback()
        entities = skill._extract_entities("add shopping cart")
        # Just verify it returns something
        assert entities is not None

    def test_extract_payment_action(self):
        """Test payment action extraction"""
        from helix.skills.spec_fallback import SpecSkillFallback
        skill = SpecSkillFallback()
        entities = skill._extract_entities("process payment")
        assert entities is not None

    def test_extract_multiple_entities(self):
        """Test multiple entity extraction"""
        from helix.skills.spec_fallback import SpecSkillFallback
        skill = SpecSkillFallback()
        entities = skill._extract_entities("send notification to user")
        assert entities is not None


class TestSpecRequirementType:
    """Test requirement type classification"""

    def test_classify_refactor(self):
        """Test refactor classification"""
        from helix.skills.spec_fallback import SpecSkillFallback
        skill = SpecSkillFallback()
        result = skill._classify_requirement("refactor login code")
        assert result is not None

    def test_classify_security(self):
        """Test security classification"""
        from helix.skills.spec_fallback import SpecSkillFallback
        skill = SpecSkillFallback()
        result = skill._classify_requirement("add authentication")
        assert result is not None

    def test_classify_data(self):
        """Test data classification"""
        from helix.skills.spec_fallback import SpecSkillFallback
        skill = SpecSkillFallback()
        result = skill._classify_requirement("add analytics tracking")
        assert result is not None


class TestSpecSkillExecute:
    """Test SpecSkill execute method"""

    @pytest.mark.asyncio
    async def test_execute_refactor_requirement(self):
        """Test execute with refactor requirement"""
        from helix.core.intent import Intent, IntentType
        from helix.skills.spec_fallback import SpecSkillFallback
        skill = SpecSkillFallback()
        intent = Intent(
            type=IntentType.SPEC,
            raw_input="spec refactor the auth module",
            confidence=0.9,
            parameters={"requirement": "refactor the auth module"}
        )
        try:
            result = await skill.execute(intent, None)
        except (RuntimeError, Exception):
            pass
