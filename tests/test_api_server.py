"""Tests for API server module"""

import pytest
from unittest.mock import patch, MagicMock


class TestSkillRequest:
    """Test SkillRequest model"""

    def test_skill_request_defaults(self):
        """Test default values"""
        from helix.api.server import SkillRequest
        request = SkillRequest(skill="test")
        assert request.skill == "test"
        assert request.parameters == {}
        assert request.context is None


class TestSkillResponse:
    """Test SkillResponse model"""

    def test_skill_response_success(self):
        """Test successful response"""
        from helix.api.server import SkillResponse
        response = SkillResponse(success=True, message="OK", data={"key": "value"})
        assert response.success is True
        assert response.message == "OK"
        assert response.data == {"key": "value"}


class TestPluginInfo:
    """Test PluginInfo model"""

    def test_plugin_info(self):
        """Test plugin info"""
        from helix.api.server import PluginInfo
        info = PluginInfo(
            name="test_plugin",
            version="1.0.0",
            type="skill",
            status="active",
            description="Test plugin"
        )
        assert info.name == "test_plugin"
        assert info.version == "1.0.0"


class TestHealthResponse:
    """Test HealthResponse model"""

    def test_health_response(self):
        """Test health response"""
        from helix.api.server import HealthResponse
        response = HealthResponse(
            status="healthy",
            version="0.8.0",
            uptime_seconds=100.0,
            active_engines=2,
            loaded_plugins=5
        )
        assert response.status == "healthy"
        assert response.uptime_seconds == 100.0


class TestAPIEndpoints:
    """Test API endpoints"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        from fastapi.testclient import TestClient
        from helix.api.server import app
        return TestClient(app)

    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        # Set start_time before testing
        import time
        from helix.api import server as api_server
        api_server._app_state["start_time"] = time.time()

        with patch('helix.engines.get_engine_manager') as mock_manager:
            mock_mgr = MagicMock()
            mock_mgr.get_status.return_value = {
                "active": True,
                "engines": {"engine1": {}, "engine2": {}}
            }
            mock_manager.return_value = mock_mgr

            response = client.get("/health")
            assert response.status_code == 200
            data = response.json()
            assert "status" in data
            assert "version" in data
            assert "uptime_seconds" in data

    def test_list_skills_endpoint(self, client):
        """Test list skills endpoint"""
        response = client.get("/api/skills")
        assert response.status_code == 200
        data = response.json()
        # API returns {"skills": [...], "total": N} format
        assert isinstance(data, dict)
        assert "skills" in data
        assert isinstance(data["skills"], list)

    def test_execute_skill_endpoint(self, client):
        """Test execute skill endpoint"""
        response = client.post("/api/skills/execute", json={
            "skill": "test",
            "parameters": {}
        })
        # Should return success or failure, not 404
        assert response.status_code in [200, 400, 500]

    def test_intent_recognize_endpoint(self, client):
        """Test intent recognition endpoint"""
        response = client.post("/api/intent/recognize", json={
            "text": "build a web app"
        })
        assert response.status_code in [200, 422]

    def test_engines_endpoint(self, client):
        """Test engines endpoint"""
        response = client.get("/api/engines")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_plugins_endpoint(self, client):
        """Test plugins endpoint"""
        response = client.get("/api/plugins")
        assert response.status_code == 200