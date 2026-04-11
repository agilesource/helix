"""
Pytest configuration and fixtures for Helix tests
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock

import pytest

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def mock_helix_context():
    """Create a mock HelixContext for testing"""
    context = MagicMock()
    context.project_name = "test-project"
    context.workspace = Path("/tmp/test-workspace")
    context.requirements = []
    context.specification = {}
    context.artifacts = {}
    return context


@pytest.fixture
def mock_intent():
    """Create a mock Intent for testing"""
    intent = MagicMock()
    intent.type = "build"
    intent.entities = {}
    intent.confidence = 0.9
    return intent


@pytest.fixture
def sample_requirements():
    """Sample requirements for testing"""
    return [
        "Build a user login system",
        "Add API endpoints for CRUD",
        "Implement caching layer"
    ]


@pytest.fixture
def sample_spec():
    """Sample specification for testing"""
    return {
        "project": "test-project",
        "requirements": ["User authentication"],
        "features": [
            {
                "name": "login",
                "description": "User login functionality",
                "components": ["LoginForm", "AuthService"]
            }
        ],
        "tech_stack": {
            "language": "python",
            "framework": "fastapi"
        }
    }


@pytest.fixture
def temp_workspace(tmp_path):
    """Create a temporary workspace for testing"""
    workspace = tmp_path / "test_workspace"
    workspace.mkdir()
    return workspace
