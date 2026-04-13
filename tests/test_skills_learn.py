"""Test Learn Skill"""

import pytest
import json
import os
from pathlib import Path
from unittest.mock import patch, Mock
from helix.skills.learn import LearnSkill, Learning
from helix.core.intent import Intent, IntentType


class TestLearning:
    """Test Learning dataclass"""

    def test_learning_creation(self):
        """Test creating a learning"""
        learning = Learning(
            id="test-001",
            key="test-key",
            insight="Test insight",
            learn_type="pattern",
            confidence=8,
            source="user-stated",
            files=["file1.py"],
            timestamp="2026-04-13T10:00:00",
            project="test-project"
        )
        assert learning.id == "test-001"
        assert learning.key == "test-key"
        assert learning.learn_type == "pattern"
        assert learning.confidence == 8


class TestLearnSkill:
    """Test LearnSkill"""

    @pytest.fixture
    def skill(self, tmp_path):
        """Create learn skill with temporary storage"""
        with patch("helix.skills.learn.Path.cwd", return_value=tmp_path):
            skill = LearnSkill()
            skill.learnings_file = tmp_path / "learnings.jsonl"
            return skill

    def test_skill_init(self, skill):
        """Test skill initialization"""
        assert skill.name == "learn"
        assert skill.category.value == "infrastructure"

    @pytest.mark.asyncio
    async def test_add_learning(self, skill):
        """Test adding a learning"""
        intent = Intent(
            type=IntentType.LEARN,
            confidence=1.0,
            raw_input="helix learn add --key test-key --insight 'Test insight'",
            parameters={"command": "add", "key": "test-key", "insight": "Test insight"}
        )

        result = await skill.execute(intent, None)
        assert result.success is True
        assert "test-key" in result.message

    @pytest.mark.asyncio
    async def test_add_learning_missing_key(self, skill):
        """Test adding learning without key fails"""
        intent = Intent(
            type=IntentType.LEARN,
            confidence=1.0,
            raw_input="helix learn add",
            parameters={"command": "add", "key": "", "insight": "Test"}
        )

        result = await skill.execute(intent, None)
        assert result.success is False

    @pytest.mark.asyncio
    async def test_show_recent(self, skill):
        """Test showing recent learnings"""
        # First add some learnings
        skill._save_learning(Learning(
            id="001",
            key="key1",
            insight="insight1",
            learn_type="pattern",
            confidence=8,
            source="user-stated",
            files=[],
            timestamp="2026-04-13T10:00:00"
        ))
        skill._save_learning(Learning(
            id="002",
            key="key2",
            insight="insight2",
            learn_type="pitfall",
            confidence=7,
            source="observed",
            files=[],
            timestamp="2026-04-13T11:00:00"
        ))

        intent = Intent(
            type=IntentType.LEARN,
            confidence=1.0,
            raw_input="helix learn",
            parameters={"command": "show"}
        )

        result = await skill.execute(intent, None)
        assert result.success is True
        assert len(result.data["learnings"]) == 2

    @pytest.mark.asyncio
    async def test_search_learnings(self, skill):
        """Test searching learnings"""
        skill._save_learning(Learning(
            id="001",
            key="python-pattern",
            insight="Use list comprehension",
            learn_type="pattern",
            confidence=8,
            source="user-stated",
            files=[],
            timestamp="2026-04-13T10:00:00"
        ))
        skill._save_learning(Learning(
            id="002",
            key="javascript-tip",
            insight="Use arrow functions",
            learn_type="pattern",
            confidence=7,
            source="observed",
            files=[],
            timestamp="2026-04-13T11:00:00"
        ))

        intent = Intent(
            type=IntentType.LEARN,
            confidence=1.0,
            raw_input="helix learn search python",
            parameters={"command": "search", "query": "python"}
        )

        result = await skill.execute(intent, None)
        assert result.success is True
        assert len(result.data["results"]) == 1
        assert "python" in result.data["results"][0]["key"]

    @pytest.mark.asyncio
    async def test_stats(self, skill):
        """Test showing stats"""
        skill._save_learning(Learning(
            id="001",
            key="key1",
            insight="insight1",
            learn_type="pattern",
            confidence=8,
            source="user-stated",
            files=[],
            timestamp="2026-04-13T10:00:00"
        ))
        skill._save_learning(Learning(
            id="002",
            key="key2",
            insight="insight2",
            learn_type="pattern",
            confidence=7,
            source="observed",
            files=[],
            timestamp="2026-04-13T11:00:00"
        ))

        intent = Intent(
            type=IntentType.LEARN,
            confidence=1.0,
            raw_input="helix learn stats",
            parameters={"command": "stats"}
        )

        result = await skill.execute(intent, None)
        assert result.success is True
        assert result.data["total"] == 2
        assert result.data["by_type"]["pattern"] == 2


class TestLearnSkillDeduplication:
    """Test learning deduplication"""

    @pytest.fixture
    def skill(self, tmp_path):
        with patch("helix.skills.learn.Path.cwd", return_value=tmp_path):
            skill = LearnSkill()
            skill.learnings_file = tmp_path / "learnings.jsonl"
            return skill

    def test_deduplicate_by_key(self, skill):
        """Test deduplication keeps latest"""
        skill._save_learning(Learning(
            id="001",
            key="same-key",
            insight="old insight",
            learn_type="pattern",
            confidence=5,
            source="user-stated",
            files=[],
            timestamp="2026-04-13T10:00:00"
        ))
        skill._save_learning(Learning(
            id="002",
            key="same-key",
            insight="new insight",
            learn_type="pattern",
            confidence=8,
            source="user-stated",
            files=[],
            timestamp="2026-04-13T12:00:00"
        ))

        learnings = skill._deduplicate_learnings()
        assert len(learnings) == 1
        assert learnings[0].insight == "new insight"


class TestExportLearnings:
    """Test learning export"""

    @pytest.fixture
    def skill(self, tmp_path):
        with patch("helix.skills.learn.Path.cwd", return_value=tmp_path):
            skill = LearnSkill()
            skill.learnings_file = tmp_path / "learnings.jsonl"
            return skill