"""Backtest engine implementation."""
from app.core.engine.base import Engine
from app.models.domain import Order, Position, Portfolio


class BacktestEngine(Engine):
    """
    Backtesting engine that simulates order execution.
    """

    def __init__(self, initial_capital: float, commission: float = 0.0003):
        """
        Initialize backtest engine.

        Args:
            initial_capital: Starting cash
            commission: Commission rate (e.g., 0.0003 = 0.03%)
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.portfolio = Portfolio(cash=initial_capital)
        self._current_prices: dict[str, float] = {}

    def submit_order(self, order: Order) -> dict:
        """
        Simulate order execution.

        Args:
            order: Order to execute

        Returns:
            Execution result with status and details
        """
        # Get execution price
        exec_price = order.price if order.price else self._current_prices.get(order.symbol)
        if exec_price is None:
            return {"status": "rejected", "reason": "no price available"}

        # Calculate costs
        order_value = exec_price * order.quantity
        commission_cost = order_value * self.commission
        total_cost = order_value + commission_cost

        if order.side == "buy":
            # Check sufficient cash
            if self.portfolio.cash < total_cost:
                return {"status": "rejected", "reason": "insufficient cash"}

            # Deduct cash
            self.portfolio.cash -= total_cost

            # Update or create position
            if order.symbol in self.portfolio.positions:
                pos = self.portfolio.positions[order.symbol]
                new_quantity = pos.quantity + order.quantity
                new_avg_price = (
                    (pos.avg_price * pos.quantity + exec_price * order.quantity) / new_quantity
                )
                pos.quantity = new_quantity
                pos.avg_price = new_avg_price
            else:
                self.portfolio.positions[order.symbol] = Position(
                    symbol=order.symbol,
                    quantity=order.quantity,
                    avg_price=exec_price
                )

        elif order.side == "sell":
            # Check sufficient position
            if order.symbol not in self.portfolio.positions:
                return {"status": "rejected", "reason": "no position to sell"}

            pos = self.portfolio.positions[order.symbol]
            if pos.quantity < order.quantity:
                return {"status": "rejected", "reason": "insufficient quantity"}

            # Receive cash (minus commission)
            self.portfolio.cash += order_value - commission_cost

            # Update position
            pos.quantity -= order.quantity
            if pos.quantity == 0:
                del self.portfolio.positions[order.symbol]

        return {
            "status": "filled",
            "price": exec_price,
            "quantity": order.quantity,
            "commission": commission_cost
        }

    def get_position(self, symbol: str) -> Position | None:
        """Get position for symbol."""
        return self.portfolio.positions.get(symbol)

    def get_portfolio(self) -> Portfolio:
        """Get current portfolio."""
        return self.portfolio
