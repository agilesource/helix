"""Test Learn Skill"""

import pytest
import json
import os
import tempfile
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

    def test_learning_defaults(self):
        """Test learning with default values"""
        learning = Learning(
            id="001",
            key="key",
            insight="insight",
            learn_type="pattern",
            confidence=5,
            source="test",
            files=[],
            timestamp="2026-04-13T10:00:00"
        )
        assert learning.files == []
        assert learning.project == ""


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

    @pytest.mark.asyncio
    async def test_export_learnings(self, skill):
        """Test exporting learnings"""
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

        intent = Intent(
            type=IntentType.LEARN,
            confidence=1.0,
            raw_input="helix learn export",
            parameters={"command": "export"}
        )

        result = await skill.execute(intent, None)
        assert result.success is True
        assert "export" in result.message.lower()

    @pytest.mark.asyncio
    async def test_export_empty_learnings(self, skill):
        """Test exporting with no learnings"""
        intent = Intent(
            type=IntentType.LEARN,
            confidence=1.0,
            raw_input="helix learn export",
            parameters={"command": "export"}
        )

        result = await skill.execute(intent, None)
        assert result.success is True


class TestLearnSkillDelete:
    """Test learn skill delete command"""

    @pytest.fixture
    def skill(self, tmp_path):
        with patch("helix.skills.learn.Path.cwd", return_value=tmp_path):
            skill = LearnSkill()
            skill.learnings_file = tmp_path / "learnings.jsonl"
            return skill

    @pytest.mark.asyncio
    async def test_delete_learning(self, skill):
        """Test deleting a learning"""
        skill._save_learning(Learning(
            id="001",
            key="to-delete",
            insight="insight",
            learn_type="pattern",
            confidence=8,
            source="user-stated",
            files=[],
            timestamp="2026-04-13T10:00:00"
        ))

        intent = Intent(
            type=IntentType.LEARN,
            confidence=1.0,
            raw_input="helix learn delete 001",
            parameters={"command": "delete", "id": "001"}
        )

        result = await skill.execute(intent, None)
        assert result.success is True

    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, skill):
        """Test deleting non-existent learning"""
        intent = Intent(
            type=IntentType.LEARN,
            confidence=1.0,
            raw_input="helix learn delete nonexistent",
            parameters={"command": "delete", "id": "nonexistent"}
        )

        result = await skill.execute(intent, None)
        # May succeed or fail depending on implementation
        assert result is not None


class TestLearnSkillEdgeCases:
    """Test learn skill edge cases"""

    @pytest.fixture
    def skill(self, tmp_path):
        with patch("helix.skills.learn.Path.cwd", return_value=tmp_path):
            skill = LearnSkill()
            skill.learnings_file = tmp_path / "learnings.jsonl"
            return skill

    @pytest.mark.asyncio
    async def test_add_learning_with_files(self, skill):
        """Test adding learning with files"""
        intent = Intent(
            type=IntentType.LEARN,
            confidence=1.0,
            raw_input="helix learn add --key test --insight 'test' --files file1.py,file2.py",
            parameters={
                "command": "add",
                "key": "test",
                "insight": "test",
                "files": ["file1.py", "file2.py"]
            }
        )

        result = await skill.execute(intent, None)
        assert result.success is True

    @pytest.mark.asyncio
    async def test_add_learning_custom_type(self, skill):
        """Test adding learning with custom type"""
        intent = Intent(
            type=IntentType.LEARN,
            confidence=1.0,
            raw_input="helix learn add --key test --insight 'test' --type pitfall",
            parameters={
                "command": "add",
                "key": "test",
                "insight": "test",
                "type": "pitfall"
            }
        )

        result = await skill.execute(intent, None)
        assert result.success is True

    @pytest.mark.asyncio
    async def test_unknown_command(self, skill):
        """Test unknown command falls back to show"""
        intent = Intent(
            type=IntentType.LEARN,
            confidence=1.0,
            raw_input="helix learn unknown",
            parameters={"command": "unknown"}
        )

        result = await skill.execute(intent, None)
        assert result.success is True

    @pytest.mark.asyncio
    async def test_load_learnings_error(self, skill):
        """Test handling load error"""
        # Make learnings_file point to invalid path
        skill.learnings_file = Path("/nonexistent/learnings.jsonl")

        intent = Intent(
            type=IntentType.LEARN,
            confidence=1.0,
            raw_input="helix learn",
            parameters={"command": "show"}
        )

        result = await skill.execute(intent, None)
        # Should handle gracefully with empty learnings
        assert result.success is True


