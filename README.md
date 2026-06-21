# Manuel H. — Data · AI · Quant Engineer

> I build **measurement systems for ads** and **execution systems for markets** — the same discipline (idempotent data, no lookahead, hard risk limits) applied to both.

Munich · [VollcomDigital](https://github.com/VollcomDigital) · [Docs portal](https://louisletcher.github.io/LouisLetcher/) · Python · BigQuery · Pine Script

A decade in **MarTech & AdTech** (Google Ads, Meta, programmatic) building attribution, data pipelines, and ML for performance marketing — now applying that same rigor to **quantitative trading** and **DeFi** infrastructure.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-PostgreSQL-4479A1?style=flat-square&logo=postgresql&logoColor=white)
![GCP](https://img.shields.io/badge/GCP-4285F4?style=flat-square&logo=googlecloud&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazonaws&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-844FBA?style=flat-square&logo=terraform&logoColor=white)

---

## What I do

Most teams treat **ads measurement** and **trade execution** as separate worlds. I work at the overlap — where **attribution lag** looks a lot like **bar lag**, and **budget caps** look a lot like **position limits**. The hard parts are the same: delayed labels, leakage control, and capital allocation under uncertainty.

```mermaid
flowchart LR
  A[Pine signal] --> B[Backtest]
  B --> C[RMS gate]
  C --> D[OMS / live]
```

---

## 🛠 Work with me — clients

I turn messy data into systems that make decisions you can trust in production.

| Capability | What you get |
| --- | --- |
| **Data platforms & pipelines** | BigQuery · dbt · Polars — idempotent, tested, observable (OpenTelemetry tracing) |
| **Measurement & attribution** | MMM, incrementality, server-side tagging, performance-marketing ML |
| **ML / forecasting** | Feature pipelines with leakage control and walk-forward validation |
| **Quant & execution infra** | Backtesting, OMS/RMS, paper↔live parity, drawdown kill-switches |
| **Edge security** | Cloudflare Workers · WAF · Terraform for webhooks & APIs |

→ [**Start an engagement**](https://github.com/LouisLetcher/LouisLetcher/issues/new?template=collaboration.yml) · browse the [architecture docs](./docs/index.md) to see how I work before we talk.

---

## 📈 Partner & invest — systematic trading

A multi-asset platform built risk-first, not backtest-first.

- **Breadth** — 8+ market-data feeds behind a shared validation layer ([case study](./docs/case-studies/quant-system.md)).
- **Promotion discipline** — walk-forward → paper → live; **no** backtest-to-live shortcuts.
- **Hard limits** — rolling-drawdown kill-switch with manual re-arm, explicit position caps ([OMS / RMS design](./docs/architecture/oms-rms-kill-switch.md)).
- **Verified track record** — signed manifests, automated lookahead checks, timestamped audit trail — methodology in the open, alpha kept private ([integrity methodology](./docs/verified-track-record.md)).

→ Confidential inquiries via [LinkedIn](https://www.linkedin.com/in/manuelheck) · read the [verified track-record methodology](./docs/verified-track-record.md) first.

---

## Selected work

| | |
| --- | --- |
| **[quant-pine](https://github.com/LouisLetcher/quant-pine)** | Pine Script strategies & indicators — the public research layer for systematic trading |
| **[cloudflare-control-plane](https://github.com/LouisLetcher/cloudflare-control-plane)** | Edge security for webhooks & APIs — WAF, Workers, Terraform |
| **quant-system** *(private)* | Multi-asset platform: 8+ data feeds, backtesting, paper/live execution with OMS/RMS split → [architecture](./docs/architecture/quant-system-overview.md) · [open-core roadmap](./docs/open-core-roadmap.md) |

Further reading: [MarTech → Quant series](./docs/community/martech-to-quant.md) · [data-pipeline patterns](./docs/architecture/data-pipeline-patterns.md) · [signal marketplace](./docs/signal-marketplace.md)

---

## How I work

- **Idempotent data** — same inputs, same outputs; re-runs are bit-identical.
- **No lookahead** — feature timestamps ≤ decision time, enforced by automated checks.
- **Hard risk limits** — bankroll caps and kill-switches are code, not intentions.
- **Tested & observable** — typed Python, pytest coverage gates, OpenTelemetry tracing end to end.

This profile hub itself is built that way — see the [`profile_ops`](./tools/profile_ops/cli.py) tooling (link validation + weekly pulse) with lint, type-check, and CI gates.

---

## Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-PostgreSQL-4479A1?style=flat-square&logo=postgresql&logoColor=white)
![GCP](https://img.shields.io/badge/GCP-4285F4?style=flat-square&logo=googlecloud&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazonaws&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-844FBA?style=flat-square&logo=terraform&logoColor=white)

BigQuery · dbt · Polars · ML / forecasting · DeFi · Cloudflare Workers · Pine Script

---

## Activity

<!-- PULSE:START -->
See the [public changelog](./docs/CHANGELOG-PUBLIC.md) for weekly repository activity (auto-generated).
<!-- PULSE:END -->

![GitHub followers](https://img.shields.io/github/followers/LouisLetcher?style=flat-square)
![quant-pine stars](https://img.shields.io/github/stars/LouisLetcher/quant-pine?style=flat-square)

---

## Connect

[![Medium](https://img.shields.io/badge/Medium-@louisletcher-000000?style=flat-square&logo=medium)](https://medium.com/@louisletcher)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Manuel%20H.-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/manuelheck)
[![Collaborate](https://img.shields.io/badge/Collaborate-open%20issue-238636?style=flat-square&logo=github)](https://github.com/LouisLetcher/LouisLetcher/issues/new?template=collaboration.yml)

**Clients:** quant infra, data pipelines, attribution/measurement, or Pine Script — [open an engagement issue](https://github.com/LouisLetcher/LouisLetcher/issues/new?template=collaboration.yml).
**Investors & partners:** reach out on [LinkedIn](https://www.linkedin.com/in/manuelheck) for confidential conversations.

---

> "Data is a tool for empowerment, not just measurement."
