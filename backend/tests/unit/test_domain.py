"""Tests for domain models."""
import pytest
from datetime import datetime
from pydantic import ValidationError
from app.models.domain import Bar, Order, Position, Portfolio


class TestBar:
    """Test Bar data structure."""

    def test_bar_creation(self, sample_bar_data):
        """Test creating a Bar with valid data."""
        bar = Bar(**sample_bar_data)

        assert bar.symbol == "000001.SZ"
        assert bar.datetime == datetime(2024, 1, 1, 9, 30)
        assert bar.open == 10.0
        assert bar.high == 10.5
        assert bar.low == 9.8
        assert bar.close == 10.2
        assert bar.volume == 1000000

    def test_bar_high_low_validation(self):
        """Test that high must be >= low."""
        with pytest.raises(ValidationError, match="high must be >= low"):
            Bar(
                symbol="TEST",
                datetime=datetime(2024, 1, 1),
                open=10.0,
                high=9.8,  # Invalid: high < low (9.8 < 10.0)
                low=10.0,
                close=10.0,
                volume=1000
            )

    def test_bar_volume_positive(self):
        """Test that volume must be positive."""
        with pytest.raises(ValidationError, match="volume must be positive"):
            Bar(
                symbol="TEST",
                datetime=datetime(2024, 1, 1),
                open=10.0,
                high=10.0,
                low=10.0,
                close=10.0,
                volume=-100  # Invalid: negative volume
            )


class TestOrder:
    """Test Order model."""

    def test_order_creation_buy(self):
        """Test creating a buy order."""
        order = Order(
            symbol="000001.SZ",
            side="buy",
            quantity=100,
            price=10.0,
            order_type="limit"
        )

        assert order.symbol == "000001.SZ"
        assert order.side == "buy"
        assert order.quantity == 100
        assert order.price == 10.0

    def test_order_market_order(self):
        """Test creating a market order (no price)."""
        order = Order(
            symbol="BTC/USDT",
            side="sell",
            quantity=1
        )

        assert order.price is None
        assert order.order_type == "market"

    def test_order_invalid_quantity(self):
        """Test that quantity must be positive."""
        with pytest.raises(ValidationError):
            Order(symbol="TEST", side="buy", quantity=-10)


class TestPosition:
    """Test Position model."""

    def test_position_creation(self):
        """Test creating a position."""
        pos = Position(symbol="000001.SZ", quantity=100, avg_price=10.0)

        assert pos.symbol == "000001.SZ"
        assert pos.quantity == 100
        assert pos.avg_price == 10.0

    def test_position_pnl_profit(self):
        """Test P&L calculation with profit."""
        pos = Position(symbol="BTC/USDT", quantity=1, avg_price=40000.0)
        pnl = pos.calculate_pnl(current_price=45000.0)

        assert pnl == 5000.0

    def test_position_pnl_loss(self):
        """Test P&L calculation with loss."""
        pos = Position(symbol="ETH/USDT", quantity=10, avg_price=3000.0)
        pnl = pos.calculate_pnl(current_price=2800.0)

        assert pnl == -2000.0


class TestPortfolio:
    """Test Portfolio model."""

    def test_portfolio_creation(self):
        """Test creating an empty portfolio."""
        portfolio = Portfolio(cash=100000.0)

        assert portfolio.cash == 100000.0
        assert len(portfolio.positions) == 0

    def test_portfolio_total_value_cash_only(self):
        """Test total value with cash only."""
        portfolio = Portfolio(cash=100000.0)
        total = portfolio.total_value({})

        assert total == 100000.0

    def test_portfolio_total_value_with_positions(self):
        """Test total value with positions."""
        portfolio = Portfolio(
            cash=50000.0,
            positions={
                "000001.SZ": Position(symbol="000001.SZ", quantity=1000, avg_price=10.0),
                "BTC/USDT": Position(symbol="BTC/USDT", quantity=1, avg_price=40000.0)
            }
        )

        current_prices = {"000001.SZ": 12.0, "BTC/USDT": 45000.0}
        total = portfolio.total_value(current_prices)

        # Cash: 50000
        # 000001.SZ: 1000 * 12 = 12000
        # BTC/USDT: 1 * 45000 = 45000
        # Total: 107000
        assert total == 107000.0