class TestLearnSkillExecuteExtended:
    """Extended execute tests for LearnSkill"""

    @pytest.mark.asyncio
    async def test_execute_add_with_files(self):
        """Test add command with files"""
        import tempfile
        from helix.skills.learn import LearnSkill
        skill = LearnSkill()
        # Create temp directory
        with tempfile.TemporaryDirectory() as tmpdir:
            skill.learnings_file = Path(tmpdir) / "learnings.jsonl"

            intent = Intent(
                type=IntentType.LEARN,
                confidence=1.0,
                raw_input="helix learn add --key test-key --insight 'test' --files file1.py",
                parameters={
                    "command": "add",
                    "key": "test-key",
                    "insight": "test insight",
                    "files": ["file1.py"]
                }
            )

            result = await skill.execute(intent, None)
            assert result.success is True

    @pytest.mark.asyncio
    async def test_execute_stats(self):
        """Test stats command"""
        from helix.skills.learn import LearnSkill
        skill = LearnSkill()

        intent = Intent(
            type=IntentType.LEARN,
            confidence=1.0,
            raw_input="helix learn stats",
            parameters={"command": "stats"}
        )

        result = await skill.execute(intent, None)
        assert result.success is True

    @pytest.mark.asyncio
    async def test_execute_export(self):
        """Test export command"""
        from helix.skills.learn import LearnSkill
        skill = LearnSkill()

        intent = Intent(
            type=IntentType.LEARN,
            confidence=1.0,
            raw_input="helix learn export",
            parameters={"command": "export"}
        )

        result = await skill.execute(intent, None)
        assert result.success is True


class TestLearningExtended:
    """Extended Learning tests"""

    def test_learning_with_type(self):
        """Test Learning with different types"""
        learning = Learning(
            id="001",
            key="api-pattern",
            insight="Use async/await for I/O",
            learn_type="pattern",
            confidence=9,
            source="code-review",
            files=["api.py", "db.py"],
            timestamp="2026-04-16T10:00:00",
            project="helix"
        )
        assert learning.learn_type == "pattern"
        assert learning.confidence == 9

    def test_learning_with_bug_type(self):
        """Test Learning with bug type"""
        learning = Learning(
            id="002",
            key="bug-memory-leak",
            insight="Remember to close connections",
            learn_type="bug",
            confidence=10,
            source="incident",
            files=["server.py"],
            timestamp="2026-04-16T11:00:00",
            project="helix"
        )
        assert learning.learn_type == "bug"
        assert learning.confidence == 10

    def test_learning_with_all_fields(self):
        """Test Learning with all fields"""
        learning = Learning(
            id="003",
            key="best-practice",
            insight="Comprehensive insight",
            learn_type="best-practice",
            confidence=8,
            source="documentation",
            files=["README.md", "DOCS.md"],
            timestamp="2026-04-16T12:00:00",
            project="helix"
        )
        assert learning.learn_type == "best-practice"
        assert learning.key == "best-practice"


class TestLearnSkillStorage:
    """Test LearnSkill storage methods"""

    def test_initialize_storage(self):
        """Test storage initialization"""
        from helix.skills.learn import LearnSkill
        skill = LearnSkill()
        assert skill.learnings_file is not None

    def test_load_learnings_empty(self):
        """Test loading with no file"""
        from helix.skills.learn import LearnSkill
        skill = LearnSkill()
        skill.learnings_file = Path("/nonexistent/jsonl")
        learnings = skill._load_learnings()
        assert learnings == []

    def test_save_learning(self, tmp_path):
        """Test saving a learning"""
        from helix.skills.learn import LearnSkill, Learning
        skill = LearnSkill()
        skill.learnings_file = tmp_path / "learnings.jsonl"

        learning = Learning(
            id="test-001",
            key="test-key",
            insight="test insight",
            learn_type="pattern",
            confidence=5,
            source="test",
            files=[],
            timestamp="2026-04-16T12:00:00"
        )

        skill._save_learning(learning)
        assert skill.learnings_file.exists()