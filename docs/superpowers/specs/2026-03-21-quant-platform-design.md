# 量化回测平台设计文档

## 1. 项目概述

### 1.1 目标
构建一个个人量化回测研究平台，支持策略开发、历史数据回测、绩效分析和参数优化。

### 1.2 核心需求
- **市场支持**：中国股票市场（A股）+ 加密货币
- **交互方式**：Web 图形界面
- **数据源**：免费公开数据（akshare + ccxt）
- **核心功能**：技术指标库、绩效分析报告、参数优化

### 1.3 扩展性预留
- **实盘交易**：Engine 基类抽象订单执行接口，未来 LiveEngine 继承即可接入
- **AI 功能**：on_event 方法支持外部信号注入，策略参数可被 AI 自动调整

---

## 2. 架构设计

### 2.1 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Frontend (Vue3)                       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  │ 策略编辑器 │ │ 回测配置  │ │ 结果可视化│ │ 参数优化  │        │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘        │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP/WebSocket
┌───────────────────────────▼─────────────────────────────────┐
│                    API Layer (FastAPI)                       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  │ /strategies│ │ /backtest │ │ /optimize │ │ /analysis │     │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘        │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    Core Engine (Python)                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  │ 回测引擎   │ │ 指标计算  │ │ 数据适配器│ │ 优化器    │        │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘        │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    Data Layer                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │ akshare (A股)│  │ ccxt (加密) │  │ Local Cache │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 设计原则
- **分层架构**：前端、API、引擎、数据四层清晰分离
- **模块化**：每个市场有独立的数据适配器，策略与市场解耦
- **本地优先**：数据缓存到本地，减少网络请求

---

## 3. 核心模块设计

### 3.1 回测引擎

```python
# 核心抽象 - 为实盘交易预留接口
class Engine(ABC):
    """交易引擎基类 - 回测引擎和实盘引擎都继承此类"""

    @abstractmethod
    def submit_order(self, order: Order) -> OrderResult:
        """提交订单 - 回测模拟执行，实盘真实执行"""
        pass

    @abstractmethod
    def get_position(self, symbol: str) -> Position:
        """获取持仓"""
        pass

    @abstractmethod
    def get_portfolio(self) -> Portfolio:
        """获取组合状态"""
        pass

class BacktestEngine(Engine):
    """回测引擎"""
    def __init__(self, config: BacktestConfig):
        self.data_source = config.data_source
        self.commission_model = config.commission_model
        self.slippage_model = config.slippage_model

    def run(self, strategy: Strategy, start: date, end: date) -> BacktestResult:
        """运行回测"""
        pass
```

**扩展性设计：**
- `Engine` 基类抽象了订单执行接口，未来 `LiveEngine` 继承即可接入实盘
- 策略与引擎解耦，同一策略可用于回测和实盘

### 3.2 策略框架

```python
class Strategy(ABC):
    """策略基类"""

    def on_bar(self, bar: Bar, engine: Engine):
        """每根K线触发 - 可被 AI Agent 调用"""
        pass

    def on_tick(self, tick: Tick, engine: Engine):
        """每个 tick 触发（高频场景）"""
        pass

    def on_event(self, event: Event, engine: Engine):
        """自定义事件 - 预留给 AI 决策信号"""
        pass

# 用户编写策略示例
class MyStrategy(Strategy):
    def on_bar(self, bar, engine):
        if self.should_buy(bar):
            engine.submit_order(Order(side='buy', symbol=bar.symbol, quantity=100))
```

**AI 扩展预留：**
- `on_event` 方法支持外部信号注入（如 AI 模型的决策信号）
- 策略参数可被 AI 自动调整

### 3.3 数据适配器

```python
class DataAdapter(ABC):
    """数据源适配器基类"""

    @abstractmethod
    def fetch_bars(self, symbol: str, start: date, end: date,
                   timeframe: str) -> List[Bar]:
        pass

    @abstractmethod
    def get_symbols(self) -> List[str]:
        """获取可用标的列表"""
        pass

class AKShareAdapter(DataAdapter):
    """A股数据适配器 - akshare"""
    pass

class CCXTAdapter(DataAdapter):
    """加密货币适配器 - ccxt"""
    pass

class DataAdapterManager:
    """统一管理多数据源"""
    def get_adapter(self, market: MarketType) -> DataAdapter:
        return self._adapters[market]
```

