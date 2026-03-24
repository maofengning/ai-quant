"""Dashboard API."""
from fastapi import APIRouter

from app.models.schemas import StrategyListResponse

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("")
async def get_dashboard():
    """Get dashboard statistics and recent backtests."""
    # Import from strategy module to get the data
    from app.api.v1.strategy import _strategies

    # Get stats
    strategy_count = len(_strategies)

    # Mock data for dashboard
    stats = {
        "strategy_count": strategy_count,
        "running_count": 0,
        "return_30d": 5.2,
        "avg_sharpe": 1.35,
    }

    # Mock recent backtests
    recent_backtests = []

    return {
        "stats": stats,
        "recent_backtests": recent_backtests,
    }


@router.get("/stats")
async def get_dashboard_stats():
    """Get dashboard statistics only."""
    from app.api.v1.strategy import _strategies

    strategy_count = len(_strategies)

    return {
        "strategy_count": strategy_count,
        "running_count": 0,
        "return_30d": 5.2,
        "avg_sharpe": 1.35,
    }