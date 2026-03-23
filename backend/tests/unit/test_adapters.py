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
        assert bars[0].symbol == "000001.SZ"  # SZ exchange for non-6xx symbols
        assert bars[0].close == 10.5
        assert bars[0].datetime == datetime(2024, 1, 1)  # Verify datetime parsing
        assert bars[1].close == 11.0
        assert bars[1].datetime == datetime(2024, 1, 2)  # Verify datetime parsing

    def test_get_symbols_returns_a_share_list(self):
        """Test getting A-share symbol list (stub)."""
        from app.adapters.akshare_adapter import AKShareAdapter
        adapter = AKShareAdapter()
        symbols = adapter.get_symbols()

        # Stub implementation returns empty list
        assert isinstance(symbols, list)
        assert len(symbols) == 0  # Stub returns empty list

    def test_fetch_bars_shanghai_exchange(self, monkeypatch):
        """Test that Shanghai stocks (6xx) get .SH suffix."""
        mock_df = pd.DataFrame({
            '日期': ['2024-01-01'],
            '开盘': [10.0],
            '收盘': [10.5],
            '最高': [10.8],
            '最低': [9.8],
            '成交量': [1000000]
        })

        def mock_stock_zh_a_hist(*args, **kwargs):
            return mock_df

        monkeypatch.setattr("akshare.stock_zh_a_hist", mock_stock_zh_a_hist)

        from app.adapters.akshare_adapter import AKShareAdapter
        adapter = AKShareAdapter()
        bars = adapter.fetch_bars("600000", date(2024, 1, 1), date(2024, 1, 2))

        assert bars[0].symbol == "600000.SH"  # SH exchange for 6xx symbols

    def test_fetch_bars_invalid_timeframe(self):
        """Test that unsupported timeframe raises ValueError."""
        from app.adapters.akshare_adapter import AKShareAdapter
        import pytest

        adapter = AKShareAdapter()
        with pytest.raises(ValueError, match="Unsupported timeframe"):
            adapter.fetch_bars("000001", date(2024, 1, 1), date(2024, 1, 2), timeframe="1h")

    def test_fetch_bars_missing_columns(self, monkeypatch):
        """Test that missing required columns raises DataError."""
        mock_df = pd.DataFrame({
            '日期': ['2024-01-01'],
            '开盘': [10.0]
            # Missing other required columns
        })

        def mock_stock_zh_a_hist(*args, **kwargs):
            return mock_df

        monkeypatch.setattr("akshare.stock_zh_a_hist", mock_stock_zh_a_hist)

        from app.adapters.akshare_adapter import AKShareAdapter, DataError
        import pytest

        adapter = AKShareAdapter()
        with pytest.raises(DataError, match="Missing required columns"):
            adapter.fetch_bars("000001", date(2024, 1, 1), date(2024, 1, 2))

    def test_fetch_bars_sorting(self, monkeypatch):
        """Test that bars are sorted by datetime in ascending order."""
        # Return data in reverse order to test sorting
        mock_df = pd.DataFrame({
            '日期': ['2024-01-03', '2024-01-01', '2024-01-02'],
            '开盘': [10.0, 10.5, 10.2],
            '收盘': [10.5, 11.0, 10.7],
            '最高': [10.8, 11.2, 10.9],
            '最低': [9.8, 10.3, 10.1],
            '成交量': [1000000, 1200000, 1100000]
        })

        def mock_stock_zh_a_hist(*args, **kwargs):
            return mock_df

        monkeypatch.setattr("akshare.stock_zh_a_hist", mock_stock_zh_a_hist)

        from app.adapters.akshare_adapter import AKShareAdapter
        adapter = AKShareAdapter()
        bars = adapter.fetch_bars("000001", date(2024, 1, 1), date(2024, 1, 3))

        # Verify bars are sorted by datetime
        assert len(bars) == 3
        assert bars[0].datetime == datetime(2024, 1, 1)
        assert bars[1].datetime == datetime(2024, 1, 2)
        assert bars[2].datetime == datetime(2024, 1, 3)
