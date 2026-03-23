"""Core domain models for the quantitative trading system."""
from datetime import datetime as dt
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class Bar(BaseModel):
    """OHLCV bar data structure."""

    model_config = ConfigDict(protected_namespaces=())

    symbol: str = Field(..., description="Trading symbol")
    datetime: dt = Field(..., description="Bar timestamp")
    open: float = Field(..., gt=0, description="Open price")
    high: float = Field(..., gt=0, description="High price")
    low: float = Field(..., gt=0, description="Low price")
    close: float = Field(..., gt=0, description="Close price")
    volume: int = Field(..., description="Trading volume")

    @model_validator(mode='after')
    def validate_high_low(self):
        """Validate that high >= low."""
        if self.high < self.low:
            raise ValueError("high must be >= low")
        return self

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
