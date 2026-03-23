# 后端实现计划 - 量化回测平台

## 1. 项目概述

基于 2026-03-21 设计文档，实现 FastAPI 后端服务，支持量化策略回测、数据管理、参数优化等核心功能。

**开发方式**：TDD（测试驱动开发）
**开发分支**：`feature/backend-impl`（使用 git worktree）
**API 契约**：基于 `docs/api-contract.yaml` OpenAPI 规范

---

## 2. 技术栈

### 2.1 核心依赖

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
    "alembic>=1.13.0",
    "python-multipart>=0.0.9",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.1.0",
    "httpx>=0.26.0",
    "faker>=24.0.0",
    "ruff>=0.3.0",
    "mypy>=1.8.0",
]
```

### 2.2 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 应用入口
│   ├── config.py               # 配置管理
│   ├── api/                    # API 路由层
│   │   ├── __init__.py
│   │   ├── deps.py             # 依赖注入
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── data.py         # 数据接口
│   │   │   ├── strategies.py   # 策略管理
│   │   │   ├── backtest.py     # 回测接口
│   │   │   ├── optimize.py     # 参数优化
│   │   │   └── analysis.py     # 绩效分析
│   ├── core/                   # 核心业务逻辑
│   │   ├── __init__.py
│   │   ├── engine/             # 回测引擎
│   │   │   ├── __init__.py
│   │   │   ├── base.py         # Engine 基类
│   │   │   ├── backtest.py     # BacktestEngine
│   │   │   ├── portfolio.py    # 持仓管理
│   │   │   └── order.py        # 订单执行
│   │   ├── strategy/           # 策略框架
│   │   │   ├── __init__.py
│   │   │   ├── base.py         # Strategy 基类
│   │   │   └── loader.py       # 动态加载策略
│   │   ├── indicators/         # 技术指标
│   │   │   ├── __init__.py
│   │   │   ├── trend.py        # 趋势指标 (MA, EMA)
│   │   │   ├── momentum.py     # 动量指标 (RSI, MACD)
│   │   │   └── volatility.py   # 波动率指标 (BB, ATR)
│   │   └── optimizer/          # 参数优化
│   │       ├── __init__.py
│   │       └── optuna_optimizer.py
│   ├── adapters/               # 数据适配器层
│   │   ├── __init__.py
│   │   ├── base.py             # DataAdapter 基类
│   │   ├── akshare_adapter.py  # A股数据
│   │   ├── ccxt_adapter.py     # 加密货币
│   │   └── cache.py            # 数据缓存管理
│   ├── models/                 # 数据模型
│   │   ├── __init__.py
│   │   ├── domain.py           # 领域模型 (Bar, Tick, Order, Position)
│   │   ├── schemas.py          # API Schema (Pydantic)
│   │   └── database.py         # SQLAlchemy ORM
│   ├── services/               # 业务服务层
│   │   ├── __init__.py
│   │   ├── backtest_service.py
│   │   ├── data_service.py
│   │   └── strategy_service.py
│   └── utils/                  # 工具函数
│       ├── __init__.py
│       ├── errors.py           # 异常定义
│       └── logger.py           # 日志配置
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # pytest fixtures
│   ├── unit/                   # 单元测试
│   │   ├── test_indicators.py
│   │   ├── test_engine.py
│   │   ├── test_adapters.py
│   │   └── test_optimizer.py
│   ├── integration/            # 集成测试
│   │   ├── test_api_data.py
│   │   ├── test_api_backtest.py
│   │   └── test_backtest_flow.py
│   └── fixtures/               # 测试数据
│       ├── market_data.py
│       └── strategies.py
├── alembic/                    # 数据库迁移
│   └── versions/
├── pyproject.toml
├── pytest.ini
└── README.md
```

---

## 3. TDD 实现计划

### Phase 0: 项目初始化 (1天)

**目标**：搭建项目脚手架，配置开发环境

**步骤**：
1. 创建 `backend/` 目录结构
2. 初始化 `pyproject.toml` 和依赖管理
3. 配置 pytest (`pytest.ini`, `conftest.py`)
4. 配置代码质量工具 (ruff, mypy)
5. 编写基础配置类 (`app/config.py`)

**验收标准**：
- ✅ `pytest` 可以成功运行（即使没有测试）
- ✅ `ruff check .` 通过
- ✅ `mypy app/` 通过

---

