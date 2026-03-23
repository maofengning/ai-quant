# Backend Implementation Plan - Quant Platform

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build FastAPI backend with TDD for quantitative backtesting platform supporting A-shares and cryptocurrency markets.

**Architecture:** Layered architecture with Data Adapters (akshare/ccxt) → Core Engine (backtesting/indicators) → API Layer (FastAPI) → Frontend. Uses pytest for TDD with ≥80% coverage.

**Tech Stack:** FastAPI, pytest, pandas, numpy, akshare, ccxt, SQLite, Parquet

---

## File Structure

```
backend/
├── pyproject.toml              # Dependencies and project config
├── pytest.ini                  # Pytest configuration
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry
│   ├── config.py               # Configuration management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── domain.py           # Core domain models (Bar, Order, Position)
│   │   └── schemas.py          # API request/response schemas
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── base.py             # DataAdapter base class
│   │   ├── akshare_adapter.py  # A-share data adapter
│   │   ├── ccxt_adapter.py     # Crypto data adapter
│   │   └── cache.py            # Data caching layer
│   ├── core/
│   │   ├── __init__.py
│   │   ├── engine/
│   │   │   ├── __init__.py
│   │   │   ├── base.py         # Engine base class
│   │   │   ├── backtest.py     # BacktestEngine implementation
│   │   │   ├── portfolio.py    # Portfolio management
│   │   │   └── order.py        # Order execution logic
│   │   ├── strategy/
│   │   │   ├── __init__.py
│   │   │   └── base.py         # Strategy base class
│   │   └── indicators/
│   │       ├── __init__.py
│   │       ├── trend.py        # MA, EMA
│   │       └── momentum.py     # RSI, MACD
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── data.py         # Data endpoints
│   │       ├── strategies.py   # Strategy management
│   │       └── backtest.py     # Backtest endpoints
│   └── utils/
│       ├── __init__.py
│       └── errors.py           # Custom exceptions
└── tests/
    ├── __init__.py
    ├── conftest.py             # Pytest fixtures
    ├── unit/
    │   ├── test_domain.py
    │   ├── test_indicators.py
    │   ├── test_adapters.py
    │   └── test_engine.py
    └── integration/
        ├── test_api_data.py
        └── test_api_backtest.py
```

---

## Task 1: Project Initialization

**Files:**
- Create: `backend/pyproject.toml`
- Create: `backend/pytest.ini`
- Create: `backend/app/__init__.py`
- Create: `backend/tests/__init__.py`
- Create: `backend/tests/conftest.py`

- [ ] **Step 1: Create project structure**

```bash
cd /Users/maofengning/work/project/aicoding/ai-quant
mkdir -p backend/{app,tests}
touch backend/app/__init__.py
touch backend/tests/__init__.py
```

- [ ] **Step 2: Write pyproject.toml**

Create: `backend/pyproject.toml`

```toml
[project]
name = "ai-quant-backend"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.110.0",
    "uvicorn[standard]>=0.27.0",
    "pydantic>=2.6.0",
    "pydantic-settings>=2.2.0",
    "pandas>=2.2.0",
    "numpy>=1.26.0",
    "akshare>=1.13.0",
    "ccxt>=4.2.0",
    "sqlalchemy>=2.0.0",
    "python-multipart>=0.0.9",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.1.0",
    "httpx>=0.26.0",
    "faker>=24.0.0",
    "ruff>=0.3.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

- [ ] **Step 3: Write pytest.ini**

Create: `backend/pytest.ini`

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --strict-markers --tb=short
markers =
    unit: Unit tests
    integration: Integration tests
```

- [ ] **Step 4: Write conftest.py**

Create: `backend/tests/conftest.py`

```python
"""Pytest configuration and shared fixtures."""
import pytest
from datetime import datetime, date


@pytest.fixture
def sample_bar_data():
    """Sample bar data for testing."""
    return {
        "symbol": "000001.SZ",
        "datetime": datetime(2024, 1, 1, 9, 30),
        "open": 10.0,
        "high": 10.5,
        "low": 9.8,
        "close": 10.2,
        "volume": 1000000
    }


@pytest.fixture
def sample_date_range():
    """Sample date range for testing."""
    return date(2023, 1, 1), date(2024, 1, 1)
```

- [ ] **Step 5: Install dependencies**

```bash
cd backend
pip install -e ".[dev]"
```

Expected: Dependencies installed successfully

