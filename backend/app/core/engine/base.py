"""Base engine class."""
from abc import ABC, abstractmethod
from app.models.domain import Order, Position, Portfolio


class Engine(ABC):
    """
    Abstract base class for trading engines.

    This interface allows the same strategy to work with both
    backtesting and live trading engines.
    """

    @abstractmethod
    def submit_order(self, order: Order) -> dict:
        """
        Submit an order for execution.

        Args:
            order: Order to execute

        Returns:
            Order execution result dict
        """
        pass

    @abstractmethod
    def get_position(self, symbol: str) -> Position | None:
        """
        Get current position for a symbol.

        Args:
            symbol: Trading symbol

        Returns:
            Position object or None if no position
        """
        pass

    @abstractmethod
    def get_portfolio(self) -> Portfolio:
        """
        Get current portfolio state.

        Returns:
            Portfolio object
        """
        pass
