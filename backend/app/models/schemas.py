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


# ============== Strategy Schemas ==============

class StrategyCreateRequest(BaseModel):
    """Request for creating a strategy."""
    name: str
    code: str
    description: str | None = None


class StrategyUpdateRequest(BaseModel):
    """Request for updating a strategy."""
    name: str | None = None
    code: str | None = None
    description: str | None = None


class StrategyResponse(BaseModel):
    """Response for a single strategy."""
    strategy_id: str
    name: str
    code: str
    created_at: str
    updated_at: str


class StrategyListResponse(BaseModel):
    """Response for strategy list."""
    strategies: list[StrategyResponse]


# ============== Backtest Schemas ==============

class BacktestRequest(BaseModel):
    """Request for starting a backtest."""
    strategy_id: str
    symbols: list[str]
    start_date: str
    end_date: str
    initial_capital: float
    commission: float = 0.001
    slippage: float = 0.001


class BacktestRunResponse(BaseModel):
    """Response for backtest run."""
    backtest_id: str
    status: Literal['running', 'completed', 'failed']


class BacktestStatusResponse(BaseModel):
    """Response for backtest status."""
    backtest_id: str
    status: Literal['running', 'completed', 'failed']
    progress: float = 0.0


class BacktestSummary(BaseModel):
    """Backtest summary metrics."""
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float


class EquityPoint(BaseModel):
    """Equity curve data point."""
    date: str
    equity: float


class Trade(BaseModel):
    """Trade record."""
    datetime: str
    symbol: str
    side: Literal['buy', 'sell']
    quantity: float
    price: float
    pnl: float


class BacktestResult(BaseModel):
    """Full backtest result."""
    backtest_id: str
    status: Literal['running', 'completed', 'failed']
    summary: BacktestSummary | None = None
    equity_curve: list[EquityPoint] = []
    trades: list[Trade] = []
    daily_returns: list[float] = []
