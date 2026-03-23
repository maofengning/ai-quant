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