### Phase 1: 数据模型层 (2天)

**TDD 流程**：先写测试 → 实现代码 → 重构

#### 1.1 领域模型 (`models/domain.py`)

**测试先行** (`tests/unit/test_domain_models.py`)：
```python
def test_bar_creation():
    """测试 Bar 数据结构创建"""
    bar = Bar(
        symbol="000001.SZ",
        datetime=datetime(2024, 1, 1, 9, 30),
        open=10.0,
        high=10.5,
        low=9.8,
        close=10.2,
        volume=1000000
    )
    assert bar.symbol == "000001.SZ"
    assert bar.high >= bar.low
    assert bar.volume > 0

def test_order_validation():
    """测试订单参数验证"""
    with pytest.raises(ValueError):
        Order(side="buy", symbol="", quantity=-100)

def test_position_pnl_calculation():
    """测试持仓盈亏计算"""
    pos = Position(symbol="BTC/USDT", quantity=1.0, avg_price=40000)
    pnl = pos.calculate_pnl(current_price=45000)
    assert pnl == 5000.0
```

**实现代码**：
- `Bar`, `Tick`, `Order`, `Position`, `Portfolio` 数据类
- 使用 Pydantic 进行数据验证
- 实现基础的业务逻辑方法

#### 1.2 API Schema (`models/schemas.py`)

**测试先行**：
```python
def test_backtest_request_schema():
    """测试回测请求参数验证"""
    request = BacktestRequest(
        strategy_id="strat_001",
        symbols=["000001.SZ"],
        start_date="2023-01-01",
        end_date="2024-01-01",
        initial_capital=100000
    )
    assert request.initial_capital > 0
    assert request.start_date < request.end_date
```

**实现代码**：
- 所有 API 的 Request/Response Schema
- 数据验证规则（日期范围、金额正数等）

---

### Phase 2: 数据适配器层 (3天)

**TDD 核心**：mock 外部数据源，测试数据转换和缓存逻辑

#### 2.1 数据适配器基类 (`adapters/base.py`)

**测试先行** (`tests/unit/test_adapters.py`)：
```python
@pytest.fixture
def mock_adapter():
    """Mock 数据适配器用于测试"""
    class MockAdapter(DataAdapter):
        def fetch_bars(self, symbol, start, end, timeframe):
            return [
                Bar(symbol=symbol, datetime=start, open=10, high=11, low=9, close=10.5, volume=1000)
            ]
        def get_symbols(self):
            return ["TEST001", "TEST002"]
    return MockAdapter()

def test_fetch_bars_returns_correct_format(mock_adapter):
    """测试数据获取返回正确格式"""
    bars = mock_adapter.fetch_bars("TEST001", date(2024, 1, 1), date(2024, 1, 2), "1d")
    assert len(bars) > 0
    assert isinstance(bars[0], Bar)
    assert bars[0].symbol == "TEST001"
```

#### 2.2 AKShare 适配器 (`adapters/akshare_adapter.py`)

**测试先行**：
```python
@pytest.fixture
def akshare_adapter():
    return AKShareAdapter()

def test_fetch_stock_daily_bars(akshare_adapter, monkeypatch):
    """测试获取A股日线数据（使用 monkeypatch mock akshare）"""
    def mock_stock_zh_a_hist(*args, **kwargs):
        return pd.DataFrame({
            '日期': ['2024-01-01'],
            '开盘': [10.0],
            '收盘': [10.5],
            '最高': [11.0],
            '最低': [9.8],
            '成交量': [1000000]
        })

    monkeypatch.setattr("akshare.stock_zh_a_hist", mock_stock_zh_a_hist)

    bars = akshare_adapter.fetch_bars("000001", date(2024, 1, 1), date(2024, 1, 2), "1d")
    assert len(bars) == 1
    assert bars[0].close == 10.5
```

**实现代码**：
- akshare API 调用封装
- 数据格式转换（DataFrame → Bar）
- 错误处理（网络超时、数据缺失）

#### 2.3 缓存管理 (`adapters/cache.py`)

**测试先行**：
```python
def test_cache_hit_avoids_network_call(tmp_path):
    """测试缓存命中时不发起网络请求"""
    cache = DataCache(cache_dir=tmp_path)
    cache.set("key1", [Bar(...)])

    result = cache.get("key1")
    assert result is not None
    assert len(result) > 0
```