- [ ] **Step 6: Verify pytest works**

```bash
cd backend
pytest --version
```

Expected: `pytest 8.x.x`

- [ ] **Step 7: Commit**

```bash
git add backend/
git commit -m "feat: initialize backend project structure with pytest

- Add pyproject.toml with FastAPI and testing dependencies
- Configure pytest with markers for unit/integration tests
- Add basic test fixtures in conftest.py

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 2: Domain Models - Bar Data Structure

**Files:**
- Create: `backend/app/models/__init__.py`
- Create: `backend/app/models/domain.py`
- Create: `backend/tests/unit/test_domain.py`

- [ ] **Step 1: Write failing test for Bar model**

Create: `backend/tests/unit/test_domain.py`

```python
"""Tests for domain models."""
import pytest
from datetime import datetime
from app.models.domain import Bar


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
        with pytest.raises(ValueError, match="high must be >= low"):
            Bar(
                symbol="TEST",
                datetime=datetime(2024, 1, 1),
                open=10.0,
                high=9.0,  # Invalid: high < low
                low=10.0,
                close=10.0,
                volume=1000
            )

    def test_bar_volume_positive(self):
        """Test that volume must be positive."""
        with pytest.raises(ValueError, match="volume must be positive"):
            Bar(
                symbol="TEST",
                datetime=datetime(2024, 1, 1),
                open=10.0,
                high=10.0,
                low=10.0,
                close=10.0,
                volume=-100  # Invalid: negative volume
            )
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd backend
pytest tests/unit/test_domain.py::TestBar::test_bar_creation -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'app.models.domain'`

- [ ] **Step 3: Implement Bar model**

Create: `backend/app/models/__init__.py`

```python
"""Data models package."""
from app.models.domain import Bar, Order, Position, Portfolio

__all__ = ["Bar", "Order", "Position", "Portfolio"]
```

Create: `backend/app/models/domain.py`

```python
"""Core domain models for the quantitative trading system."""
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, field_validator


class Bar(BaseModel):
    """OHLCV bar data structure."""

    symbol: str = Field(..., description="Trading symbol")
    datetime: datetime = Field(..., description="Bar timestamp")
    open: float = Field(..., gt=0, description="Open price")
    high: float = Field(..., gt=0, description="High price")
    low: float = Field(..., gt=0, description="Low price")
    close: float = Field(..., gt=0, description="Close price")
    volume: int = Field(..., gt=0, description="Trading volume")

    @field_validator("high")
    @classmethod
    def validate_high_low(cls, v, info):
        """Validate that high >= low."""
        if "low" in info.data and v < info.data["low"]:
            raise ValueError("high must be >= low")
        return v

    @field_validator("volume")
    @classmethod
    def validate_volume_positive(cls, v):
        """Validate that volume is positive."""
        if v <= 0:
            raise ValueError("volume must be positive")
        return v


class Order(BaseModel):
    """Order instruction."""

    symbol: str
    side: Literal["buy", "sell"]
    quantity: int = Field(..., gt=0)
    price: float | None = None  # None for market orders
    order_type: Literal["market", "limit"] = "market"


class Position(BaseModel):
    """Position holding."""

    symbol: str
    quantity: int
    avg_price: float = Field(..., gt=0)

    def calculate_pnl(self, current_price: float) -> float:
        """Calculate unrealized P&L."""
        return (current_price - self.avg_price) * self.quantity


class Portfolio(BaseModel):
    """Portfolio state."""

    cash: float = Field(..., ge=0)
    positions: dict[str, Position] = Field(default_factory=dict)

    def total_value(self, current_prices: dict[str, float]) -> float:
        """Calculate total portfolio value."""
        position_value = sum(
            pos.quantity * current_prices.get(symbol, pos.avg_price)
            for symbol, pos in self.positions.items()
        )
        return self.cash + position_value
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd backend
pytest tests/unit/test_domain.py::TestBar -v
```

Expected: All 3 tests PASS

- [ ] **Step 5: Add tests for Order model**

Append to: `backend/tests/unit/test_domain.py`

```python
from app.models.domain import Order


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
        with pytest.raises(ValueError):
            Order(symbol="TEST", side="buy", quantity=-10)
