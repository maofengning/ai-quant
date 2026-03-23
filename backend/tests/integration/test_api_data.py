"""Integration tests for data API."""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestDataAPI:
    """Test data endpoints."""

    def test_get_symbols(self, client):
        """Test getting symbol list."""
        response = client.get("/api/v1/data/symbols?market=cn_stock")
        assert response.status_code == 200
        data = response.json()
        assert "symbols" in data
        assert isinstance(data["symbols"], list)

    def test_get_symbols_invalid_market(self, client):
        """Test getting symbols with invalid market."""
        response = client.get("/api/v1/data/symbols?market=invalid")
        assert response.status_code == 422
