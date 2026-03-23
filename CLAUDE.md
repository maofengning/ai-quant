# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Quant Platform - A quantitative backtesting platform supporting A-share (akshare) and crypto (ccxt) markets.

## Development Commands

### Backend (Python 3.11+)
```bash
cd backend

# Install dependencies
pip install -e ".[dev]"

# Run development server
uvicorn app.main:app --reload --port 8000

# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_engine.py

# Run specific test with verbose
pytest tests/unit/test_engine.py::TestBacktestEngine -v

# Run with coverage
pytest --cov=app --cov-report=html

# Lint
ruff check .
```

### Frontend (Vue 3 + TypeScript)
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage

# Lint
npm run lint
```

## Architecture

### Backend Structure
```
backend/app/
├── api/v1/          # FastAPI routes (data, strategies, backtest, optimize)
├── core/
│   ├── engine/      # Trading engines
│   │   ├── base.py      # Engine ABC (submit_order, get_position, get_portfolio)
│   │   └── backtest.py  # BacktestEngine implementation
│   └── indicators/  # Technical indicators (MA, RSI, MACD)
├── adapters/        # Data source adapters
│   ├── base.py          # DataAdapter ABC (fetch_bars, get_symbols)
│   └── akshare_adapter.py  # A-share data via akshare
├── models/
│   ├── domain.py    # Core domain: Bar, Order, Position, Portfolio
│   └── schemas.py   # Pydantic API schemas
└── config.py        # Settings via pydantic-settings
```

**Key Design Patterns:**
- `Engine` ABC enables same strategy to work for backtesting and future live trading
- `DataAdapter` ABC abstracts data sources - add new markets by implementing this interface
- Domain models use Pydantic validators (e.g., Bar validates high >= low, volume > 0)

### Frontend Structure
```
frontend/src/
├── api/             # Axios client and API functions
├── components/      # Vue components (common/, features/)
├── stores/          # Pinia state management
├── types/           # TypeScript interfaces (api.ts)
├── mocks/           # MSW mock handlers for development
└── utils/           # Formatting, calculations
```

**API Base URL:** Set via `VITE_API_BASE_URL` env var, defaults to `/api/v1`

### Test Structure
- Backend: `tests/unit/` and `tests/integration/` with pytest
- Frontend: `tests/` with vitest, jsdom environment, setup file at `tests/setup.ts`
- Frontend uses MSW (Mock Service Worker) for API mocking in tests and development