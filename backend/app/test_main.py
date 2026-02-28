"""
Backend smoke tests — run with: pytest app/test_main.py -v
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Health endpoint must return 200 with status=healthy."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "healthy", f"Unexpected response: {data}"


def test_health_endpoint_content_type():
    """Health endpoint must return JSON."""
    response = client.get("/api/health")
    assert "application/json" in response.headers.get("content-type", "")
