"""Tests for technical indicators."""
import pytest
import pandas as pd
import numpy as np
from app.core.indicators.trend import calculate_sma, calculate_ema


class TestSMA:
    """Test Simple Moving Average."""

    def test_sma_basic_calculation(self):
        """Test SMA with known values."""
        prices = pd.Series([10, 11, 12, 13, 14, 15])
        sma = calculate_sma(prices, window=3)

        expected = pd.Series([np.nan, np.nan, 11.0, 12.0, 13.0, 14.0])
        pd.testing.assert_series_equal(sma, expected)

    def test_sma_window_larger_than_data(self):
        """Test SMA when window > data length."""
        prices = pd.Series([10, 11, 12])
        sma = calculate_sma(prices, window=5)

        assert sma.isna().all()

    def test_sma_window_one(self):
        """Test SMA with window=1 returns original data."""
        prices = pd.Series([10, 11, 12])
        sma = calculate_sma(prices, window=1)

        pd.testing.assert_series_equal(sma, prices, check_dtype=False)

    def test_sma_window_zero_raises_error(self):
        """Test SMA with window=0 raises ValueError."""
        prices = pd.Series([10, 11, 12])
        with pytest.raises(ValueError, match="Window must be positive"):
            calculate_sma(prices, window=0)

    def test_sma_negative_window_raises_error(self):
        """Test SMA with negative window raises ValueError."""
        prices = pd.Series([10, 11, 12])
        with pytest.raises(ValueError, match="Window must be positive"):
            calculate_sma(prices, window=-5)

    def test_sma_empty_series_raises_error(self):
        """Test SMA with empty series raises ValueError."""
        prices = pd.Series([], dtype=float)
        with pytest.raises(ValueError, match="Price series cannot be empty"):
            calculate_sma(prices, window=3)

    def test_sma_non_numeric_data_raises_error(self):
        """Test SMA with non-numeric data raises ValueError."""
        prices = pd.Series(["a", "b", "c"])
        with pytest.raises(ValueError, match="Price series must contain numeric data"):
            calculate_sma(prices, window=3)

    def test_sma_with_nan_values(self):
        """Test SMA handles NaN values in input data."""
        prices = pd.Series([10, np.nan, 12, 13, 14, 15])
        sma = calculate_sma(prices, window=3)

        # SMA should propagate NaN where insufficient valid data
        assert pd.isna(sma.iloc[0])
        assert pd.isna(sma.iloc[1])
        # After NaN, with window=3, positions 2-3 should still be NaN
        assert pd.isna(sma.iloc[2])
        assert pd.isna(sma.iloc[3])
        # Position 4 has [12, 13, 14] - all valid
        assert not pd.isna(sma.iloc[4])

    def test_sma_with_multiple_nan_gaps(self):
        """Test SMA with multiple NaN gaps (simulating market data gaps)."""
        prices = pd.Series([10, 11, np.nan, np.nan, 14, 15, 16])
        sma = calculate_sma(prices, window=3)

        # Check that NaN propagates as expected
        assert pd.isna(sma.iloc[0])
        assert pd.isna(sma.iloc[1])
        # Positions with NaN in window
        assert pd.isna(sma.iloc[2])
        assert pd.isna(sma.iloc[3])
        # Position 4 has [NaN, NaN, 14] - should be NaN
        assert pd.isna(sma.iloc[4])
        # Position 5 has [NaN, 14, 15] - should be NaN
        assert pd.isna(sma.iloc[5])
        # Position 6 has [14, 15, 16] - all valid
        assert not pd.isna(sma.iloc[6])
        assert sma.iloc[6] == 15.0


class TestEMA:
    """Test Exponential Moving Average."""

    def test_ema_basic_calculation(self):
        """Test EMA gives more weight to recent prices."""
        prices = pd.Series([10, 11, 12, 13, 14, 15])
        ema = calculate_ema(prices, span=3)

        # EMA values should be defined from first element
        assert not ema.isna().any()
        # EMA should be greater than SMA due to recency weighting
        sma = calculate_sma(prices, window=3)
        assert ema.iloc[-1] > sma.iloc[-1]

    def test_ema_span_one(self):
        """Test EMA with span=1 returns original data."""
        prices = pd.Series([10, 11, 12])
        ema = calculate_ema(prices, span=1)

        pd.testing.assert_series_equal(ema, prices, check_dtype=False)

    def test_ema_span_zero_raises_error(self):
        """Test EMA with span=0 raises ValueError."""
        prices = pd.Series([10, 11, 12])
        with pytest.raises(ValueError, match="Span must be positive"):
            calculate_ema(prices, span=0)

    def test_ema_negative_span_raises_error(self):
        """Test EMA with negative span raises ValueError."""
        prices = pd.Series([10, 11, 12])
        with pytest.raises(ValueError, match="Span must be positive"):
            calculate_ema(prices, span=-5)

    def test_ema_empty_series_raises_error(self):
        """Test EMA with empty series raises ValueError."""
        prices = pd.Series([], dtype=float)
        with pytest.raises(ValueError, match="Price series cannot be empty"):
            calculate_ema(prices, span=3)

    def test_ema_non_numeric_data_raises_error(self):
        """Test EMA with non-numeric data raises ValueError."""
        prices = pd.Series(["a", "b", "c"])
        with pytest.raises(ValueError, match="Price series must contain numeric data"):
            calculate_ema(prices, span=3)

    def test_ema_with_nan_values(self):
        """Test EMA handles NaN values in input data."""
        prices = pd.Series([10, np.nan, 12, 13, 14, 15])
        ema = calculate_ema(prices, span=3)

        # First value should be 10
        assert ema.iloc[0] == 10
        # EMA propagates previous value when encountering NaN (useful for market gaps)
        assert ema.iloc[1] == 10.0
        # After NaN, EMA continues computing with new values
        assert not pd.isna(ema.iloc[2])
        # Rest should be valid
        assert not pd.isna(ema.iloc[3])
        assert not pd.isna(ema.iloc[4])
        assert not pd.isna(ema.iloc[5])

    def test_ema_with_multiple_nan_gaps(self):
        """Test EMA with multiple NaN gaps (simulating market data gaps)."""
        prices = pd.Series([10, 11, np.nan, np.nan, 14, 15, 16])
        ema = calculate_ema(prices, span=3)

        # First two values should be valid
        assert not pd.isna(ema.iloc[0])
        assert not pd.isna(ema.iloc[1])
        # EMA propagates previous value during NaN gap (market close/weekends)
        assert not pd.isna(ema.iloc[2])
        assert not pd.isna(ema.iloc[3])
        # EMA continues computing after gap
        assert not pd.isna(ema.iloc[4])
        assert not pd.isna(ema.iloc[5])
        assert not pd.isna(ema.iloc[6])
