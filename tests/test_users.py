"""Test cases"""
import pytest
from fastapi.testclient import TestClient

def test_list_users(client: TestClient):
    """Test list users"""
    response = client.get("/api/users")
    assert response.status_code == 200

def test_create_users(client: TestClient):
    """Test create users"""
    data = {}
    response = client.post("/api/users", json=data)
    assert response.status_code in [200, 201]
