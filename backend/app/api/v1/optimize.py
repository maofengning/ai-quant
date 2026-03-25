"""Parameter optimization API using Optuna."""
import uuid
import asyncio
from datetime import datetime
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    OptimizeRequest,
    OptimizeRunResponse,
    OptimizeStatusResponse,
    OptimizeResult,
    OptimizationTrial,
)

router = APIRouter(prefix="/optimize", tags=["optimize"])

# In-memory storage for optimizations
_optimizations: Dict[str, Dict] = {}


@router.post("/start", response_model=OptimizeRunResponse)
async def start_optimization(request: OptimizeRequest):
    """Start a new parameter optimization."""
    optimize_id = str(uuid.uuid4())

    # Store optimization request
    _optimizations[optimize_id] = {
        "status": "running",
        "progress": 0.0,
        "request": request.model_dump(),
        "result": None,
        "trials": [],
        "best_trial": None,
        "created_at": datetime.now().isoformat(),
    }

    # Run optimization in background
    asyncio.create_task(_run_optimization_task(optimize_id, request))

    return OptimizeRunResponse(optimize_id=optimize_id, status="running")


@router.get("/{optimize_id}/status", response_model=OptimizeStatusResponse)
async def get_optimization_status(optimize_id: str):
    """Get optimization status."""
    if optimize_id not in _optimizations:
        raise HTTPException(status_code=404, detail="Optimization not found")

    opt = _optimizations[optimize_id]
    return OptimizeStatusResponse(
        optimize_id=optimize_id,
        status=opt["status"],
        progress=opt["progress"],
        trials_count=len(opt["trials"]),
        best_value=opt["best_trial"]["value"] if opt["best_trial"] else None,
    )


@router.get("/{optimize_id}/result", response_model=OptimizeResult)
async def get_optimization_result(optimize_id: str):
    """Get optimization result."""
    if optimize_id not in _optimizations:
        raise HTTPException(status_code=404, detail="Optimization not found")

    opt = _optimizations[optimize_id]

    if opt["status"] != "completed":
        raise HTTPException(status_code=400, detail="Optimization not completed")

    # Convert dict trials to OptimizationTrial objects
    trials = [OptimizationTrial(**t) if isinstance(t, dict) else t for t in opt["trials"]]
    best = OptimizationTrial(**opt["best_trial"]) if isinstance(opt["best_trial"], dict) else opt["best_trial"]

    return OptimizeResult(
        optimize_id=optimize_id,
        status="completed",
        best_trial=best,
        all_trials=trials,
        total_trials=len(trials),
    )


async def _run_optimization_task(optimize_id: str, request: OptimizeRequest):
    """Background task to run parameter optimization using Optuna."""
    try:
        import optuna
        import random

        # Store trial results
        trials_results = []
        best_trial_result = None

        # Define objective function
        def objective(trial):
            params = {}
            for param_name, param_config in request.param_space.items():
                if param_config.type == "int":
                    params[param_name] = trial.suggest_int(param_name, int(param_config.low), int(param_config.high))
                elif param_config.type == "float":
                    params[param_name] = trial.suggest_float(param_name, param_config.low, param_config.high)
                elif param_config.type == "categorical":
                    params[param_name] = trial.suggest_categorical(param_name, param_config.choices or [])

            # Mock objective value
            base_score = 0.5 + random.random() * 0.5
            param_score = sum(params.values()) / (len(params) * 10) if params else 0
            return min(base_score + param_score, 2.0)

        # Create study
        study = optuna.create_study(direction="maximize" if request.direction == "maximize" else "minimize")

        # Run optimization
        total_trials = request.n_trials
        
        for i in range(total_trials):
            if optimize_id not in _optimizations:
                break

            try:
                # Run single trial
                study.optimize(objective, n_trials=1)
                
                # Get the last trial
                trial = study.trials[-1]
                
                if trial.value is not None:
                    # Store trial result as dict
                    trial_dict = {
                        "trial_number": trial.number,
                        "value": trial.value,
                        "params": trial.params or {},
                    }
                    trials_results.append(trial_dict)

                    # Update best trial
                    if study.best_trial and study.best_trial.value is not None:
                        best_trial_result = {
                            "trial_number": study.best_trial.number,
                            "value": study.best_trial.value,
                            "params": study.best_trial.params or {},
                        }

                    # Update progress in main dict
                    _optimizations[optimize_id]["progress"] = (i + 1) / total_trials

            except Exception as e:
                print(f"Trial {i} failed: {e}")
                continue

            await asyncio.sleep(0.1)

        # Store final results
        _optimizations[optimize_id]["trials"] = trials_results
        _optimizations[optimize_id]["best_trial"] = best_trial_result
        _optimizations[optimize_id]["status"] = "completed"
        _optimizations[optimize_id]["progress"] = 1.0

    except Exception as e:
        print(f"Optimization failed: {e}")
        _optimizations[optimize_id]["status"] = "failed"
        _optimizations[optimize_id]["error"] = str(e)
