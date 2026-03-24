"""Strategy management API."""
import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    StrategyCreateRequest,
    StrategyUpdateRequest,
    StrategyResponse,
    StrategyListResponse,
)

router = APIRouter(prefix="/strategies", tags=["strategies"])

# In-memory storage for demo (replace with database in production)
_strategies: dict[str, dict] = {}


@router.get("", response_model=StrategyListResponse)
async def list_strategies():
    """List all strategies."""
    strategies = [
        StrategyResponse(
            strategy_id=sid,
            name=data["name"],
            code=data["code"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )
        for sid, data in _strategies.items()
    ]
    return StrategyListResponse(strategies=strategies)


@router.get("/{strategy_id}", response_model=StrategyResponse)
async def get_strategy(strategy_id: str):
    """Get a single strategy by ID."""
    if strategy_id not in _strategies:
        raise HTTPException(status_code=404, detail="Strategy not found")
    data = _strategies[strategy_id]
    return StrategyResponse(
        strategy_id=strategy_id,
        name=data["name"],
        code=data["code"],
        created_at=data["created_at"],
        updated_at=data["updated_at"],
    )


@router.post("", response_model=StrategyResponse, status_code=201)
async def create_strategy(request: StrategyCreateRequest):
    """Create a new strategy."""
    strategy_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    _strategies[strategy_id] = {
        "name": request.name,
        "code": request.code,
        "description": request.description,
        "created_at": now,
        "updated_at": now,
    }
    return StrategyResponse(
        strategy_id=strategy_id,
        name=request.name,
        code=request.code,
        created_at=now,
        updated_at=now,
    )


@router.put("/{strategy_id}", response_model=StrategyResponse)
async def update_strategy(strategy_id: str, request: StrategyUpdateRequest):
    """Update an existing strategy."""
    if strategy_id not in _strategies:
        raise HTTPException(status_code=404, detail="Strategy not found")

    strategy = _strategies[strategy_id]
    now = datetime.now().isoformat()

    if request.name is not None:
        strategy["name"] = request.name
    if request.code is not None:
        strategy["code"] = request.code
    if request.description is not None:
        strategy["description"] = request.description

    strategy["updated_at"] = now

    return StrategyResponse(
        strategy_id=strategy_id,
        name=strategy["name"],
        code=strategy["code"],
        created_at=strategy["created_at"],
        updated_at=now,
    )


@router.delete("/{strategy_id}", status_code=204)
async def delete_strategy(strategy_id: str):
    """Delete a strategy."""
    if strategy_id not in _strategies:
        raise HTTPException(status_code=404, detail="Strategy not found")
    del _strategies[strategy_id]