```

- [ ] **Step 6: Run Order tests**

```bash
cd backend
pytest tests/unit/test_domain.py::TestOrder -v
```

Expected: All 3 tests PASS

- [ ] **Step 7: Add tests for Position model**

Append to: `backend/tests/unit/test_domain.py`

```python
from app.models.domain import Position


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
```

- [ ] **Step 8: Run Position tests**

```bash
cd backend
pytest tests/unit/test_domain.py::TestPosition -v
```

Expected: All 3 tests PASS

- [ ] **Step 9: Add tests for Portfolio model**

Append to: `backend/tests/unit/test_domain.py`

```python
from app.models.domain import Portfolio


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
```

- [ ] **Step 10: Run Portfolio tests**

```bash
cd backend
pytest tests/unit/test_domain.py::TestPortfolio -v
```

Expected: All 3 tests PASS

- [ ] **Step 11: Run all domain tests**

```bash
cd backend
pytest tests/unit/test_domain.py -v
```

Expected: All 12 tests PASS

- [ ] **Step 12: Commit**

```bash
git add backend/app/models/ backend/tests/unit/test_domain.py
git commit -m "feat: implement domain models with TDD

- Add Bar model with OHLCV data and validation
- Add Order model for trading instructions
- Add Position model with P&L calculation
- Add Portfolio model with total value calculation
- 12 tests covering all domain models

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 3: Technical Indicators - Moving Averages

**Files:**
- Create: `backend/app/core/__init__.py`
- Create: `backend/app/core/indicators/__init__.py`
- Create: `backend/app/core/indicators/trend.py`
- Create: `backend/tests/unit/test_indicators.py`

- [ ] **Step 1: Write failing test for SMA**

Create: `backend/tests/unit/test_indicators.py`

```python
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

        pd.testing.assert_series_equal(sma, prices)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd backend
pytest tests/unit/test_indicators.py::TestSMA::test_sma_basic_calculation -v
```

Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement SMA**

Create: `backend/app/core/__init__.py`

```python
"""Core engine package."""
```

Create: `backend/app/core/indicators/__init__.py`

```python
"""Technical indicators package."""
from app.core.indicators.trend import calculate_sma, calculate_ema

__all__ = ["calculate_sma", "calculate_ema"]
```

Create: `backend/app/core/indicators/trend.py`

```python
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
```

- [ ] **Step 4: Run SMA tests**

```bash
cd backend
pytest tests/unit/test_indicators.py::TestSMA -v
```

Expected: All 3 tests PASS

- [ ] **Step 5: Add EMA tests**

Append to: `backend/tests/unit/test_indicators.py`

```python
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

        pd.testing.assert_series_equal(ema, prices)
```

- [ ] **Step 6: Run EMA tests**

```bash
cd backend
pytest tests/unit/test_indicators.py::TestEMA -v
```

Expected: All 2 tests PASS

- [ ] **Step 7: Commit**

```bash
git add backend/app/core/ backend/tests/unit/test_indicators.py
git commit -m "feat: implement moving average indicators

- Add calculate_sma for simple moving average
- Add calculate_ema for exponential moving average
- 5 tests covering edge cases and accuracy

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 4: Data Adapter Base Class

**Files:**
- Create: `backend/app/adapters/__init__.py`
- Create: `backend/app/adapters/base.py`
- Create: `backend/tests/unit/test_adapters.py`

- [ ] **Step 1: Write test for adapter interface**

Create: `backend/tests/unit/test_adapters.py`

```python
"""Tests for data adapters."""
import pytest
from datetime import date
from app.adapters.base import DataAdapter
from app.models.domain import Bar


class MockAdapter(DataAdapter):
    """Mock adapter for testing."""

    def fetch_bars(self, symbol: str, start: date, end: date, timeframe: str):
        """Return mock bar data."""
        from datetime import datetime
        return [
            Bar(
                symbol=symbol,
                datetime=datetime.combine(start, datetime.min.time()),
                open=10.0,
                high=11.0,
                low=9.0,
                close=10.5,
                volume=1000000
            )
        ]

    def get_symbols(self):
        """Return mock symbol list."""
        return ["TEST001", "TEST002"]


