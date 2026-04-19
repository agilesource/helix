"""
Helix Intent Classifier Module

Intent classification with rule-based matching and optional LLM fallback.
"""

import re
from typing import Dict, List, Optional

from helix.core.intent import Intent, IntentType
from helix.core.context import HelixContext


class IntentClassifier:
    """
    Intent classifier with rule-based matching and context awareness.

    Usage:
        classifier = IntentClassifier()
        intent = await classifier.classify("帮我写一个登录功能", context)
    """

    # Intent patterns for rule-based matching
    PATTERNS: Dict[IntentType, List[str]] = {
        IntentType.SPEC: [
            r"需求", r"spec", r"规格", r"想要.*功能",
            r"设计.*功能", r"我要.*功能", r"创建一个",
            r"开发.*功能", r"需要.*功能"  # Added
        ],
        IntentType.BUILD: [
            r"实现", r"开发", r"写代码", r"build",
            r"编写", r"代码", r"实现.*功能",
            r"帮我写"  # Added
        ],
        IntentType.VERIFY: [
            r"测试", r"验证", r"检查", r"verify",
            r"检验", r"跑.*测试", r"单元测试",
            r"验证.*代码"  # Added
        ],
        IntentType.SHIP: [
            r"发布", r"部署", r"ship", r"上线",
            r"发布.*版本", r"部署.*环境"
        ],
        IntentType.REVIEW: [
            r"review", r"审查", r"代码审查",
            r"review.*代码", r"帮我.*review"
        ],
        IntentType.TEST: [
            r"测试", r"写.*测试", r"测试.*生成",
            r"单元测试", r"集成测试"
        ],
        IntentType.AUDIT: [
            r"审计", r"audit", r"安全.*检查",
            r"漏洞.*扫描", r"依赖.*检查"
        ],
        IntentType.GATE: [
            r"gate", r"门禁", r"质量.*检查",
            r"合并.*检查", r"pr.*检查"
        ],
        IntentType.BROWSE: [
            r"browse", r"浏览器", r"打开.*网页",
            r"访问", r"截图"
        ],
        IntentType.DESIGN: [
            r"design", r"设计", r"生成.*界面",
            r"ui", r"页面.*设计"
        ],
        IntentType.LEARN: [
            r"learn", r"学习", r"记住",
            r"记录", r"知识.*添加"
        ],
        IntentType.CHECKPOINT: [
            r"checkpoint", r"保存.*状态", r"保存.*进度",
            r"继续.*工作", r"恢复.*状态"
        ],
        IntentType.HELP: [
            r"help", r"帮助", r"怎么.*做",
            r"使用.*方法", r"命令.*帮助"
        ],
    }

    # Context window size
    DEFAULT_CONTEXT_WINDOW = 5

    # Confidence threshold for rule-based matching
    RULE_CONFIDENCE = 0.8
    LLM_FALLBACK_THRESHOLD = 0.7

    def __init__(self, context_window: int = DEFAULT_CONTEXT_WINDOW):
        """
        Initialize intent classifier.

        Args:
            context_window: Number of recent intents to consider for context
        """
        self._context_window = context_window
        self._compiled_patterns: Dict[IntentType, List[re.Pattern]] = {}
        self._compile_patterns()

    def _compile_patterns(self) -> None:
        """Compile regex patterns for efficiency."""
        for intent_type, patterns in self.PATTERNS.items():
            self._compiled_patterns[intent_type] = [
                re.compile(p, re.IGNORECASE) for p in patterns
            ]

    async def classify(
        self,
        user_input: str,
        context: Optional[HelixContext] = None
    ) -> Intent:
        """
        Classify user input into intent.

        Args:
            user_input: Raw user input
            context: Optional HelixContext for context-aware classification

        Returns:
            Intent object with type and confidence
        """
        # Step 1: Rule-based classification
        intent = self._rule_based_classify(user_input)

        # Step 2: Context enhancement
        if context:
            intent = self._enhance_with_context(intent, context)

        # Step 3: Calculate confidence
        intent.confidence = self._calculate_confidence(intent)

        return intent

    def _rule_based_classify(self, user_input: str) -> Intent:
        """
        Rule-based intent classification.

        Args:
            user_input: Raw user input

        Returns:
            Intent with matched type
        """
        scores: Dict[IntentType, float] = {}

        # Check each intent type's patterns
        for intent_type, compiled_patterns in self._compiled_patterns.items():
            score = 0.0
            for pattern in compiled_patterns:
                if pattern.search(user_input):
                    score += 1.0

            if score > 0:
                scores[intent_type] = score

        # Find best match
        if not scores:
            # Default to GENERAL if no match
            return Intent(
                type=IntentType.GENERAL,
                raw_input=user_input,
                confidence=0.5
            )

        # Get highest scoring intent type
        best_type = max(scores, key=lambda k: scores[k])
        best_score = scores[best_type]

        # Normalize confidence based on number of matches
        num_patterns = len(self._compiled_patterns[best_type])
        confidence = min(self.RULE_CONFIDENCE, best_score / num_patterns * 2)

        return Intent(
            type=best_type,
            raw_input=user_input,
            confidence=confidence
        )

    def _enhance_with_context(
        self,
        intent: Intent,
        context: HelixContext
    ) -> Intent:
        """
        Enhance intent classification with context.

        If recent intents suggest a workflow progression (e.g., spec -> build),
        boost the confidence of likely next intents.

        Args:
            intent: Initial intent from rule-based classification
            context: HelixContext with recent interactions

        Returns:
            Enhanced intent
        """
        # Get recent intents from interactions
        recent_interactions = context.get_recent_interactions(count=self._context_window)

        if not recent_interactions:
            return intent

        # Get the last intent type from interactions
        if recent_interactions:
            last_intent_type_str = recent_interactions[0].intent_type
            try:
                last_intent_type = IntentType(last_intent_type_str)
            except ValueError:
                return intent

            # Define workflow progressions
            workflow_progression = {
                IntentType.SPEC: [IntentType.BUILD, IntentType.VERIFY],
                IntentType.BUILD: [IntentType.VERIFY],
                IntentType.VERIFY: [IntentType.SHIP, IntentType.BUILD],
                IntentType.REVIEW: [IntentType.BUILD, IntentType.TEST],
            }

            # Check if current intent matches workflow progression
            if last_intent_type in workflow_progression:
                expected_next = workflow_progression[last_intent_type]
                if intent.type in expected_next:
                    # Boost confidence for workflow progression
                    intent.confidence = min(0.95, intent.confidence + 0.1)
                    intent.context_window = f"workflow:{last_intent_type.value}"

        return intent

    def _calculate_confidence(self, intent: Intent) -> float:
        """
        Calculate final confidence score.

        Args:
            intent: Intent to calculate confidence for

        Returns:
            Confidence score between 0 and 1
        """
        # Base confidence from rule matching
        base_confidence: float = float(intent.confidence)

        # Adjust based on input length (longer inputs tend to be more specific)
        input_length = len(intent.raw_input)
        if input_length > 50:
            base_confidence = min(0.95, base_confidence + 0.05)
        elif input_length < 10:
            base_confidence = max(0.3, base_confidence - 0.1)

        return base_confidence

    def register_pattern(self, intent_type: IntentType, pattern: str) -> None:
        """
        Register a new pattern for intent type.

        Args:
            intent_type: Intent type to register pattern for
            pattern: Regex pattern to match
        """
        if intent_type not in self.PATTERNS:
            self.PATTERNS[intent_type] = []

        self.PATTERNS[intent_type].append(pattern)
        self._compiled_patterns[intent_type].append(
            re.compile(pattern, re.IGNORECASE)
        )
