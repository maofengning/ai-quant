"""Trend-following indicators."""
import pandas as pd


def calculate_sma(prices: pd.Series, window: int) -> pd.Series:
    """
    Calculate Simple Moving Average.

    Args:
        prices: Price series
        window: Window size

    Returns:
        SMA series with same index as input
    """
    return prices.rolling(window=window).mean()


def calculate_ema(prices: pd.Series, span: int) -> pd.Series:
    """
    Calculate Exponential Moving Average.

    Args:
        prices: Price series
        span: Span parameter (roughly equivalent to window size)

    Returns:
        EMA series with same index as input
    """
    return prices.ewm(span=span, adjust=False).mean()
