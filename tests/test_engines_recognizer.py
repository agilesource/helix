"""Test Engines - Recognizer"""

import pytest
from helix.engines.recognizer import IntentRecognizer


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