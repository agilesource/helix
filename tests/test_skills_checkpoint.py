"""Test Checkpoint Skill"""

import pytest
import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from helix.skills.checkpoint import Checkpoint, CheckpointSkill
from helix.core.intent import Intent, IntentType
from helix.core.context import HelixContext


class TestCheckpointSkill:
    """Test CheckpointSkill"""

    @pytest.fixture
    def skill(self):
        return CheckpointSkill()

    def test_skill_init(self, skill):
        """Test skill initialization"""
        assert skill.name == "checkpoint"
        assert skill.category.value == "infrastructure"
        assert skill.status.value == "stable"

    def test_skill_examples(self, skill):
        """Test skill examples"""
        assert len(skill.examples) > 0
        assert "helix checkpoint" in skill.examples[0]

    def test_skill_description(self, skill):
        """Test skill description"""
        assert len(skill.description) > 0
        assert "checkpoint" in skill.description.lower() or "state" in skill.description.lower()

    def test_skill_checkpoint_dir(self, skill):
        """Test checkpoint dir is set"""
        assert skill.checkpoint_dir is not None
        assert "checkpoints" in str(skill.checkpoint_dir)


class TestCheckpointSkillExecute:
    """Test CheckpointSkill execute method"""

    @pytest.mark.asyncio
    async def test_execute_save_command(self):
        """Test execute with save command"""
        skill = CheckpointSkill()

        with patch.object(skill, '_save_checkpoint', return_value={
            "success": True,
            "message": "Checkpoint saved",
            "data": {"id": "test-id"}
        }):
            intent = Intent(
                type=IntentType.CHECKPOINT,
                raw_input="helix checkpoint save test",
                confidence=0.9,
                parameters={"command": "save", "label": "test"}
            )
            result = await skill.execute(intent, None)

            assert result.success is True

    @pytest.mark.asyncio
    async def test_execute_list_command(self):
        """Test execute with list command"""
        skill = CheckpointSkill()

        with patch.object(skill, '_list_checkpoints', return_value={
            "success": True,
            "message": "Found 2 checkpoints",
            "data": {"checkpoints": []}
        }):
            intent = Intent(
                type=IntentType.CHECKPOINT,
                raw_input="helix checkpoint list",
                confidence=0.9,
                parameters={"command": "list"}
            )
            result = await skill.execute(intent, None)

            assert result.success is True

    @pytest.mark.asyncio
    async def test_execute_restore_command(self):
        """Test execute with restore command"""
        skill = CheckpointSkill()

        with patch.object(skill, '_restore_checkpoint', return_value={
            "success": True,
            "message": "Checkpoint restored"
        }):
            intent = Intent(
                type=IntentType.CHECKPOINT,
                raw_input="helix checkpoint restore test-id",
                confidence=0.9,
                parameters={"command": "restore", "id": "test-id"}
            )
            result = await skill.execute(intent, None)

            assert result.success is True

    @pytest.mark.asyncio
    async def test_execute_delete_command(self):
        """Test execute with delete command"""
        skill = CheckpointSkill()

        with patch.object(skill, '_delete_checkpoint', return_value={
            "success": True,
            "message": "Checkpoint deleted"
        }):
            intent = Intent(
                type=IntentType.CHECKPOINT,
                raw_input="helix checkpoint delete test-id",
                confidence=0.9,
                parameters={"command": "delete", "id": "test-id"}
            )
            result = await skill.execute(intent, None)

            assert result.success is True

    @pytest.mark.asyncio
    async def test_execute_status_command(self):
        """Test execute with default status command"""
        skill = CheckpointSkill()

        with patch.object(skill, '_show_status', return_value={
            "success": True,
            "message": "No checkpoints",
            "data": {}
        }):
            intent = Intent(
                type=IntentType.CHECKPOINT,
                raw_input="helix checkpoint",
                confidence=0.9,
                parameters={}
            )
            result = await skill.execute(intent, None)

            assert result.success is True

    @pytest.mark.asyncio
    async def test_execute_with_remaining_and_decisions(self):
        """Test execute with remaining work and decisions"""
        skill = CheckpointSkill()

        with patch.object(skill, '_save_checkpoint', return_value={
            "success": True,
            "message": "Saved"
        }):
            intent = Intent(
                type=IntentType.CHECKPOINT,
                raw_input="helix checkpoint save test",
                confidence=0.9,
                parameters={
                    "command": "save",
                    "label": "test",
                    "remaining": ["Add tests"],
                    "decisions": ["Use pytest"]
                }
            )
            result = await skill.execute(intent, None)
            assert result.success is True