**实现代码**：
- Parquet 文件读写
- 缓存键生成（symbol + timeframe + date range）
- 缓存过期策略

---

### Phase 3: 核心引擎层 (5天)

#### 3.1 技术指标库 (`core/indicators/`)

**测试先行** (`tests/unit/test_indicators.py`)：
```python
def test_sma_calculation():
    """测试简单移动平均线计算"""
    prices = pd.Series([10, 11, 12, 13, 14, 15])
    sma = calculate_sma(prices, window=3)

    expected = pd.Series([np.nan, np.nan, 11.0, 12.0, 13.0, 14.0])
    pd.testing.assert_series_equal(sma, expected)

def test_rsi_calculation():
    """测试 RSI 指标计算"""
    prices = pd.Series([44, 44.34, 44.09, 43.61, 44.33, 44.83])
    rsi = calculate_rsi(prices, period=3)

    assert 0 <= rsi.iloc[-1] <= 100
    # 使用已知数据验证准确性
```

**实现代码**：
- `calculate_sma`, `calculate_ema`, `calculate_rsi`, `calculate_macd`
- 使用 pandas/numpy 实现高性能计算
- 边界情况处理（数据不足、NaN值）

#### 3.2 回测引擎 (`core/engine/backtest.py`)

**测试先行** (`tests/unit/test_engine.py`)：
```python
@pytest.fixture
def simple_strategy():
    """简单的买入持有策略用于测试"""
    class BuyAndHoldStrategy(Strategy):
        def __init__(self):
            self.bought = False

        def on_bar(self, bar, engine):
            if not self.bought:
                engine.submit_order(Order(
                    side="buy",
                    symbol=bar.symbol,
                    quantity=100
                ))
                self.bought = True
    return BuyAndHoldStrategy()

def test_backtest_execution(simple_strategy):
    """测试回测流程执行"""
    engine = BacktestEngine(
        initial_capital=100000,
        commission=0.0003
    )

    # Mock 数据
    bars = create_test_bars(symbol="TEST", days=10)

    result = engine.run(simple_strategy, bars)

    assert result.total_trades > 0
    assert result.final_capital != 100000
    assert len(result.equity_curve) == 10

def test_order_execution_with_commission():
    """测试订单执行扣除手续费"""
    engine = BacktestEngine(initial_capital=10000, commission=0.001)

    order = Order(side="buy", symbol="TEST", quantity=100, price=10.0)
    result = engine.submit_order(order)

    # 成交金额 = 100 * 10 = 1000
    # 手续费 = 1000 * 0.001 = 1
    assert result.commission == 1.0
    assert engine.cash == 10000 - 1000 - 1

def test_position_tracking():
    """测试持仓跟踪"""
    engine = BacktestEngine(initial_capital=10000)

    # 买入
    engine.submit_order(Order(side="buy", symbol="TEST", quantity=100, price=10))
    pos = engine.get_position("TEST")
    assert pos.quantity == 100
    assert pos.avg_price == 10.0

    # 部分卖出
    engine.submit_order(Order(side="sell", symbol="TEST", quantity=50, price=12))
    pos = engine.get_position("TEST")
    assert pos.quantity == 50
```

**实现代码**：
- `BacktestEngine.run()` 主循环
- `submit_order()` 订单执行逻辑
- 持仓管理（开仓、平仓、成本计算）
- 资金管理（现金、总资产）
- 手续费/滑点模型

#### 3.3 策略框架 (`core/strategy/base.py`)

**测试先行**：
```python
def test_strategy_lifecycle():
    """测试策略生命周期"""
    class TestStrategy(Strategy):
        def __init__(self):
            self.on_start_called = False
            self.on_bar_count = 0

        def on_start(self, engine):
            self.on_start_called = True

        def on_bar(self, bar, engine):
            self.on_bar_count += 1

    strategy = TestStrategy()
    engine = BacktestEngine(initial_capital=10000)

    bars = create_test_bars(days=5)
    engine.run(strategy, bars)

    assert strategy.on_start_called
    assert strategy.on_bar_count == 5
```

**实现代码**：
- `Strategy` 基类定义
- 生命周期钩子 (`on_start`, `on_bar`, `on_stop`, `on_event`)
- 策略上下文 (访问历史数据、当前持仓)

---

### Phase 4: API 路由层 (4天)

#### 4.1 数据接口 (`api/v1/data.py`)

