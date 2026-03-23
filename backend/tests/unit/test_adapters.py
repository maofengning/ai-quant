"""Tests for data adapters."""
from datetime import date
from app.adapters.base import DataAdapter
from app.models.domain import Bar


class MockAdapter(DataAdapter):
    """Mock adapter for testing."""

    def fetch_bars(self, symbol: str, start: date, end: date, timeframe: str):
        """Return mock bar data."""
        from datetime import datetime
        return [
            Bar(
                symbol=symbol,
                datetime=datetime.combine(start, datetime.min.time()),
                open=10.0,
                high=11.0,
                low=9.0,
                close=10.5,
                volume=1000000
            )
        ]

    def get_symbols(self):
        """Return mock symbol list."""
        return ["TEST001", "TEST002"]


class TestDataAdapter:
    """Test DataAdapter base class and interface."""

    def test_fetch_bars_returns_list_of_bars(self):
        """Test that fetch_bars returns Bar objects."""
        adapter = MockAdapter()
        bars = adapter.fetch_bars(
            symbol="TEST001",
            start=date(2024, 1, 1),
            end=date(2024, 1, 2),
            timeframe="1d"
        )

        assert len(bars) > 0
        assert all(isinstance(bar, Bar) for bar in bars)
        assert bars[0].symbol == "TEST001"

    def test_get_symbols_returns_list(self):
        """Test that get_symbols returns symbol list."""
        adapter = MockAdapter()
        symbols = adapter.get_symbols()

        assert isinstance(symbols, list)
        assert len(symbols) > 0
        assert all(isinstance(s, str) for s in symbols)