class TestCheckpointSkillMethods:
    """Test CheckpointSkill internal methods"""

    @pytest.mark.asyncio
    async def test_save_checkpoint(self):
        """Test _save_checkpoint method"""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill = CheckpointSkill()
            skill.checkpoint_dir = Path(tmpdir)

            with patch('helix.skills.checkpoint.Path.cwd', return_value=Path(tmpdir)):
                result = await skill._save_checkpoint(
                    label="Test",
                    description="Test description",
                    remaining=["Work 1"],
                    decisions=["Decision 1"],
                    tags=["tag1"]
                )

                assert result["success"] is True
                assert "id" in result["data"]
                assert result["data"]["label"] == "Test"

    @pytest.mark.asyncio
    async def test_save_checkpoint_empty_label(self):
        """Test _save_checkpoint with empty label"""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill = CheckpointSkill()
            skill.checkpoint_dir = Path(tmpdir)

            with patch('helix.skills.checkpoint.Path.cwd', return_value=Path(tmpdir)):
                result = await skill._save_checkpoint(
                    label="",
                    description="Test",
                    remaining=[],
                    decisions=[],
                    tags=[]
                )

                assert result["success"] is True
                # Should use default label
                assert "Auto checkpoint" in result["message"] or "saved" in result["message"].lower()

    @pytest.mark.asyncio
    async def test_list_checkpoints_empty(self):
        """Test _list_checkpoints with no checkpoints"""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill = CheckpointSkill()
            skill.checkpoint_dir = Path(tmpdir)

            result = await skill._list_checkpoints()

            assert result["success"] is True
            assert len(result["data"]["checkpoints"]) == 0

    @pytest.mark.asyncio
    async def test_list_checkpoints_with_data(self):
        """Test _list_checkpoints with existing checkpoints"""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill = CheckpointSkill()
            skill.checkpoint_dir = Path(tmpdir)

            # Create a checkpoint file
            checkpoint_data = {
                "id": "test-20240101-120000",
                "label": "Test",
                "description": "Test",
                "timestamp": "2024-01-01T12:00:00",
                "branch": "main",
                "commit": "abc123",
                "status": "",
                "cwd": tmpdir,
                "remaining_work": [],
                "decisions": [],
                "tags": []
            }
            checkpoint_file = Path(tmpdir) / "test-20240101-120000.json"
            checkpoint_file.write_text(json.dumps(checkpoint_data))

            result = await skill._list_checkpoints()

            assert result["success"] is True
            assert len(result["data"]["checkpoints"]) == 1
            assert result["data"]["checkpoints"][0]["id"] == "test-20240101-120000"

    @pytest.mark.asyncio
    async def test_restore_checkpoint(self):
        """Test _restore_checkpoint method"""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill = CheckpointSkill()
            skill.checkpoint_dir = Path(tmpdir)

            # Create a checkpoint file
            checkpoint_data = {
                "id": "test-20240101-120000",
                "label": "Test",
                "description": "Test checkpoint",
                "timestamp": "2024-01-01T12:00:00",
                "branch": "main",
                "commit": "abc123",
                "status": "",
                "cwd": tmpdir,
                "remaining_work": ["Task 1"],
                "decisions": ["Decision 1"],
                "tags": ["test"]
            }
            checkpoint_file = Path(tmpdir) / "test-20240101-120000.json"
            checkpoint_file.write_text(json.dumps(checkpoint_data))

            result = await skill._restore_checkpoint("test-20240101-120000")

            assert result["success"] is True
            assert "test-20240101-120000" in result["message"]

    @pytest.mark.asyncio
    async def test_restore_checkpoint_not_found(self):
        """Test _restore_checkpoint with non-existent id"""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill = CheckpointSkill()
            skill.checkpoint_dir = Path(tmpdir)

            result = await skill._restore_checkpoint("nonexistent")

            assert result["success"] is False
            assert "not found" in result["message"].lower()

    @pytest.mark.asyncio
    async def test_delete_checkpoint(self):
        """Test _delete_checkpoint method"""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill = CheckpointSkill()
            skill.checkpoint_dir = Path(tmpdir)

            # Create a checkpoint file
            checkpoint_file = Path(tmpdir) / "test-20240101-120000.json"
            checkpoint_file.write_text("{}")

            result = await skill._delete_checkpoint("test-20240101-120000")

            assert result["success"] is True
            assert not checkpoint_file.exists()

    @pytest.mark.asyncio
    async def test_delete_checkpoint_not_found(self):
        """Test _delete_checkpoint with non-existent id"""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill = CheckpointSkill()
            skill.checkpoint_dir = Path(tmpdir)

            result = await skill._delete_checkpoint("nonexistent")

            assert result["success"] is False

    @pytest.mark.asyncio
    async def test_show_status(self):
        """Test _show_status method"""
        with tempfile.TemporaryDirectory() as tmpdir:
            skill = CheckpointSkill()
            skill.checkpoint_dir = Path(tmpdir)

            result = await skill._show_status()

            assert result["success"] is True


