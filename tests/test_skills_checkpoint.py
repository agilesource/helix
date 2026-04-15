"""Test Checkpoint Skill"""

import pytest
from pathlib import Path
from helix.skills.checkpoint import Checkpoint, CheckpointSkill


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