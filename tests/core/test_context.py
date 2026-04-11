"""Tests for HelixContext"""

import pytest
from datetime import datetime
from helix.core.context import (
    HelixContext,
    SessionState,
    ProjectState,
    Interaction,
)


class TestSessionState:
    """Test SessionState enum"""

    def test_session_state_values(self):
        """Test SessionState enum values"""
        assert SessionState.IDLE.value == "idle"
        assert SessionState.RUNNING.value == "running"
        assert SessionState.WAITING_CONFIRMATION.value == "waiting_confirmation"
        assert SessionState.COMPLETED.value == "completed"
        assert SessionState.ERROR.value == "error"


class TestProjectState:
    """Test ProjectState dataclass"""

    def test_project_state_defaults(self):
        """Test default values"""
        state = ProjectState(project_path="/test/path", project_type="python")
        assert state.project_path == "/test/path"
        assert state.project_type == "python"
        assert state.framework is None
        assert state.current_branch is None
        assert state.is_dirty is False
        assert state.lines_of_code == 0
        assert state.test_coverage == 0.0
        assert state.last_review_score is None
        assert state.gate_level == 0

    def test_project_state_custom(self):
        """Test custom values"""
        state = ProjectState(
            project_path="/custom/path",
            project_type="javascript",
            framework="react",
            current_branch="main",
            is_dirty=True,
            lines_of_code=1000,
            test_coverage=85.5,
            last_review_score=4.5,
            gate_level=2,
        )
        assert state.framework == "react"
        assert state.current_branch == "main"
        assert state.is_dirty is True
        assert state.lines_of_code == 1000
        assert state.test_coverage == 85.5
        assert state.last_review_score == 4.5
        assert state.gate_level == 2


class TestHelixContext:
    """Test HelixContext class"""

    def test_init(self):
        """Test initialization"""
        ctx = HelixContext()
        assert ctx.session_id is not None
        assert ctx.session_state == SessionState.IDLE
        assert ctx.started_at is not None
        assert ctx.project is None
        assert ctx.interactions == []
        assert ctx.memories == []
        assert ctx.temp_data == {}

    def test_start_session(self):
        """Test session start"""
        ctx = HelixContext()
        ctx.start_session("/test/project")

        assert ctx.session_state == SessionState.RUNNING
        assert ctx.project is not None
        assert ctx.project.project_path == "/test/project"
        assert ctx.project.project_type == "unknown"

    def test_add_memory(self):
        """Test adding memory"""
        ctx = HelixContext()
        ctx.add_memory("pattern", "Use async/await for I/O", ["performance", "async"])

        assert len(ctx.memories) == 1
        memory = ctx.memories[0]
        assert memory["type"] == "pattern"
        assert memory["content"] == "Use async/await for I/O"
        assert "performance" in memory["tags"]
        assert "async" in memory["tags"]

    def test_get_recent_interactions_empty(self):
        """Test get recent interactions when empty"""
        ctx = HelixContext()
        recent = ctx.get_recent_interactions()
        assert recent == []

    def test_get_recent_interactions_with_data(self):
        """Test get recent interactions with data"""
        ctx = HelixContext()
        # Add mock interactions
        for i in range(15):
            interaction = Interaction(
                timestamp=datetime.now(),
                intent_type="build",
                user_input=f"test input {i}",
                skill_name="build",
                result_success=True,
                result_message="success",
            )
            ctx.interactions.append(interaction)

        # Default count
        recent = ctx.get_recent_interactions()
        assert len(recent) == 10

        # Custom count
        recent = ctx.get_recent_interactions(5)
        assert len(recent) == 5

    def test_get_summary(self):
        """Test context summary"""
        ctx = HelixContext()
        ctx.start_session("/test/project")

        summary = ctx.get_summary()

        assert "session_id" in summary
        assert summary["state"] == "running"
        assert "duration_seconds" in summary
        assert summary["interaction_count"] == 0
        assert summary["memory_count"] == 0
        assert summary["project"]["path"] == "/test/project"
        assert summary["project"]["type"] == "unknown"

    def test_get_summary_no_project(self):
        """Test context summary without project"""
        ctx = HelixContext()
        summary = ctx.get_summary()
        assert summary["project"] is None