**测试先行** (`tests/integration/test_api_data.py`)：
```python
@pytest.fixture
def client():
    """测试客户端"""
    from app.main import app
    return TestClient(app)

def test_get_symbols(client, monkeypatch):
    """测试获取标的列表"""
    # Mock 数据服务
    def mock_get_symbols(market):
        return ["000001.SZ", "000002.SZ"]

    monkeypatch.setattr("app.services.data_service.get_symbols", mock_get_symbols)

    response = client.get("/api/v1/data/symbols?market=cn_stock")
    assert response.status_code == 200
    data = response.json()
    assert len(data["symbols"]) == 2

def test_get_bars_with_cache(client):
    """测试获取K线数据（测试缓存逻辑）"""
    response = client.get(
        "/api/v1/data/bars",
        params={
            "symbol": "000001.SZ",
            "start_date": "2024-01-01",
            "end_date": "2024-01-10",
            "timeframe": "1d"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "bars" in data
    assert len(data["bars"]) > 0
```

**实现代码**：
- `GET /symbols` - 获取标的列表
- `GET /bars` - 获取K线数据
- `POST /sync` - 同步数据缓存
- 依赖注入 (`Depends(get_data_service)`)

#### 4.2 回测接口 (`api/v1/backtest.py`)

**测试先行** (`tests/integration/test_api_backtest.py`)：
```python
def test_run_backtest(client, db_session):
    """测试启动回测"""
    request_data = {
        "strategy_id": "test_strategy",
        "symbols": ["000001.SZ"],
        "start_date": "2023-01-01",
        "end_date": "2024-01-01",
        "initial_capital": 100000,
        "commission": 0.0003
    }

    response = client.post("/api/v1/backtest/run", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "backtest_id" in data
    assert data["status"] == "running"

def test_get_backtest_result(client):
    """测试获取回测结果"""
    response = client.get("/api/v1/backtest/test_bt_001/result")
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "total_return" in data["summary"]
```

**实现代码**：
- `POST /backtest/run` - 启动回测（异步任务）
- `GET /backtest/{id}/status` - 查询回测状态
- `GET /backtest/{id}/result` - 获取回测结果
- 异步任务管理（使用 asyncio 或 Celery）

#### 4.3 策略管理接口 (`api/v1/strategies.py`)

**测试先行**：
```python
def test_create_strategy(client):
    """测试创建策略"""
    strategy_code = """
class MyStrategy(Strategy):
    def on_bar(self, bar, engine):
        pass
"""
    response = client.post(
        "/api/v1/strategies",
        json={"name": "test_strat", "code": strategy_code}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["strategy_id"] is not None

def test_list_strategies(client):
    """测试列出策略"""
    response = client.get("/api/v1/strategies")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["strategies"], list)
```

**实现代码**：
- `GET /strategies` - 列出策略
- `POST /strategies` - 创建策略
- `GET /strategies/{id}` - 获取策略详情
- `PUT /strategies/{id}` - 更新策略
- `DELETE /strategies/{id}` - 删除策略
- 策略代码安全验证（AST 解析）

---

### Phase 5: 业务服务层 (3天)

#### 5.1 回测服务 (`services/backtest_service.py`)

**测试先行** (`tests/unit/test_backtest_service.py`)：
```python
@pytest.fixture
def backtest_service():
    return BacktestService(
        data_service=mock_data_service,
        strategy_service=mock_strategy_service
    )

def test_create_backtest_task(backtest_service):
    """测试创建回测任务"""
    config = BacktestConfig(
        strategy_id="test",
        symbols=["000001.SZ"],
        start_date=date(2023, 1, 1),
        end_date=date(2024, 1, 1),
        initial_capital=100000
    )

    task_id = backtest_service.create_task(config)
    assert task_id is not None

    status = backtest_service.get_status(task_id)
    assert status.state in ["pending", "running"]

def test_backtest_execution_flow(backtest_service):
    """测试完整回测流程"""
    task_id = backtest_service.create_task(config)
    result = backtest_service.wait_for_result(task_id)

    assert result.status == "completed"
    assert result.summary.total_return is not None
```

**实现代码**：
- 回测任务管理（创建、状态跟踪、结果存储）
- 协调数据服务、策略服务、引擎执行
- 错误处理和重试逻辑

#### 5.2 数据服务 (`services/data_service.py`)

