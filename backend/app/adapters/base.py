"""Base class for data adapters."""
from abc import ABC, abstractmethod
from datetime import date
from app.models.domain import Bar


class DataAdapter(ABC):
    """
    Abstract base class for data source adapters.

    Adapters convert external data sources (akshare, ccxt, etc.)
    into the standardized Bar format.
    """

    @abstractmethod
    def fetch_bars(
        self,
        symbol: str,
        start: date,
        end: date,
        timeframe: str = "1d"
    ) -> list[Bar]:
        """
        Fetch OHLCV bars for a symbol in the given date range.

        Args:
            symbol: Trading symbol
            start: Start date
            end: End date
            timeframe: Bar timeframe (1d, 1h, etc.)

        Returns:
            List of Bar objects sorted by datetime (ascending order).
            Implementations must ensure the returned list is sorted by datetime.

        Raises:
            ValueError: If symbol is invalid or timeframe is not supported
            ConnectionError: If network/API connection fails
            TimeoutError: If request times out
            Exception: Subclasses may raise custom exceptions (e.g., DataError) for data fetching/parsing failures
        """
        pass

    @abstractmethod
    def get_symbols(self) -> list[str]:
        """
        Get list of available trading symbols.

        Returns:
            List of symbol strings
        """
        pass