**扩展性设计：**
- 新增市场只需实现新的 `DataAdapter`
- 统一的 `Bar` 数据结构，屏蔽不同数据源差异

---

## 4. 数据流与存储

### 4.1 数据流向

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  外部数据源   │────▶│  数据适配器   │────▶│  数据缓存层   │
│  akshare/    │     │  Adapter     │     │  SQLite/     │
│  ccxt        │     │              │     │  Parquet     │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                 │
                                                 ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  回测结果     │◀────│  回测引擎     │◀────│  标准化数据   │
│  SQLite      │     │  Engine      │     │  Bar/Tick    │
└──────────────┘     └──────────────┘     └──────────────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐
│  绩效分析     │────▶│  前端可视化   │
│  Analyzer    │     │  Charts      │
└──────────────┘     └──────────────┘
```

### 4.2 存储方案

| 数据类型 | 存储格式 | 位置 | 说明 |
|---------|---------|------|------|
| 行情数据 | Parquet | `data/cache/{market}/{symbol}/` | 列式存储，查询快 |
| 策略文件 | Python 文件 | `strategies/{user}/` | 版本控制友好 |
| 回测结果 | SQLite | `data/backtest.db` | 结构化查询 |
| 系统配置 | YAML/JSON | `config/` | 易读易改 |

### 4.3 目录结构

```
ai-quant/
├── backend/                 # FastAPI 后端
│   ├── api/                 # API 路由
│   ├── engine/              # 回测引擎
│   ├── adapters/            # 数据适配器
│   ├── models/              # 数据模型
│   └── services/            # 业务逻辑
├── frontend/                # Vue3 前端
│   ├── src/
│   │   ├── views/           # 页面
│   │   ├── components/      # 组件
│   │   └── stores/          # 状态管理
├── strategies/              # 用户策略存储
├── data/                    # 数据存储
│   ├── cache/              # 行情缓存
│   └── backtest.db         # 回测结果
└── config/                  # 配置文件
```

---

## 5. 错误处理与测试

### 5.1 错误处理策略

```python
# 分层错误处理
class QuantError(Exception):
    """基础异常"""
    pass

class DataError(QuantError):
    """数据层错误：数据源不可用、数据格式错误"""
    pass

class EngineError(QuantError):
    """引擎层错误：回测执行失败、订单异常"""
    pass

class StrategyError(QuantError):
    """策略层错误：策略语法错误、运行时异常"""
    pass

# API 层统一处理
@app.exception_handler(QuantError)
async def quant_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"code": exc.code, "message": str(exc)}
    )
```

**错误分级：**

| 级别 | 场景 | 处理方式 |
|-----|------|---------|
| 警告 | 数据缺失部分字段、缓存过期 | 记录日志，降级处理 |
| 错误 | 数据源不可用、回测参数无效 | 返回错误，用户可重试 |
| 致命 | 系统配置丢失、存储损坏 | 停止服务，提示修复 |

### 5.2 测试策略

```
测试金字塔
    ┌───────────┐
    │   E2E     │  ← 完整回测流程（少量）
    ├───────────┤
    │ 集成测试   │  ← API + 数据源 + 引擎（中等）
    ├───────────┤
    │ 单元测试   │  ← 指标计算、订单逻辑、数据转换（大量）
    └───────────┘
