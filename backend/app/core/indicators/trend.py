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

    Raises:
        ValueError: If window <= 0 or prices is empty or contains non-numeric data
    """
    if window <= 0:
        raise ValueError(f"Window must be positive, got {window}")

    if prices.empty:
        raise ValueError("Price series cannot be empty")

    if not pd.api.types.is_numeric_dtype(prices):
        raise ValueError("Price series must contain numeric data")

    return prices.rolling(window=window).mean()


def calculate_ema(prices: pd.Series, span: int) -> pd.Series:
    """
    Calculate Exponential Moving Average.

    Args:
        prices: Price series
        span: Span parameter (roughly equivalent to window size)

    Returns:
        EMA series with same index as input

    Raises:
        ValueError: If span <= 0 or prices is empty or contains non-numeric data
    """
    if span <= 0:
        raise ValueError(f"Span must be positive, got {span}")

    if prices.empty:
        raise ValueError("Price series cannot be empty")

    if not pd.api.types.is_numeric_dtype(prices):
        raise ValueError("Price series must contain numeric data")

    return prices.ewm(span=span, adjust=False).mean()