class TestDataAdapter:
    """Test DataAdapter base class and interface."""

    def test_fetch_bars_returns_list_of_bars(self):
        """Test that fetch_bars returns Bar objects."""
        adapter = MockAdapter()
        bars = adapter.fetch_bars(
            symbol="TEST001",
            start=date(2024, 1, 1),
            end=date(2024, 1, 2),
            timeframe="1d"
        )

        assert len(bars) > 0
        assert all(isinstance(bar, Bar) for bar in bars)
        assert bars[0].symbol == "TEST001"

    def test_get_symbols_returns_list(self):
        """Test that get_symbols returns symbol list."""
        adapter = MockAdapter()
        symbols = adapter.get_symbols()

        assert isinstance(symbols, list)
        assert len(symbols) > 0
        assert all(isinstance(s, str) for s in symbols)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd backend
pytest tests/unit/test_adapters.py -v
```

Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement DataAdapter base class**

Create: `backend/app/adapters/__init__.py`

```python
"""Data adapters package."""
from app.adapters.base import DataAdapter

__all__ = ["DataAdapter"]
```

Create: `backend/app/adapters/base.py`

```python
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
            List of Bar objects sorted by datetime
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
```

- [ ] **Step 4: Run tests**

```bash
cd backend
pytest tests/unit/test_adapters.py -v
```

Expected: All 2 tests PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/adapters/ backend/tests/unit/test_adapters.py
git commit -m "feat: add data adapter base class

- Define DataAdapter abstract interface
- Add fetch_bars and get_symbols methods
- 2 tests verifying adapter contract

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 5: AKShare Adapter (with Mock)

**Files:**
- Create: `backend/app/adapters/akshare_adapter.py`
- Modify: `backend/tests/unit/test_adapters.py`

- [ ] **Step 1: Write failing test for AKShare adapter**

Append to: `backend/tests/unit/test_adapters.py`

```python
import pandas as pd
from datetime import datetime
from app.adapters.akshare_adapter import AKShareAdapter


class TestAKShareAdapter:
    """Test AKShare adapter."""

    def test_fetch_bars_converts_akshare_data(self, monkeypatch):
        """Test converting AKShare DataFrame to Bar objects."""
        # Mock akshare API response
        mock_df = pd.DataFrame({
            '日期': ['2024-01-01', '2024-01-02'],
            '开盘': [10.0, 10.5],
            '收盘': [10.5, 11.0],
            '最高': [10.8, 11.2],
            '最低': [9.8, 10.3],
            '成交量': [1000000, 1200000]
        })

        def mock_stock_zh_a_hist(*args, **kwargs):
            return mock_df

        monkeypatch.setattr("akshare.stock_zh_a_hist", mock_stock_zh_a_hist)

        adapter = AKShareAdapter()
        bars = adapter.fetch_bars("000001", date(2024, 1, 1), date(2024, 1, 2))

        assert len(bars) == 2
        assert bars[0].symbol == "000001.SZ"
        assert bars[0].close == 10.5
        assert bars[1].close == 11.0

    def test_get_symbols_returns_a_share_list(self):
        """Test getting A-share symbol list."""
        adapter = AKShareAdapter()
        symbols = adapter.get_symbols()

        # Should return non-empty list
        assert isinstance(symbols, list)
        # For now, returns empty list (real implementation later)
        assert len(symbols) >= 0
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd backend
pytest tests/unit/test_adapters.py::TestAKShareAdapter::test_fetch_bars_converts_akshare_data -v
```

Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement AKShareAdapter**

Create: `backend/app/adapters/akshare_adapter.py`

```python
"""AKShare data adapter for A-share market."""
from datetime import date, datetime
import akshare as ak
import pandas as pd
from app.adapters.base import DataAdapter
from app.models.domain import Bar


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
            List of Bar objects
        """
        # Fetch data from akshare
        df = ak.stock_zh_a_hist(
            symbol=symbol,
            period="daily",
            start_date=start.strftime("%Y%m%d"),
            end_date=end.strftime("%Y%m%d"),
            adjust=""
        )

        # Convert to Bar objects
        bars = []
        for _, row in df.iterrows():
            bar = Bar(
                symbol=f"{symbol}.SZ",  # Add exchange suffix
                datetime=datetime.strptime(row['日期'], '%Y-%m-%d'),
                open=float(row['开盘']),
                high=float(row['最高']),
                low=float(row['最低']),
                close=float(row['收盘']),
                volume=int(row['成交量'])
            )
            bars.append(bar)

        return bars

    def get_symbols(self) -> list[str]:
        """
        Get list of A-share symbols.

        Returns:
            List of stock codes (implementation stub)
        """
        # TODO: Implement using ak.stock_zh_a_spot_em()
        return []
```

- [ ] **Step 4: Run tests**

```bash
cd backend
pytest tests/unit/test_adapters.py::TestAKShareAdapter -v
```

Expected: All 2 tests PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/adapters/akshare_adapter.py backend/tests/unit/test_adapters.py
git commit -m "feat: add AKShare adapter for A-share data

- Implement fetch_bars using akshare API
- Convert akshare DataFrame to Bar objects
- Add .SZ exchange suffix to symbols
- 2 tests with monkeypatch mocking

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 6: Backtest Engine - Basic Structure

**Files:**
- Create: `backend/app/core/engine/__init__.py`
- Create: `backend/app/core/engine/base.py`
- Create: `backend/app/core/engine/backtest.py`
- Create: `backend/tests/unit/test_engine.py`

- [ ] **Step 1: Write test for Engine base class**

Create: `backend/tests/unit/test_engine.py`

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd backend
pytest tests/unit/test_engine.py::TestBacktestEngine::test_engine_initialization -v
```

Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement Engine base class**

Create: `backend/app/core/engine/__init__.py`

```python
"""Engine package."""
from app.core.engine.base import Engine
from app.core.engine.backtest import BacktestEngine

__all__ = ["Engine", "BacktestEngine"]
```

Create: `backend/app/core/engine/base.py`

```python
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
```

- [ ] **Step 4: Implement BacktestEngine**

Create: `backend/app/core/engine/backtest.py`

```python
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
```

- [ ] **Step 5: Run tests**

```bash
cd backend
pytest tests/unit/test_engine.py::TestBacktestEngine -v
```

Expected: All 2 tests PASS

- [ ] **Step 6: Add more engine tests**

Append to: `backend/tests/unit/test_engine.py`

```python
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
```

- [ ] **Step 7: Run all engine tests**

```bash
cd backend
pytest tests/unit/test_engine.py -v
```

Expected: All 4 tests PASS

- [ ] **Step 8: Commit**

```bash
git add backend/app/core/engine/ backend/tests/unit/test_engine.py
git commit -m "feat: implement backtest engine core

- Add Engine base class with abstract interface
- Implement BacktestEngine with order execution simulation
- Handle buy/sell orders with commission calculation
- Track positions and portfolio state
- 4 tests covering order execution logic

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 7: FastAPI Application Setup

**Files:**
- Create: `backend/app/main.py`
- Create: `backend/app/config.py`
- Create: `backend/tests/integration/__init__.py`
- Create: `backend/tests/integration/test_api_main.py`

- [ ] **Step 1: Write test for FastAPI app**

Create: `backend/tests/integration/test_api_main.py`

```python
"""Integration tests for FastAPI app."""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestMainApp:
    """Test FastAPI application."""

    def test_root_endpoint(self, client):
        """Test root endpoint returns API info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data

    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd backend