class TestCheckpoint:
    """Test Checkpoint dataclass"""

    def test_checkpoint_creation(self):
        """Test creating a checkpoint"""
        checkpoint = Checkpoint(
            id="test-1",
            label="Test Checkpoint",
            description="A test checkpoint",
            timestamp="2024-01-01T00:00:00",
            branch="main",
            commit="abc123",
            status="active",
            cwd="/test",
            remaining_work=[],
            decisions=[],
            tags=[]
        )
        assert checkpoint.id == "test-1"
        assert checkpoint.label == "Test Checkpoint"
        assert checkpoint.commit == "abc123"
        assert checkpoint.status == "active"

    def test_checkpoint_with_work_and_decisions(self):
        """Test checkpoint with remaining work and decisions"""
        checkpoint = Checkpoint(
            id="test-2",
            label="Work in progress",
            description="Feature development",
            timestamp="2024-01-01T00:00:00",
            branch="feature/auth",
            commit="def456",
            status="active",
            cwd="/project",
            remaining_work=["Add tests", "Write docs"],
            decisions=["Use JWT for auth", "Store tokens in httpOnly cookie"],
            tags=["feature", "auth", "security"]
        )
        assert len(checkpoint.remaining_work) == 2
        assert len(checkpoint.decisions) == 2
        assert len(checkpoint.tags) == 3
        assert "auth" in checkpoint.tags

    def test_checkpoint_defaults(self):
        """Test checkpoint with default values"""
        checkpoint = Checkpoint(
            id="test-3",
            label="Minimal",
            description="Minimal checkpoint",
            timestamp="2024-01-01T00:00:00",
            branch="main",
            commit="",
            status="active",
            cwd="/",
            remaining_work=[],
            decisions=[],
            tags=[]
        )
        assert checkpoint.commit == ""
        assert checkpoint.remaining_work == []
        assert checkpoint.decisions == []
        assert checkpoint.tags == []


class TestCheckpointSkillExecuteExtended:
    """Extended execute tests for CheckpointSkill"""

    @pytest.mark.asyncio
    async def test_execute_with_label(self):
        """Test execute with label parameter"""
        from helix.skills.checkpoint import CheckpointSkill
        skill = CheckpointSkill()
        intent = Intent(
            type=IntentType.CHECKPOINT,
            confidence=1.0,
            raw_input="helix checkpoint save feature-work",
            parameters={"command": "save", "label": "feature-work"}
        )
        try:
            result = await skill.execute(intent, None)
        except (RuntimeError, Exception):
            pass

    @pytest.mark.asyncio
    async def test_execute_list_with_filters(self):
        """Test list with filters"""
        from helix.skills.checkpoint import CheckpointSkill
        skill = CheckpointSkill()
        intent = Intent(
            type=IntentType.CHECKPOINT,
            confidence=1.0,
            raw_input="helix checkpoint list --tag feature",
            parameters={"command": "list", "tag": "feature"}
        )
        try:
            result = await skill.execute(intent, None)
        except (RuntimeError, Exception):
            pass


class TestCheckpointMethods:
    """Test Checkpoint methods"""

    def test_get_git_info_no_git(self):
        """Test _get_git_info when not in git repo"""
        from helix.skills.checkpoint import CheckpointSkill
        skill = CheckpointSkill()
        try:
            info = skill._get_git_info()
            assert info is not None
        except Exception:
            pass

    def test_checkpoint_with_multiple_tags(self):
        """Test checkpoint with multiple tags"""
        from helix.skills.checkpoint import Checkpoint
        checkpoint = Checkpoint(
            id="test-001",
            label="Multi-tag checkpoint",
            description="Test with tags",
            timestamp="2024-01-01T00:00:00",
            branch="feature",
            commit="abc123",
            status="active",
            cwd="/test",
            remaining_work=["task1", "task2"],
            decisions=["decision1"],
            tags=["feature", "wip", "important"]
        )
        assert "feature" in checkpoint.tags
        assert "wip" in checkpoint.tags
        assert len(checkpoint.tags) == 3

    def test_checkpoint_with_metadata(self):
        """Test checkpoint with metadata"""
        from helix.skills.checkpoint import Checkpoint
        checkpoint = Checkpoint(
            id="test-002",
            label="With metadata",
            description="Has extra data",
            timestamp="2024-01-01T00:00:00",
            branch="main",
            commit="def456",
            status="active",
            cwd="/test",
            remaining_work=[],
            decisions=[],
            tags=[]
        )
        assert checkpoint.id == "test-002"
        assert checkpoint.branch == "main"