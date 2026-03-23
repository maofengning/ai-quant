"""AKShare data adapter for A-share market."""
from datetime import date, datetime
import akshare as ak
import pandas as pd
from app.adapters.base import DataAdapter
from app.models.domain import Bar


class DataError(Exception):
    """Data adapter error."""
    pass


class AKShareAdapter(DataAdapter):
    """Adapter for AKShare A-share data source."""

    def fetch_bars(
        self,
        symbol: str,
        start: date,
        end: date,
        timeframe: str = "1d"
    ) -> list[Bar]:
        """
        Fetch A-share bars from AKShare.

        Args:
            symbol: Stock code (e.g., "000001")
            start: Start date
            end: End date
            timeframe: Only "1d" supported currently

        Returns:
            List of Bar objects sorted by datetime (ascending)

        Raises:
            ValueError: If timeframe is not supported
            DataError: If data fetching or parsing fails
        """
        # Validate timeframe
        if timeframe != "1d":
            raise ValueError(f"Unsupported timeframe: {timeframe}. Only '1d' is currently supported.")
        try:
            # Fetch data from akshare
            df = ak.stock_zh_a_hist(
                symbol=symbol,
                period="daily",
                start_date=start.strftime("%Y%m%d"),
                end_date=end.strftime("%Y%m%d"),
                adjust=""
            )
        except Exception as e:
            raise DataError(f"Failed to fetch data from akshare: {e}")

        if df is None or df.empty:
            raise DataError(f"No data returned for symbol {symbol}")

        # Validate required columns
        required_columns = ['日期', '开盘', '最高', '最低', '收盘', '成交量']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise DataError(f"Missing required columns in akshare data: {missing_columns}")

        # Detect exchange: stocks starting with 6 are Shanghai (SH), others are Shenzhen (SZ)
        exchange = "SH" if symbol.startswith("6") else "SZ"

        # Convert to Bar objects
        bars = []
        try:
            for _, row in df.iterrows():
                bar = Bar(
                    symbol=f"{symbol}.{exchange}",  # Add exchange suffix (SH/SZ)
                    datetime=datetime.strptime(row['日期'], '%Y-%m-%d'),
                    open=float(row['开盘']),
                    high=float(row['最高']),
                    low=float(row['最低']),
                    close=float(row['收盘']),
                    volume=int(row['成交量'])
                )
                bars.append(bar)
        except (KeyError, ValueError) as e:
            raise DataError(f"Failed to parse akshare data: {e}")

        # Sort by datetime as required by base class contract
        return sorted(bars, key=lambda b: b.datetime)

    def get_symbols(self) -> list[str]:
        """
        Get list of A-share symbols.

        Returns:
            Empty list (stub implementation)

        Note:
            This is a stub. Real implementation should use ak.stock_zh_a_spot_em()
        """
        return []
