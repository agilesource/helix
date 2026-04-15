"""Test Engines - Recognizer"""

import pytest
from helix.engines.recognizer import (
    IntentRecognizer,
    IntentSource,
    IntentPattern,
    get_recognizer,
)
from helix.core.intent import IntentType


class TestIntentRecognizer:
    """Test IntentRecognizer"""

    @pytest.fixture
    def recognizer(self):
        return IntentRecognizer()

    def test_recognizer_init(self, recognizer):
        """Test recognizer initialization"""
        assert recognizer is not None
        assert hasattr(recognizer, '_patterns')

    def test_recognizer_default_patterns(self, recognizer):
        """Test default patterns are loaded"""
        # Should have some default patterns (list of IntentPattern)
        assert isinstance(recognizer._patterns, list)
        assert len(recognizer._patterns) > 0

    def test_recognize_explicit_spec(self, recognizer):
        """Test explicit /spec invocation"""
        result = recognizer.recognize("/spec")
        assert result.intent.type == IntentType.SPEC
        assert result.confidence == 1.0
        assert result.source == IntentSource.EXPLICIT

    def test_recognize_explicit_build(self, recognizer):
        """Test explicit /build invocation"""
        result = recognizer.recognize("/build")
        assert result.intent.type == IntentType.BUILD
        assert result.confidence == 1.0

    def test_recognize_explicit_ship(self, recognizer):
        """Test explicit /ship invocation"""
        result = recognizer.recognize("/ship")
        assert result.intent.type == IntentType.SHIP

    def test_recognize_pattern_build(self, recognizer):
        """Test pattern matching for build"""
        result = recognizer.recognize("build the project")
        assert result.intent.type == IntentType.BUILD
        assert result.confidence > 0

    def test_recognize_keyword_verify(self, recognizer):
        """Test keyword matching for verify"""
        result = recognizer.recognize("run tests")
        assert result.intent.type == IntentType.VERIFY

    def test_recognize_audit(self, recognizer):
        """Test audit intent recognition"""
        result = recognizer.recognize("security audit")
        assert result.intent.type == IntentType.AUDIT

    def test_recognize_design(self, recognizer):
        """Test design intent recognition"""
        result = recognizer.recognize("create a design")
        assert result.intent.type == IntentType.DESIGN

    def test_recognize_learn(self, recognizer):
        """Test learn intent recognition"""
        result = recognizer.recognize("learn from this")
        assert result.intent.type == IntentType.LEARN

    def test_recognize_checkpoint(self, recognizer):
        """Test checkpoint intent recognition"""
        result = recognizer.recognize("/checkpoint")
        assert result.intent.type == IntentType.CHECKPOINT

    def test_recognize_unknown_returns_general(self, recognizer):
        """Test unknown input returns general intent"""
        result = recognizer.recognize("random text xyz")
        assert result.intent.type == IntentType.GENERAL

    def test_recognize_chinese(self, recognizer):
        """Test Chinese input recognition"""
        result = recognizer.recognize("写代码")
        assert result.intent.type == IntentType.BUILD

    def test_recognizer_learn(self, recognizer):
        """Test learning from user correction"""
        recognizer.learn("fix authentication", IntentType.BUILD)
        assert "fix authentication" in recognizer._learned_patterns
        assert recognizer._learned_patterns["fix authentication"] == IntentType.BUILD

    def test_recognizer_get_suggestions(self, recognizer):
        """Test skill suggestions"""
        suggestions = recognizer.get_suggestions("bu")
        assert len(suggestions) > 0
        assert any("build" in s for s in suggestions)

    def test_recognizer_empty_input(self, recognizer):
        """Test empty input handling"""
        result = recognizer.recognize("")
        assert result is not None


class TestIntentSource:
    """Test IntentSource enum"""

    def test_intent_source_values(self):
        """Test IntentSource values"""
        assert IntentSource.PATTERN.value == "pattern"
        assert IntentSource.KEYWORD.value == "keyword"
        assert IntentSource.EXPLICIT.value == "explicit"
        assert IntentSource.LEARNED.value == "learned"


class TestIntentPattern:
    """Test IntentPattern dataclass"""

    def test_intent_pattern_creation(self):
        """Test IntentPattern creation"""
        pattern = IntentPattern(
            intent_type=IntentType.BUILD,
            patterns=[r"build"],
            keywords=["build"]
        )
        assert pattern.intent_type == IntentType.BUILD
        assert pattern.patterns == [r"build"]
        assert pattern.keywords == ["build"]
        assert pattern.weight == 1.0

    def test_intent_pattern_custom_weight(self):
        """Test IntentPattern with custom weight"""
        pattern = IntentPattern(
            intent_type=IntentType.BUILD,
            patterns=[r"build"],
            keywords=["build"],
            weight=0.5
        )
        assert pattern.weight == 0.5


class TestGetRecognizer:
    """Test get_recognizer factory"""

    def test_get_recognizer_singleton(self):
        """Test recognizer is a singleton"""
        r1 = get_recognizer()
        r2 = get_recognizer()
        assert r1 is r2