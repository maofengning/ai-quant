"""Pytest configuration and shared fixtures."""
import pytest
from datetime import datetime, date


@pytest.fixture
def sample_bar_data():
    """Sample bar data for testing."""
    return {
        "symbol": "000001.SZ",
        "datetime": datetime(2024, 1, 1, 9, 30),
        "open": 10.0,
        "high": 10.5,
        "low": 9.8,
        "close": 10.2,
        "volume": 1000000
    }


@pytest.fixture
def sample_date_range():
    """Sample date range for testing."""
    return date(2023, 1, 1), date(2024, 1, 1)
