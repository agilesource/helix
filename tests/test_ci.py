"""Test CI Module"""

import pytest
from helix.ci import (
    CIWorkflow,
    generate_github_actions_workflow,
    generate_gitlab_ci_workflow,
    create_github_actions_file,
    create_gitlab_ci_file,
    get_status_badge,
)


class TestCIWorkflow:
    """Test CIWorkflow"""

    def test_workflow_creation(self):
        """Test creating a workflow"""
        workflow = CIWorkflow(name="test", on=["push"], jobs={})
        assert workflow.name == "test"
        assert "push" in workflow.on


class TestGenerateGitHubActions:
    """Test GitHub Actions workflow generation"""

    def test_generate_workflow(self):
        """Test generating GitHub Actions workflow"""
        result = generate_github_actions_workflow("test-project")
        assert isinstance(result, str)
        assert "jobs" in result

    def test_generate_gitlab_workflow(self):
        """Test generating GitLab CI workflow"""
        result = generate_gitlab_ci_workflow("test-project")
        assert isinstance(result, str)
        assert "stages" in result


class TestStatusBadge:
    """Test status badge"""

    def test_get_status_badge_success(self):
        """Test success badge"""
        result = get_status_badge("https://github.com/test", "success")
        assert isinstance(result, str)
        assert "success" in result.lower() or "green" in result.lower()

    def test_get_status_badge_failure(self):
        """Test failure badge"""
        result = get_status_badge("https://github.com/test", "failure")
        assert isinstance(result, str)