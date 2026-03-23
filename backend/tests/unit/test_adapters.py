"""Tests for data adapters."""
import pandas as pd
from datetime import date, datetime
from app.adapters.base import DataAdapter
from app.models.domain import Bar


class MockAdapter(DataAdapter):
    """Mock adapter for testing."""

    def fetch_bars(self, symbol: str, start: date, end: date, timeframe: str = "1d") -> list[Bar]:
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


class TestAKShareAdapter:
    """Test AKShare adapter."""

    def test_fetch_bars_converts_akshare_data(self, monkeypatch):
        """Test converting AKShare DataFrame to Bar objects."""
        # Mock akshare API response
        mock_df = pd.DataFrame({
            '日期': ['2024-01-01', '2024-01-02'],
            '开盘': [10.0, 10.5],
            '收盘': [10.5, 11.0],
            '最高': [10.8, 11.2],
            '最低': [9.8, 10.3],
            '成交量': [1000000, 1200000]
        })

        def mock_stock_zh_a_hist(*args, **kwargs):
            return mock_df

        monkeypatch.setattr("akshare.stock_zh_a_hist", mock_stock_zh_a_hist)

        from app.adapters.akshare_adapter import AKShareAdapter
        adapter = AKShareAdapter()
        bars = adapter.fetch_bars("000001", date(2024, 1, 1), date(2024, 1, 2))

        assert len(bars) == 2
        assert bars[0].symbol == "000001.SZ"
        assert bars[0].close == 10.5
        assert bars[1].close == 11.0

    def test_get_symbols_returns_a_share_list(self):
        """Test getting A-share symbol list (stub)."""
        from app.adapters.akshare_adapter import AKShareAdapter
        adapter = AKShareAdapter()
        symbols = adapter.get_symbols()

        # Stub implementation returns empty list
        assert isinstance(symbols, list)
        assert len(symbols) == 0  # Stub returns empty list
