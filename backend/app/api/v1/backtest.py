"""Backtest execution API."""
import uuid
import asyncio
from datetime import datetime
from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    BacktestRequest,
    BacktestRunResponse,
    BacktestStatusResponse,
    BacktestResult,
    BacktestSummary,
    EquityPoint,
    Trade,
)

router = APIRouter(prefix="/backtest", tags=["backtest"])

# In-memory storage for demo
_backtests: dict[str, dict] = {}


@router.post("/run", response_model=BacktestRunResponse)
async def run_backtest(request: BacktestRequest):
    """Start a new backtest."""
    backtest_id = str(uuid.uuid4())

    # Store backtest request
    _backtests[backtest_id] = {
        "status": "running",
        "progress": 0.0,
        "request": request.model_dump(),
        "result": None,
        "created_at": datetime.now().isoformat(),
    }

    # Run backtest in background
    asyncio.create_task(_run_backtest_task(backtest_id, request))

    return BacktestRunResponse(backtest_id=backtest_id, status="running")


async def _run_backtest_task(backtest_id: str, request: BacktestRequest):
    """Background task to run backtest simulation."""
    try:
        # Simulate backtest progress
        for i in range(1, 11):
            await asyncio.sleep(0.3)
            if backtest_id in _backtests:
                _backtests[backtest_id]["progress"] = i / 10.0

        # Generate mock result
        initial_capital = request.initial_capital
        total_return = 0.15 + (hash(backtest_id) % 100) / 500  # Random return
        final_equity = initial_capital * (1 + total_return)

        # Generate equity curve
        equity_curve = []
        days = 100
        for i in range(days):
            date = datetime.now()
            date = date.replace(day=max(1, (i + 1) % 28))
            equity = initial_capital * (1 + (i / days) * total_return)
            equity_curve.append(EquityPoint(date=date.strftime("%Y-%m-%d"), equity=equity))

        # Generate mock trades
        trades = []
        symbols = request.symbols
        for i in range(10):
            symbol = symbols[i % len(symbols)] if symbols else "BTC"
            side = "buy" if i % 2 == 0 else "sell"
            trades.append(Trade(
                datetime=datetime.now().strftime("%Y-%m-%d"),
                symbol=symbol,
                side=side,
                quantity=0.1,
                price=50000,
                pnl=100 if side == "sell" else 0,
            ))

        # Calculate summary
        annual_return = total_return * 252 / days
        summary = BacktestSummary(
            total_return=total_return,
            annual_return=annual_return,
            max_drawdown=0.1 + (hash(backtest_id) % 50) / 500,
            sharpe_ratio=1.5 + (hash(backtest_id) % 100) / 50,
            win_rate=0.5 + (hash(backtest_id) % 40) / 100,
        )

        # Generate daily returns
        daily_returns = [0.01 * ((hash(f"{backtest_id}{i}") % 100) - 50) / 50 for i in range(days)]

        result = BacktestResult(
            backtest_id=backtest_id,
            status="completed",
            summary=summary,
            equity_curve=equity_curve,
            trades=trades,
            daily_returns=daily_returns,
        )

        if backtest_id in _backtests:
            _backtests[backtest_id]["status"] = "completed"
            _backtests[backtest_id]["progress"] = 1.0
            _backtests[backtest_id]["result"] = result.model_dump()

    except Exception as e:
        if backtest_id in _backtests:
            _backtests[backtest_id]["status"] = "failed"
            _backtests[backtest_id]["error"] = str(e)


@router.get("/{backtest_id}/status", response_model=BacktestStatusResponse)
async def get_backtest_status(backtest_id: str):
    """Get backtest status."""
    if backtest_id not in _backtests:
        raise HTTPException(status_code=404, detail="Backtest not found")

    bt = _backtests[backtest_id]
    return BacktestStatusResponse(
        backtest_id=backtest_id,
        status=bt["status"],
        progress=bt.get("progress", 0.0),
    )


@router.get("/{backtest_id}/result", response_model=BacktestResult)
async def get_backtest_result(backtest_id: str):
    """Get backtest result."""
    if backtest_id not in _backtests:
        raise HTTPException(status_code=404, detail="Backtest not found")

    bt = _backtests[backtest_id]
    if bt["result"] is None:
        raise HTTPException(status_code=400, detail="Backtest not completed")

    result_data = bt["result"]
    return BacktestResult(
        backtest_id=result_data["backtest_id"],
        status=result_data["status"],
        summary=result_data.get("summary"),
        equity_curve=[EquityPoint(**e) for e in result_data.get("equity_curve", [])],
        trades=[Trade(**t) for t in result_data.get("trades", [])],
        daily_returns=result_data.get("daily_returns", []),
    )