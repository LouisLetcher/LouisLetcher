# Quant System — Case Study (Public Summary)

## Context

Private repository: [VollcomDigital/quant-system](https://github.com/VollcomDigital/quant-system)  
Author: Manuel H. ([LouisLetcher](https://github.com/LouisLetcher))

## Problem statement

Retail and semi-pro quant stacks often collapse research, sizing, and execution into one script — leading to lookahead bugs, unbounded loops, and live capital exposed to un tested signals.

## Approach

1. **Modular adapters** for 8+ market data sources with shared validation layer
2. **Strategy plugins** output signals only; RMS applies bankroll and exposure rules
3. **Vectorized backtester** with explicit bar lag and walk-forward promotion
4. **OMS** with reconciliation loops and paper/live parity
5. **Kill switch** on rolling drawdown with manual re-arm

## Results (representative, redacted)

| Metric | Backtest window | Notes |
| ------ | --------------- | ----- |
| Instruments | Multi-asset | Equities, crypto adapters |
| Data vendors | 8+ | Yahoo, Alpha Vantage, others |
| Promotion path | Walk-forward → paper → live | No direct backtest → live |

Specific PnL and Sharpe figures are **not published** in this public hub. See [verified track record](../verified-track-record.md) for integrity methodology.

## Why private

- Live API credentials and proprietary alpha
- Open-core plan: public SDK for adapters + backtest harness ([roadmap](../open-core-roadmap.md))

## Artifacts you can inspect today

- [Architecture overview](../architecture/quant-system-overview.md)
- [OMS / RMS design](../architecture/oms-rms-kill-switch.md)
- Public research: [quant-pine](https://github.com/LouisLetcher/quant-pine)

## Collaborate

Interested in architecture review or adapter contributions? [Open a collaboration issue](https://github.com/LouisLetcher/LouisLetcher/issues/new?template=collaboration.yml).
