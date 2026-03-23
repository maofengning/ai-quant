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