**测试先行**：
```python
def test_get_bars_with_cache(data_service):
    """测试获取数据（缓存逻辑）"""
    # 第一次调用 - 从数据源获取
    bars1 = data_service.get_bars("000001.SZ", start, end, "1d")

    # 第二次调用 - 从缓存获取
    bars2 = data_service.get_bars("000001.SZ", start, end, "1d")

    assert bars1 == bars2
    # 验证只调用了一次外部数据源
```

**实现代码**：
- 数据获取（优先缓存，缓存未命中则调用适配器）
- 数据同步任务
- 缓存管理（清理、更新）

---

### Phase 6: 高级功能 (3天)

#### 6.1 参数优化 (`core/optimizer/optuna_optimizer.py`)

**测试先行** (`tests/unit/test_optimizer.py`)：
```python
def test_parameter_optimization():
    """测试参数优化"""
    def objective(params):
        # 运行回测并返回目标指标
        result = run_backtest(strategy_params=params)
        return result.sharpe_ratio

    optimizer = OptunaOptimizer()
    best_params = optimizer.optimize(
        objective=objective,
        param_space={
            "fast_period": (5, 20),
            "slow_period": (20, 50)
        },
        n_trials=10
    )

    assert "fast_period" in best_params
    assert best_params["fast_period"] < best_params["slow_period"]
```

**实现代码**：
- Optuna 集成
- 参数空间定义
- 并行优化支持

#### 6.2 绩效分析 (`services/analysis_service.py`)

**测试先行**：
```python
def test_performance_metrics_calculation():
    """测试绩效指标计算"""
    equity_curve = [100000, 102000, 101000, 105000, 103000]

    metrics = calculate_metrics(equity_curve)

    assert "total_return" in metrics
    assert "max_drawdown" in metrics
    assert "sharpe_ratio" in metrics
    assert metrics["total_return"] == 0.03  # 3%
```

**实现代码**：
- 收益率计算
- 最大回撤
- 夏普比率
- 胜率、盈亏比

---

### Phase 7: 错误处理与日志 (2天)

#### 7.1 异常处理 (`utils/errors.py`)

**测试先行**：
```python
def test_data_error_handling(client):
    """测试数据源错误处理"""
    response = client.get("/api/v1/data/bars?symbol=INVALID")
    assert response.status_code == 400
    data = response.json()
    assert data["code"] == "DATA_NOT_FOUND"

def test_engine_error_handling():
    """测试引擎错误处理"""
    engine = BacktestEngine(initial_capital=1000)

    # 尝试买入超过资金的数量
    with pytest.raises(InsufficientFundsError):
        engine.submit_order(Order(side="buy", quantity=1000, price=100))
```

**实现代码**：
- 自定义异常类层次结构
- API 层异常处理器
- 友好的错误消息

#### 7.2 日志配置 (`utils/logger.py`)

**实现代码**：
- 结构化日志 (JSON 格式)
- 日志级别配置
- 日志轮转

---

### Phase 8: 集成测试与优化 (2天)

#### 8.1 端到端测试 (`tests/integration/test_backtest_flow.py`)

**测试场景**：
```python
def test_complete_backtest_flow(client):
    """测试完整回测流程：创建策略 → 运行回测 → 获取结果"""
    # 1. 创建策略
    strategy_response = client.post("/api/v1/strategies", json={...})
    strategy_id = strategy_response.json()["strategy_id"]

    # 2. 启动回测
    backtest_response = client.post("/api/v1/backtest/run", json={
        "strategy_id": strategy_id,
        ...
    })
    backtest_id = backtest_response.json()["backtest_id"]

    # 3. 等待完成
    while True:
        status_response = client.get(f"/api/v1/backtest/{backtest_id}/status")
        if status_response.json()["status"] == "completed":
            break
        time.sleep(1)

    # 4. 获取结果
    result_response = client.get(f"/api/v1/backtest/{backtest_id}/result")
    assert result_response.status_code == 200
    assert result_response.json()["summary"]["total_return"] is not None
```

#### 8.2 性能测试

**测试场景**：
- 大数据量回测（10年日线数据）
- 并发请求测试（多个回测同时运行）
- 缓存命中率测试

---

## 4. 开发流程规范

### 4.1 TDD 红-绿-重构循环

```
🔴 RED   → 编写失败的测试
🟢 GREEN → 编写最少代码使测试通过
🔵 REFACTOR → 重构代码保持测试通过
```

### 4.2 分支管理

