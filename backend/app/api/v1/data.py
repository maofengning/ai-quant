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
