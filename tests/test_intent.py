"""Test Intent Module"""

import pytest
from helix.core.intent import IntentType, Intent


class TestIntentType:
    """Test IntentType enum"""

    def test_intent_type_values(self):
        """Test IntentType enum values"""
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


class TestIntent:
    """Test Intent dataclass"""

    def test_intent_creation(self):
        """Test Intent creation"""
        intent = Intent(
            type=IntentType.BUILD,
            raw_input="build the project",
            confidence=0.9
        )
        assert intent.type == IntentType.BUILD
        assert intent.raw_input == "build the project"
        assert intent.confidence == 0.9
        assert intent.entities == {}
        assert intent.parameters == {}
        assert intent.context_window is None

    def test_intent_with_entities(self):
        """Test Intent with entities"""
        intent = Intent(
            type=IntentType.BUILD,
            raw_input="build the project",
            confidence=0.8,
            entities={"project": "myapp", "target": "prod"},
            parameters={"force": True}
        )
        assert intent.entities == {"project": "myapp", "target": "prod"}
        assert intent.parameters == {"force": True}

    def test_intent_confidence_validation(self):
        """Test confidence validation"""
        with pytest.raises(ValueError):
            Intent(type=IntentType.BUILD, raw_input="test", confidence=1.5)

        with pytest.raises(ValueError):
            Intent(type=IntentType.BUILD, raw_input="test", confidence=-0.1)

    def test_intent_is_clear(self):
        """Test is_clear property"""
        intent_clear = Intent(type=IntentType.BUILD, raw_input="test", confidence=0.8)
        assert intent_clear.is_clear is True

        intent_unclear = Intent(type=IntentType.BUILD, raw_input="test", confidence=0.5)
        assert intent_unclear.is_clear is False

        intent_boundary = Intent(type=IntentType.BUILD, raw_input="test", confidence=0.7)
        assert intent_boundary.is_clear is True

    def test_intent_add_entity(self):
        """Test adding entity"""
        intent = Intent(type=IntentType.BUILD, raw_input="test", confidence=0.8)
        intent.add_entity("framework", "fastapi")
        assert intent.entities["framework"] == "fastapi"

    def test_intent_set_parameter(self):
        """Test setting parameter"""
        intent = Intent(type=IntentType.BUILD, raw_input="test", confidence=0.8)
        intent.set_parameter("verbose", True)
        assert intent.parameters["verbose"] is True