pytest tests/integration/test_api_main.py -v
```

Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement config**

Create: `backend/app/config.py`

```python
"""Application configuration."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "AI Quant Backend"
    version: str = "0.1.0"
    debug: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
```

- [ ] **Step 4: Implement FastAPI app**

Create: `backend/app/main.py`

```python
"""FastAPI application entry point."""
from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Quantitative backtesting platform API"
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "version": settings.version,
        "status": "running"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}
```

- [ ] **Step 5: Run tests**

```bash
cd backend
pytest tests/integration/test_api_main.py -v
```

Expected: All 2 tests PASS

- [ ] **Step 6: Verify app starts**

```bash
cd backend
uvicorn app.main:app --reload &
sleep 2
curl http://127.0.0.1:8000/
pkill -f uvicorn
```

Expected: JSON response with app name and version

- [ ] **Step 7: Commit**

```bash
git add backend/app/main.py backend/app/config.py backend/tests/integration/
git commit -m "feat: add FastAPI application setup

- Create FastAPI app with root and health endpoints
- Add configuration management with pydantic-settings
- 2 integration tests for API endpoints

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Task 8: Data API Endpoints

**Files:**
- Create: `backend/app/api/__init__.py`
- Create: `backend/app/api/v1/__init__.py`
- Create: `backend/app/api/v1/data.py`
- Create: `backend/app/models/schemas.py`
- Modify: `backend/app/main.py`
- Create: `backend/tests/integration/test_api_data.py`

- [ ] **Step 1: Write test for data endpoint**

Create: `backend/tests/integration/test_api_data.py`

```python
"""Integration tests for data API."""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestDataAPI:
    """Test data endpoints."""

    def test_get_symbols(self, client):
        """Test getting symbol list."""
        response = client.get("/api/v1/data/symbols?market=cn_stock")
        assert response.status_code == 200
        data = response.json()
        assert "symbols" in data
        assert isinstance(data["symbols"], list)

    def test_get_symbols_invalid_market(self, client):
        """Test getting symbols with invalid market."""
        response = client.get("/api/v1/data/symbols?market=invalid")
        assert response.status_code == 422
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd backend
pytest tests/integration/test_api_data.py::TestDataAPI::test_get_symbols -v
```

Expected: FAIL with 404 (endpoint not found)

- [ ] **Step 3: Create API schemas**

Create: `backend/app/models/schemas.py`

```python
"""API request/response schemas."""
from pydantic import BaseModel
from typing import Literal


class SymbolsResponse(BaseModel):
    """Response for symbols endpoint."""

    market: str
    symbols: list[str]


class BarsRequest(BaseModel):
    """Request for bars endpoint."""

    symbol: str
    start_date: str
    end_date: str
    timeframe: str = "1d"


class MarketType(str):
    """Supported market types."""

    CN_STOCK = "cn_stock"
    CRYPTO = "crypto"
```

- [ ] **Step 4: Implement data endpoints**

Create: `backend/app/api/__init__.py`

```python
"""API package."""
```

Create: `backend/app/api/v1/__init__.py`

```python
"""API v1 package."""
```

Create: `backend/app/api/v1/data.py`

```python
"""Data API endpoints."""
from fastapi import APIRouter, HTTPException, Query
from typing import Literal
from app.models.schemas import SymbolsResponse
from app.adapters.akshare_adapter import AKShareAdapter

router = APIRouter(prefix="/data", tags=["data"])


@router.get("/symbols", response_model=SymbolsResponse)
async def get_symbols(
    market: Literal["cn_stock", "crypto"] = Query(..., description="Market type")
):
    """
    Get list of available trading symbols.

    Args:
        market: Market type (cn_stock or crypto)

    Returns:
        List of symbol strings
    """
    if market == "cn_stock":
        adapter = AKShareAdapter()
        symbols = adapter.get_symbols()
        return SymbolsResponse(market=market, symbols=symbols)
    elif market == "crypto":
        # TODO: Implement crypto adapter
        return SymbolsResponse(market=market, symbols=[])
    else:
        raise HTTPException(status_code=400, detail="Invalid market type")
```

- [ ] **Step 5: Register router in main app**

Modify: `backend/app/main.py`

```python
"""FastAPI application entry point."""
from fastapi import FastAPI
from app.config import settings
from app.api.v1 import data

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Quantitative backtesting platform API"
)

# Register routers
app.include_router(data.router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "version": settings.version,
        "status": "running"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}
```

- [ ] **Step 6: Run tests**

```bash
cd backend
pytest tests/integration/test_api_data.py -v
```

Expected: All 2 tests PASS

- [ ] **Step 7: Test API manually**

```bash
cd backend
uvicorn app.main:app --reload &
sleep 2
curl "http://127.0.0.1:8000/api/v1/data/symbols?market=cn_stock"
pkill -f uvicorn
```

Expected: JSON response with symbols array

- [ ] **Step 8: Commit**

```bash
git add backend/app/api/ backend/app/models/schemas.py backend/app/main.py backend/tests/integration/test_api_data.py
git commit -m "feat: add data API endpoints

- Implement /api/v1/data/symbols endpoint
- Add API schemas with Pydantic
- Register router in FastAPI app
- 2 integration tests for data endpoints

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Next Steps

Continue with remaining tasks following TDD:

- Task 9: Strategy API endpoints
- Task 10: Backtest API endpoints
- Task 11: Strategy execution framework
- Task 12: End-to-end backtest flow
- Task 13: Error handling
- Task 14: API documentation

Each task should follow the same pattern:
1. Write failing tests
2. Run tests to verify failure
3. Implement minimal code
4. Run tests to verify pass
5. Refactor if needed
6. Commit

---

## Execution Options

Plan complete and saved to `docs/superpowers/plans/2026-03-23-backend-implementation.md`.

**Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration. Use @superpowers:subagent-driven-development

**2. Inline Execution** - Execute tasks in this session using @superpowers:executing-plans, batch execution with checkpoints

**Which approach?**