```

**核心测试覆盖：**

| 模块 | 测试内容 | 工具 |
|-----|---------|------|
| 指标计算 | MA/RSI/MACD 正确性 | pytest + numpy 测试数据 |
| 回测引擎 | 订单执行、持仓计算、手续费扣除 | pytest + mock 数据 |
| 数据适配器 | 数据获取、格式转换、缓存逻辑 | pytest + VCR.py 录制 |
| API 接口 | 请求参数、响应格式、错误码 | pytest + httpx |

---

## 6. 技术栈

### 6.1 后端技术栈

| 领域 | 选型 | 理由 |
|-----|------|------|
| Web 框架 | FastAPI | 异步、高性能、自动文档 |
| 数据处理 | pandas, numpy | 量化标配，生态成熟 |
| 技术指标 | ta-lib / pandas-ta | 专业指标库 |
| 数据源-A股 | akshare | 免费开源，A股覆盖全 |
| 数据源-加密 | ccxt | 统一 100+ 交易所 API |
| 数据存储 | SQLite + Parquet | 轻量、无需部署 |
| 参数优化 | Optuna | 现代、易用、支持并行 |
| 任务队列 | asyncio / Celery | 回测异步执行 |

### 6.2 前端技术栈

| 领域 | 选型 | 理由 |
|-----|------|------|
| 框架 | Vue3 + TypeScript | 响应式、类型安全 |
| 构建 | Vite | 快速开发体验 |
| 状态管理 | Pinia | Vue3 官方推荐 |
| UI 组件 | Element Plus | 中文友好、组件丰富 |
| 图表 | ECharts | 金融图表支持好 |
| 代码编辑器 | Monaco Editor | 策略代码编辑，VS Code 同款 |
| HTTP | Axios | 成熟稳定 |

### 6.3 核心依赖

**后端 (pyproject.toml):**
```toml
[project]
dependencies = [
    "fastapi>=0.110.0",
    "uvicorn>=0.27.0",
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "akshare>=1.12.0",
    "ccxt>=4.0.0",
    "optuna>=3.5.0",
    "pydantic>=2.0.0",
]
```

**前端 (package.json):**
```json
{
  "dependencies": {
    "vue": "^3.4.0",
    "pinia": "^2.1.0",
    "element-plus": "^2.5.0",
    "echarts": "^5.5.0",
    "monaco-editor": "^0.47.0",
    "axios": "^1.6.0"
  }
}
```

---

## 7. API 设计

### 7.1 RESTful API 概览

```
/api/v1
├── /data                    # 数据接口
│   ├── GET  /symbols        # 获取可用标的
│   ├── GET  /bars           # 获取K线数据
│   └── POST /sync           # 同步/更新缓存
│
├── /strategies              # 策略管理
│   ├── GET  /               # 列出策略
│   ├── POST /               # 创建策略
│   ├── GET  /{id}           # 获取策略详情
│   ├── PUT  /{id}           # 更新策略
│   └── DELETE /{id}         # 删除策略
│
├── /backtest                # 回测执行
│   ├── POST /run            # 启动回测
│   ├── GET  /{id}/status    # 查询回测状态
│   └── GET  /{id}/result    # 获取回测结果
│
├── /optimize                # 参数优化
│   ├── POST /start          # 启动优化
│   ├── GET  /{id}/progress  # 优化进度
│   └── GET  /{id}/best      # 最优参数
│
└── /analysis                # 绩效分析
    └── GET  /{backtest_id}  # 详细分析报告
```

### 7.2 核心接口示例

**启动回测：**
```json
// POST /api/v1/backtest/run
{
    "strategy_id": "strat_001",
    "symbols": ["000001.SZ", "BTC/USDT"],
    "start_date": "2023-01-01",
    "end_date": "2024-01-01",
    "initial_capital": 100000,
    "commission": 0.0003,
    "slippage": 0.0001
}

// Response
{
    "backtest_id": "bt_20240321_001",
    "status": "running"
}
```

**获取回测结果：**
```json
// GET /api/v1/backtest/{id}/result
{
    "backtest_id": "bt_20240321_001",
    "status": "completed",
    "summary": {
        "total_return": 0.23,
        "annual_return": 0.18,
        "max_drawdown": -0.12,
        "sharpe_ratio": 1.45,
        "win_rate": 0.58
    },
    "equity_curve": [],
    "trades": [],
    "daily_returns": []
}
```

### 7.3 WebSocket 实时通信

```
ws://localhost:8000/ws/backtest/{id}

// 回测进度推送
{
    "type": "progress",
    "current": 150,
    "total": 365,
    "message": "Processing 2023-05-30"
}

// 参数优化进度
{
    "type": "optimization",
    "trial": 42,
    "best_value": 1.52,
    "params": {"fast": 12, "slow": 26}
}
```

---

## 8. 扩展性设计

### 8.1 实盘交易扩展路径
1. 实现 `LiveEngine(Engine)` 类
2. 接入券商/交易所 API
3. 添加风控模块和订单状态同步
4. 前端增加实盘交易页面

### 8.2 AI 功能扩展路径
1. AI 信号生成器：通过 `on_event` 注入交易信号
2. 参数自动优化：AI Agent 调用优化 API
3. 策略代码生成：集成 LLM 生成策略模板
4. 智能分析：AI 解读回测结果，给出改进建议