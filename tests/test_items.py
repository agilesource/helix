"""Test cases"""
import pytest
from fastapi.testclient import TestClient

def test_list_items(client: TestClient):
    """Test list items"""
    response = client.get("/api/items")
    assert response.status_code == 200

def test_create_items(client: TestClient):
    """Test create items"""
    data = {}
    response = client.post("/api/items", json=data)
    assert response.status_code in [200, 201]
