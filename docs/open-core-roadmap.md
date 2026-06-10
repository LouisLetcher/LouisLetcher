# Open-Core Roadmap — quant-system

HashiCorp-style split: **public harness**, **private alpha**.

## Tiers

| Tier | Visibility | Contents |
| ---- | ---------- | -------- |
| **Core SDK** | Public (future repo) | Data adapters, validation, backtest engine, OTel hooks |
| **Strategies** | Private | Signal logic, hyperparameters, live configs |
| **Execution** | Private | OMS/RMS, credentials, kill-switch thresholds |

## Phase A — Extract adapters (Q3)

- Yahoo, Alpha Vantage adapters with Pydantic models
- Deterministic replay from Parquet snapshots
- pytest suite with mocked HTTP (respx)

## Phase B — Backtest harness (Q4)

- Vectorized engine with configurable bar lag
- Walk-forward CLI
- Report generator (HTML + JSON metrics)

## Phase C — Paper OMS interface (Q1 next)

- Abstract `ExecutionSink` protocol
- Paper sink with slippage model
- Reconciliation loop tests

## What stays private

- Live exchange keys and wallet signers
- Proprietary signals and portfolio weights
- Production kill-switch thresholds

## Contribution model

1. Discuss in [Collaboration issue](https://github.com/LouisLetcher/LouisLetcher/issues/new?template=collaboration.yml)
2. PR to public SDK repo (when published)
3. CLA for strategy contributors (optional)

## Success metrics

| Metric | Target |
| ------ | ------ |
| Adapter test coverage | >80% |
| Replay determinism | Bit-identical on re-run |
| Docs | Every public module has architecture note |

## Related

- [Case study](./case-studies/quant-system.md)
- [Signal marketplace](./signal-marketplace.md)
