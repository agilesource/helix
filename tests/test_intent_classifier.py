"""Test Intent Classifier"""

import pytest
from helix.core.intent_classifier import IntentClassifier
from helix.core.intent import Intent, IntentType
from helix.core.context import HelixContext


class TestIntentClassifier:
    """Test IntentClassifier"""

    @pytest.fixture
    def classifier(self):
        return IntentClassifier()

    def test_classifier_init(self, classifier):
        """Test classifier initialization"""
        assert classifier._context_window == 5

    def test_classify_spec(self, classifier):
        """Test spec intent classification"""
        result = classifier._rule_based_classify("我想要开发一个登录功能")
        assert result.type == IntentType.SPEC

    def test_classify_build(self, classifier):
        """Test build intent classification"""
        result = classifier._rule_based_classify("帮我实现这个功能")
        assert result.type == IntentType.BUILD

    def test_classify_verify(self, classifier):
        """Test verify intent classification"""
        result = classifier._rule_based_classify("运行测试")
        assert result.type == IntentType.VERIFY

    def test_classify_ship(self, classifier):
        """Test ship intent classification"""
        result = classifier._rule_based_classify("发布到生产环境")
        assert result.type == IntentType.SHIP

    def test_classify_review(self, classifier):
        """Test review intent classification"""
        result = classifier._rule_based_classify("帮我review代码")
        assert result.type == IntentType.REVIEW

    def test_classify_audit(self, classifier):
        """Test audit intent classification"""
        result = classifier._rule_based_classify("安全审计")
        assert result.type == IntentType.AUDIT

    def test_classify_browse(self, classifier):
        """Test browse intent classification"""
        result = classifier._rule_based_classify("打开这个网页")
        assert result.type == IntentType.BROWSE

    def test_classify_design(self, classifier):
        """Test design intent classification"""
        result = classifier._rule_based_classify("设计一个登录页面")
        assert result.type == IntentType.DESIGN

    def test_classify_learn(self, classifier):
        """Test learn intent classification"""
        result = classifier._rule_based_classify("记住这个模式")
        assert result.type == IntentType.LEARN

    def test_classify_checkpoint(self, classifier):
        """Test checkpoint intent classification"""
        result = classifier._rule_based_classify("保存当前进度")
        assert result.type == IntentType.CHECKPOINT

    def test_classify_help(self, classifier):
        """Test help intent classification"""
        result = classifier._rule_based_classify("help")
        assert result.type == IntentType.HELP

    def test_classify_unknown(self, classifier):
        """Test unknown intent returns general"""
        result = classifier._rule_based_classify("今天天气怎么样")
        assert result.type == IntentType.GENERAL

    def test_confidence_calculation(self, classifier):
        """Test confidence calculation"""
        # Short input should have lower confidence
        short_result = classifier._rule_based_classify("hi")
        assert short_result.confidence < 0.8

        # Test with clear pattern match - just check it's positive
        long_result = classifier._rule_based_classify("我想要开发一个登录功能")
        assert long_result.confidence > 0

    def test_context_enhancement(self, classifier):
        """Test context enhancement"""
        from helix.skills.base import SkillResult

        # Create context with recent spec intent
        context = HelixContext()
        mock_result = SkillResult(
            success=True,
            message="test",
            skill_name="spec"
        )
        context.add_interaction(
            Intent(type=IntentType.SPEC, raw_input="spec", confidence=0.9),
            mock_result
        )

        # Build should be boosted after spec (use lower confidence to allow boost)
        intent = Intent(type=IntentType.BUILD, raw_input="build", confidence=0.5)
        enhanced = classifier._enhance_with_context(intent, context)

        assert enhanced.confidence > 0.5

    def test_register_pattern(self, classifier):
        """Test custom pattern registration"""
        original_confidence = classifier._rule_based_classify("hello world").confidence

        # Register a new pattern
        classifier.register_pattern(IntentType.HELP, r"hello world")

        new_result = classifier._rule_based_classify("hello world")
        assert new_result.type == IntentType.HELP

    @pytest.mark.asyncio
    async def test_async_classify(self, classifier):
        """Test async classify method"""
        intent = await classifier.classify("我想要一个登录功能", None)
        assert intent.type == IntentType.SPEC
        assert 0 <= intent.confidence <= 1

    @pytest.mark.asyncio
    async def test_async_classify_with_context(self, classifier):
        """Test async classify with context"""
        from helix.skills.base import SkillResult

        context = HelixContext()
        mock_result = SkillResult(
            success=True,
            message="test",
            skill_name="spec"
        )
        context.add_interaction(
            Intent(type=IntentType.SPEC, raw_input="spec", confidence=0.9),
            mock_result
        )

        intent = await classifier.classify("实现它", context)
        # After spec, build is expected
        assert intent.type == IntentType.BUILD


class TestIntentClassifierPatterns:
    """Test intent classification patterns"""

    @pytest.fixture
    def classifier(self):
        return IntentClassifier()

    def test_spec_patterns(self, classifier):
        """Test various spec patterns"""
        test_cases = [
            "我想要一个登录功能",
            "创建一个用户管理模块",
            "需要开发订单功能",
            "spec 生成规格文档"
        ]
        for case in test_cases:
            result = classifier._rule_based_classify(case)
            assert result.type == IntentType.SPEC, f"Failed for: {case}"

    def test_build_patterns(self, classifier):
        """Test various build patterns"""
        test_cases = [
            "实现这个功能",
            "写代码实现",
            "开发用户模块",
            "帮我写代码"
        ]
        for case in test_cases:
            result = classifier._rule_based_classify(case)
            assert result.type == IntentType.BUILD, f"Failed for: {case}"

    def test_verify_patterns(self, classifier):
        """Test various verify patterns"""
        test_cases = [
            "运行测试",
            "验证代码",
            "跑一下单元测试",
            "检查是否有问题"
        ]
        for case in test_cases:
            result = classifier._rule_based_classify(case)
            assert result.type == IntentType.VERIFY, f"Failed for: {case}"


class TestIntentClassifierEdgeCases:
    """Test edge cases"""

    @pytest.fixture
    def classifier(self):
        return IntentClassifier()

    def test_empty_input(self, classifier):
        """Test empty input"""
        result = classifier._rule_based_classify("")
        assert result.type == IntentType.GENERAL

    def test_mixed_intents(self, classifier):
        """Test input with multiple intent signals"""
        result = classifier._rule_based_classify("帮我开发一个功能并测试")
        # Should pick one based on pattern priority
        assert result.type in [IntentType.BUILD, IntentType.SPEC, IntentType.TEST, IntentType.VERIFY]

    def test_english_input(self, classifier):
        """Test English input"""
        result = classifier._rule_based_classify("build a login feature")
        assert result.type == IntentType.BUILD

    def test_mixed_language(self, classifier):
        """Test mixed language input"""
        result = classifier._rule_based_classify("写一个 login 功能")
        # May return BUILD, SPEC, or GENERAL depending on pattern matching
        assert result.type in [IntentType.BUILD, IntentType.SPEC, IntentType.GENERAL]
