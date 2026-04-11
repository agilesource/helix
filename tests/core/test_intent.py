"""Tests for Intent Recognition"""

import pytest
from helix.core.intent import Intent, IntentType


class TestIntentType:
    """Test IntentType enum"""

    def test_intent_type_values(self):
        """Test all IntentType values"""
        assert IntentType.SPEC.value == "spec"
        assert IntentType.BUILD.value == "build"
        assert IntentType.VERIFY.value == "verify"
        assert IntentType.SHIP.value == "ship"
        assert IntentType.REVIEW.value == "review"
        assert IntentType.TEST.value == "test"
        assert IntentType.AUDIT.value == "audit"
        assert IntentType.GATE.value == "gate"
        assert IntentType.BROWSE.value == "browse"
        assert IntentType.DESIGN.value == "design"
        assert IntentType.LEARN.value == "learn"
        assert IntentType.CHECKPOINT.value == "checkpoint"
        assert IntentType.GENERAL.value == "general"
        assert IntentType.HELP.value == "help"

    def test_intent_type_execution_layer(self):
        """Test execution layer intents"""
        execution_intents = [IntentType.SPEC, IntentType.BUILD, IntentType.VERIFY, IntentType.SHIP]
        for intent in execution_intents:
            assert intent.value in ["spec", "build", "verify", "ship"]

    def test_intent_type_quality_layer(self):
        """Test quality layer intents"""
        quality_intents = [IntentType.REVIEW, IntentType.TEST, IntentType.AUDIT, IntentType.GATE]
        for intent in quality_intents:
            assert intent.value in ["review", "test", "audit", "gate"]

    def test_intent_type_infrastructure_layer(self):
        """Test infrastructure layer intents"""
        infra_intents = [IntentType.BROWSE, IntentType.DESIGN, IntentType.LEARN, IntentType.CHECKPOINT]
        for intent in infra_intents:
            assert intent.value in ["browse", "design", "learn", "checkpoint"]


class TestIntent:
    """Test Intent dataclass"""

    def test_intent_creation(self):
        """Test basic intent creation"""
        intent = Intent(
            type=IntentType.BUILD,
            raw_input="Build a login feature",
            confidence=0.9,
        )
        assert intent.type == IntentType.BUILD
        assert intent.raw_input == "Build a login feature"
        assert intent.confidence == 0.9
        assert intent.entities == {}
        assert intent.parameters == {}

    def test_intent_with_entities(self):
        """Test intent with entities"""
        intent = Intent(
            type=IntentType.SPEC,
            raw_input="Create API spec",
            confidence=0.85,
            entities={"endpoint": "/api/users", "method": "GET"},
        )
        assert intent.entities["endpoint"] == "/api/users"
        assert intent.entities["method"] == "GET"

    def test_intent_with_parameters(self):
        """Test intent with parameters"""
        intent = Intent(
            type=IntentType.VERIFY,
            raw_input="Verify the code",
            confidence=0.95,
            parameters={"strict": True, "coverage": 80},
        )
        assert intent.parameters["strict"] is True
        assert intent.parameters["coverage"] == 80

    def test_confidence_validation(self):
        """Test confidence validation"""
        # Valid confidence values
        Intent(type=IntentType.BUILD, raw_input="test", confidence=0.0)
        Intent(type=IntentType.BUILD, raw_input="test", confidence=1.0)
        Intent(type=IntentType.BUILD, raw_input="test", confidence=0.5)

        # Invalid confidence - too high
        with pytest.raises(ValueError):
            Intent(type=IntentType.BUILD, raw_input="test", confidence=1.5)

        # Invalid confidence - negative
        with pytest.raises(ValueError):
            Intent(type=IntentType.BUILD, raw_input="test", confidence=-0.1)

    def test_is_clear_property(self):
        """Test is_clear property"""
        # High confidence - clear
        intent = Intent(type=IntentType.BUILD, raw_input="test", confidence=0.9)
        assert intent.is_clear is True

        # Boundary - exactly 0.7
        intent = Intent(type=IntentType.BUILD, raw_input="test", confidence=0.7)
        assert intent.is_clear is True

        # Below threshold - not clear
        intent = Intent(type=IntentType.BUILD, raw_input="test", confidence=0.5)
        assert intent.is_clear is False

        # Low confidence
        intent = Intent(type=IntentType.BUILD, raw_input="test", confidence=0.3)
        assert intent.is_clear is False

    def test_add_entity(self):
        """Test add_entity method"""
        intent = Intent(type=IntentType.BUILD, raw_input="test", confidence=0.9)
        intent.add_entity("feature", "login")
        intent.add_entity("priority", "high")

        assert intent.entities["feature"] == "login"
        assert intent.entities["priority"] == "high"

    def test_set_parameter(self):
        """Test set_parameter method"""
        intent = Intent(type=IntentType.VERIFY, raw_input="test", confidence=0.9)
        intent.set_parameter("coverage", 80)
        intent.set_parameter("strict", True)

        assert intent.parameters["coverage"] == 80
        assert intent.parameters["strict"] is True

    def test_optional_fields(self):
        """Test optional fields"""
        intent = Intent(
            type=IntentType.DESIGN,
            raw_input="Design a dashboard",
            confidence=0.8,
            context_window="dashboard-v1",
            related_intents=["spec", "build"],
        )
        assert intent.context_window == "dashboard-v1"
        assert "spec" in intent.related_intents
        assert "build" in intent.related_intents
