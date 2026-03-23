import type { Strategy } from '@/types/api'

export const mockStrategies: Strategy[] = [
  {
    strategy_id: 'strat_001',
    name: 'MA Crossover',
    code: `class MACrossover(Strategy):
    def on_bar(self, bar, engine):
        # Simple MA crossover strategy
        pass`,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z'
  },
  {
    strategy_id: 'strat_002',
    name: 'RSI Strategy',
    code: `class RSIStrategy(Strategy):
    def on_bar(self, bar, engine):
        # RSI-based strategy
        pass`,
    created_at: '2024-01-02T00:00:00Z',
    updated_at: '2024-01-02T00:00:00Z'
  }
]
