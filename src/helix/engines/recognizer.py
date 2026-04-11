"""
Helix Intent Recognition Engine

Natural language → Skill routing:
- Pattern-based intent detection
- Keyword matching
- Confidence scoring
- Learning from user corrections
"""

import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

from helix.core.intent import Intent, IntentType


class IntentSource(Enum):
    """Intent recognition source"""
    PATTERN = "pattern"
    KEYWORD = "keyword"
    EXPLICIT = "explicit"
    LEARNED = "learned"


@dataclass
class IntentPattern:
    """Intent pattern"""
    intent_type: IntentType
    patterns: List[str]  # Regex patterns
    keywords: List[str]  # Simple keywords
    weight: float = 1.0


@dataclass
class RecognitionResult:
    """Recognition result"""
    intent: Intent
    confidence: float
    source: IntentSource
    alternatives: List[Tuple[IntentType, float]] = field(default_factory=list)


class IntentRecognizer:
    """
    Intent Recognition Engine

    Converts natural language to structured Intent
    """

    def __init__(self):
        self._patterns: List[IntentPattern] = []
        self._learned_patterns: Dict[str, IntentType] = {}
        self._initialize_default_patterns()

    def _initialize_default_patterns(self) -> None:
        """Initialize default intent patterns"""

        # Execution layer
        self._patterns.extend([
            IntentPattern(
                IntentType.SPEC,
                patterns=[r"(?:create|write|generate)\s+(?:a\s+)?spec", r"requirement.*spec"],
                keywords=["spec", "specification", "需求", "规格"],
                weight=1.0
            ),
            IntentPattern(
                IntentType.BUILD,
                patterns=[r"build", r"implement", r"code", r"写代码"],
                keywords=["build", "implement", "代码", "开发"],
                weight=0.8
            ),
            IntentPattern(
                IntentType.VERIFY,
                patterns=[r"verify", r"test", r"check", r"验证"],
                keywords=["verify", "test", "测试", "检查", "验证"],
                weight=1.0
            ),
            IntentPattern(
                IntentType.SHIP,
                patterns=[r"ship", r"deploy", r"release", r"push.*pr", r"merge"],
                keywords=["ship", "deploy", "release", "发布", "部署", "推送", "合并"],
                weight=1.0
            ),
        ])

        # Quality layer
        self._patterns.extend([
            IntentPattern(
                IntentType.REVIEW,
                patterns=[r"review", r"code.*review", r"pr.*review", r"代码审查"],
                keywords=["review", "审查", "review"],
                weight=1.0
            ),
            IntentPattern(
                IntentType.TEST,
                patterns=[r"test", r"qa", r"testing", r"测试"],
                keywords=["test", "qa", "测试"],
                weight=0.9
            ),
            IntentPattern(
                IntentType.AUDIT,
                patterns=[r"audit", r"security", r"vulnerability", r"安全审计"],
                keywords=["audit", "security", "安全", "审计"],
                weight=1.0
            ),
            IntentPattern(
                IntentType.GATE,
                patterns=[r"gate", r"quality.*gate", r"门禁"],
                keywords=["gate", "quality", "质量门禁"],
                weight=1.0
            ),
        ])

        # Infrastructure layer
        self._patterns.extend([
            IntentPattern(
                IntentType.BROWSE,
                patterns=[r"browse", r"open.*url", r"visit", r"浏览器"],
                keywords=["browse", "open", "访问", "浏览器"],
                weight=1.0
            ),
            IntentPattern(
                IntentType.DESIGN,
                patterns=[r"design", r"design.*system", r"设计系统"],
                keywords=["design", "设计", "样式"],
                weight=1.0
            ),
            IntentPattern(
                IntentType.LEARN,
                patterns=[r"learn", r"learning", r"knowledge", r"学习"],
                keywords=["learn", "learning", "学习", "知识"],
                weight=1.0
            ),
            IntentPattern(
                IntentType.CHECKPOINT,
                patterns=[r"checkpoint", r"save.*state", r"resume", r"检查点"],
                keywords=["checkpoint", "save", "resume", "保存", "恢复"],
                weight=1.0
            ),
        ])

    def recognize(self, input_text: str) -> RecognitionResult:
        """Recognize intent from input text"""
        input_lower = input_text.lower().strip()

        # Check for explicit skill invocation (e.g., /spec, /build)
        explicit_intent = self._check_explicit(input_text)
        if explicit_intent:
            return RecognitionResult(
                intent=explicit_intent,
                confidence=1.0,
                source=IntentSource.EXPLICIT
            )

        # Check learned patterns first
        learned_intent = self._check_learned(input_lower)
        if learned_intent:
            return RecognitionResult(
                intent=learned_intent,
                confidence=0.9,
                source=IntentSource.LEARNED
            )

        # Pattern matching
        scores: Dict[IntentType, float] = {}
        for pattern in self._patterns:
            score = self._match_pattern(pattern, input_lower)
            if score > 0:
                scores[pattern.intent_type] = max(
                    scores.get(pattern.intent_type, 0),
                    score * pattern.weight
                )

        if not scores:
            # Default to general
            return RecognitionResult(
                intent=Intent(
                    type=IntentType.GENERAL,
                    raw_input=input_text,
                    confidence=0.5
                ),
                confidence=0.5,
                source=IntentSource.KEYWORD
            )

        # Sort by score
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        best_intent_type, best_score = sorted_scores[0]

        # Build alternatives
        alternatives = [
            (intent_type, score)
            for intent_type, score in sorted_scores[1:3]
        ]

        return RecognitionResult(
            intent=Intent(
                type=best_intent_type,
                raw_input=input_text,
                confidence=min(best_score, 1.0)
            ),
            confidence=min(best_score, 1.0),
            source=IntentSource.PATTERN,
            alternatives=alternatives
        )

    def _check_explicit(self, input_text: str) -> Optional[Intent]:
        """Check for explicit skill invocation"""
        # Remove leading slash if present
        text = input_text.strip()
        if text.startswith("/"):
            text = text[1:]

        # Map to intent type
        mapping = {
            "spec": IntentType.SPEC,
            "build": IntentType.BUILD,
            "verify": IntentType.VERIFY,
            "ship": IntentType.SHIP,
            "review": IntentType.REVIEW,
            "test": IntentType.TEST,
            "qa": IntentType.TEST,
            "audit": IntentType.AUDIT,
            "gate": IntentType.GATE,
            "browse": IntentType.BROWSE,
            "design": IntentType.DESIGN,
            "learn": IntentType.LEARN,
            "checkpoint": IntentType.CHECKPOINT,
        }

        intent_type = mapping.get(text.lower())
        if intent_type:
            return Intent(
                type=intent_type,
                raw_input=input_text,
                confidence=1.0
            )

        return None

    def _check_learned(self, input_text: str) -> Optional[Intent]:
        """Check learned patterns"""
        for pattern, intent_type in self._learned_patterns.items():
            if pattern in input_text:
                return Intent(
                    type=intent_type,
                    raw_input=input_text,
                    confidence=0.9
                )
        return None

    def _match_pattern(self, pattern: IntentPattern, text: str) -> float:
        """Match pattern against text"""
        score = 0.0

        # Regex patterns
        for p in pattern.patterns:
            if re.search(p, text, re.IGNORECASE):
                score = max(score, 1.0)
                break

        # Keywords
        if score == 0:
            for kw in pattern.keywords:
                if kw.lower() in text:
                    score = max(score, 0.7)
                    break

        return score

    def learn(self, input_text: str, intent_type: IntentType) -> None:
        """Learn from user correction"""
        # Extract key pattern (simple: first significant word)
        words = re.findall(r'\w+', input_text.lower())
        if words:
            # Use first 2-3 words as pattern
            pattern = ' '.join(words[:2])
            self._learned_patterns[pattern] = intent_type

    def get_suggestions(self, partial_input: str) -> List[str]:
        """Get skill suggestions based on partial input"""
        suggestions = []

        # Get all keywords
        all_keywords = []
        for pattern in self._patterns:
            all_keywords.extend(pattern.keywords)

        # Filter by partial match
        partial = partial_input.lower()
        for kw in all_keywords:
            if kw.startswith(partial):
                suggestions.append(f"/{kw}")

        return list(set(suggestions))[:5]


# Global instance
_recognizer: Optional[IntentRecognizer] = None


def get_recognizer() -> IntentRecognizer:
    """Get global intent recognizer"""
    global _recognizer
    if _recognizer is None:
        _recognizer = IntentRecognizer()
    return _recognizer
