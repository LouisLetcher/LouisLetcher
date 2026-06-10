# Manuel H. · LouisLetcher

**Data Engineer** · MarTech / AdTech · Quantitative Trading · DeFi  
Munich · [@VollcomDigital](https://github.com/VollcomDigital)

Modular data pipelines, performance marketing measurement, and automated trading infrastructure — with institutional-grade risk controls.

---

## Proof

| Area | Public artifact |
| ---- | --------------- |
| TradingView research | [quant-pine](https://github.com/LouisLetcher/quant-pine) — Pine Script strategies & indicators |
| Edge / infra posture | [cloudflare-control-plane](https://github.com/LouisLetcher/cloudflare-control-plane) — Terraform + Workers |
| Quant platform (private) | [Architecture overview](./docs/architecture/quant-system-overview.md) · [Case study](./docs/case-studies/quant-system.md) |
| OMS / RMS / kill-switch | [Design note](./docs/architecture/oms-rms-kill-switch.md) |
| Writing | [Medium @louisletcher](https://medium.com/@louisletcher) |

---

## Projects

### [quant-pine](https://github.com/LouisLetcher/quant-pine) · Public

Pine Script strategies and indicators for TradingView — research front-end for algorithmic ideas.

| | |
| --- | --- |
| **Stack** | Pine Script v5/v6, TradingView |
| **Status** | Active · 19+ stars |
| **Deep dive** | [Signal marketplace map](./docs/signal-marketplace.md) |

```mermaid
flowchart LR
  A[Pine signal] --> B[Manual / alert]
  B --> C[quant-system backtest]
  C --> D[Paper / live OMS]
```

---

### [cloudflare-control-plane](https://github.com/LouisLetcher/cloudflare-control-plane) · Public

Terraform-managed Cloudflare stack: email routing, WAF lockdown, Worker KV, deploy tooling.

| | |
| --- | --- |
| **Stack** | Terraform, Python, Cloudflare Workers |
| **Status** | Active |
| **Why it matters** | Webhook and API endpoints for trading bots need edge hardening |

---

### quant-system · Private ([VollcomDigital](https://github.com/VollcomDigital))

Multi-asset quant platform: 8+ data sources, modular strategies, backtesting, and live execution with OMS/RMS separation.

| | |
| --- | --- |
| **Stack** | Python, Docker, Makefile |
| **Access** | Private org repository |
| **Public docs** | [Overview](./docs/architecture/quant-system-overview.md) · [Open-core roadmap](./docs/open-core-roadmap.md) · [Case study](./docs/case-studies/quant-system.md) |

> Core alpha and live credentials remain private. Public documentation describes architecture and safety patterns only.

---

## Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-PostgreSQL-4479A1?style=flat-square&logo=postgresql&logoColor=white)
![GCP](https://img.shields.io/badge/GCP-4285F4?style=flat-square&logo=googlecloud&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazonaws&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-844FBA?style=flat-square&logo=terraform&logoColor=white)

Data engineering · ML / predictive modeling · BigQuery / dbt · AdTech (Google Ads, Meta, programmatic) · DeFi · Cloudflare edge

---

## Activity

<!-- PULSE:START -->
See [public changelog](./docs/CHANGELOG-PUBLIC.md) for weekly repository activity (auto-generated).
<!-- PULSE:END -->

![GitHub followers](https://img.shields.io/github/followers/LouisLetcher?style=flat-square)
![GitHub stars quant-pine](https://img.shields.io/github/stars/LouisLetcher/quant-pine?style=flat-square&label=quant-pine%20stars)

---

## Connect

[![GitHub](https://img.shields.io/badge/GitHub-LouisLetcher-181717?style=flat-square&logo=github)](https://github.com/LouisLetcher)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Manuel%20H.-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/feed?nis=true)
[![Medium](https://img.shields.io/badge/Medium-@louisletcher-000000?style=flat-square&logo=medium)](https://medium.com/@louisletcher)
[![Collaboration](https://img.shields.io/badge/Collaborate-open%20an%20issue-238636?style=flat-square&logo=github)](https://github.com/LouisLetcher/LouisLetcher/issues/new?template=collaboration.yml)

**Collaboration:** [Open a collaboration issue](https://github.com/LouisLetcher/LouisLetcher/issues/new?template=collaboration.yml) · [Portal / docs](https://louisletcher.github.io/LouisLetcher/)

---

## Background

Over the past decade I've led teams building scalable, data-driven advertising solutions across **Google Ads, Meta, and programmatic** ecosystems. Recent work focuses on **quantitative trading**, **DeFi**, and the measurement rigor that bridges MarTech attribution with execution systems.

→ [MarTech → Quant crossover series](./docs/community/martech-to-quant.md)

---

> “Data is a tool for empowerment, not just measurement.”
