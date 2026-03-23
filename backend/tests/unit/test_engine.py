"""Tests for backtest engine."""
import pytest
from datetime import datetime
from app.core.engine.base import Engine
from app.core.engine.backtest import BacktestEngine
from app.models.domain import Order, Position


class TestBacktestEngine:
    """Test BacktestEngine."""

    def test_engine_initialization(self):
        """Test creating a backtest engine."""
        engine = BacktestEngine(initial_capital=100000.0, commission=0.0003)

        assert engine.initial_capital == 100000.0
        assert engine.commission == 0.0003
        assert engine.portfolio.cash == 100000.0

    def test_submit_buy_order(self):
        """Test submitting a buy order."""
        engine = BacktestEngine(initial_capital=100000.0, commission=0.001)

        order = Order(
            symbol="000001.SZ",
            side="buy",
            quantity=100,
            price=10.0,
            order_type="limit"
        )

        # Set current price for execution
        engine._current_prices = {"000001.SZ": 10.0}
        result = engine.submit_order(order)

        # Verify order executed
        assert result["status"] == "filled"
        # Cost = 100 * 10 = 1000
        # Commission = 1000 * 0.001 = 1
        # Cash should decrease by 1001
        assert engine.portfolio.cash == 100000.0 - 1001.0

        # Verify position created
        pos = engine.get_position("000001.SZ")
        assert pos is not None
        assert pos.quantity == 100
        assert pos.avg_price == 10.0


class TestBacktestEngineSell:
    """Test sell orders."""

    def test_submit_sell_order(self):
        """Test selling a position."""
        engine = BacktestEngine(initial_capital=100000.0, commission=0.001)
        engine._current_prices = {"000001.SZ": 10.0}

        # First buy
        buy_order = Order(symbol="000001.SZ", side="buy", quantity=100, price=10.0)
        engine.submit_order(buy_order)

        # Then sell
        engine._current_prices = {"000001.SZ": 12.0}
        sell_order = Order(symbol="000001.SZ", side="sell", quantity=50, price=12.0)
        result = engine.submit_order(sell_order)

        assert result["status"] == "filled"
        # Verify position reduced
        pos = engine.get_position("000001.SZ")
        assert pos.quantity == 50

    def test_sell_without_position(self):
        """Test selling without holding position."""
        engine = BacktestEngine(initial_capital=100000.0)
        engine._current_prices = {"000001.SZ": 10.0}

        sell_order = Order(symbol="000001.SZ", side="sell", quantity=100)
        result = engine.submit_order(sell_order)

        assert result["status"] == "rejected"
        assert "no position" in result["reason"]