```bash
# 创建 worktree
cd /Users/maofengning/work/project/aicoding/ai-quant
git worktree add .claude/worktrees/backend-impl -b feature/backend-impl

# 开发流程
cd .claude/worktrees/backend-impl
# 每个 Phase 完成后 commit
git add .
git commit -m "feat(phase1): implement domain models with TDD"

# Phase 完成后推送
git push origin feature/backend-impl
```

### 4.3 测试覆盖率要求

- **单元测试覆盖率**: ≥ 80%
- **关键模块覆盖率**: ≥ 90% (engine, indicators, adapters)
- **集成测试**: 覆盖所有 API 端点

```bash
# 运行测试并生成覆盖率报告
pytest --cov=app --cov-report=html --cov-report=term
```

### 4.4 代码质量检查

```bash
# 代码格式化
ruff format app/ tests/

# 代码检查
ruff check app/ tests/

# 类型检查
mypy app/
```

---

## 5. API 契约对接

### 5.1 OpenAPI 规范生成

FastAPI 自动生成 OpenAPI 文档：

```python
# app/main.py
app = FastAPI(
    title="AI Quant Backend API",
    version="1.0.0",
    description="量化回测平台后端 API",
    docs_url="/docs",
    openapi_url="/openapi.json"
)
```

访问 `http://localhost:8000/docs` 查看交互式文档

### 5.2 导出 API 契约

```bash
# 启动服务
uvicorn app.main:app --reload

# 导出 OpenAPI schema
curl http://localhost:8000/openapi.json > docs/api-contract.yaml
```

前端团队基于此文件生成 TypeScript 类型和 Mock 数据

---

## 6. 时间估算

| Phase | 模块 | 工作量 | 依赖 |
|-------|------|-------|------|
| Phase 0 | 项目初始化 | 1天 | - |
| Phase 1 | 数据模型层 | 2天 | Phase 0 |
| Phase 2 | 数据适配器层 | 3天 | Phase 1 |
| Phase 3 | 核心引擎层 | 5天 | Phase 1, 2 |
| Phase 4 | API 路由层 | 4天 | Phase 3 |
| Phase 5 | 业务服务层 | 3天 | Phase 3, 4 |
| Phase 6 | 高级功能 | 3天 | Phase 5 |
| Phase 7 | 错误处理与日志 | 2天 | Phase 4 |
| Phase 8 | 集成测试与优化 | 2天 | 所有 Phase |

**总计**: 约 25 个工作日（1 人月）

---

## 7. 里程碑验收标准

### Milestone 1: 核心引擎可用 (Phase 1-3 完成)
- ✅ 所有单元测试通过
- ✅ 可以运行简单策略回测
- ✅ 技术指标计算正确
- ✅ 数据缓存正常工作

### Milestone 2: API 服务可用 (Phase 4-5 完成)
- ✅ 所有 API 端点测试通过
- ✅ 可以通过 HTTP 接口启动回测
- ✅ OpenAPI 文档生成完整

### Milestone 3: 功能完整 (Phase 6-8 完成)
- ✅ 参数优化功能可用
- ✅ 集成测试全部通过
- ✅ 代码覆盖率达标
- ✅ 性能测试通过

---

## 8. 风险与对策

| 风险 | 影响 | 对策 |
|-----|------|------|
| akshare/ccxt API 变更 | 数据获取失败 | 适配器模式解耦，版本锁定 |
| 大数据量性能问题 | 回测慢 | 使用 Parquet、向量化计算、并行优化 |
| 策略代码安全问题 | 恶意代码执行 | AST 解析限制、沙箱执行（可选） |
| 异步任务管理复杂 | 状态不一致 | 使用成熟的任务队列（Celery） |

---

## 9. 后续扩展预留

### 9.1 实盘交易接口
- `LiveEngine(Engine)` 继承基类
- 订单状态同步机制
- 风控模块

### 9.2 AI 功能
- `on_event` 事件系统对接 AI 信号
- 强化学习参数优化
- LLM 策略生成

### 9.3 高频回测
- Tick 级别数据支持
- 更精细的滑点模型
- 微观市场结构模拟

---

## 10. 参考资料

- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [pytest 文档](https://docs.pytest.org/)
- [akshare 文档](https://akshare.akfamily.xyz/)
- [CCXT 文档](https://docs.ccxt.com/)
- [Optuna 文档](https://optuna.readthedocs.io/)
