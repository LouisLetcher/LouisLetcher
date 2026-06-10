# Manuel H.

**Data engineer** building measurement systems for ads — and execution systems for markets.

Munich · [VollcomDigital](https://github.com/VollcomDigital) · Python · BigQuery · Pine Script

I spent a decade in **MarTech & AdTech** (Google Ads, Meta, programmatic) building attribution, pipelines, and ML for performance marketing. Now I apply that same rigor — idempotent data, no lookahead, hard risk limits — to **quantitative trading** and **DeFi** infrastructure.

**Public work:** [quant-pine](https://github.com/LouisLetcher/quant-pine) · [cloudflare-control-plane](https://github.com/LouisLetcher/cloudflare-control-plane) · [docs portal](https://louisletcher.github.io/LouisLetcher/)

---

## What I build

| | |
| --- | --- |
| **[quant-pine](https://github.com/LouisLetcher/quant-pine)** | Pine Script strategies & indicators — the research layer for systematic trading |
| **[cloudflare-control-plane](https://github.com/LouisLetcher/cloudflare-control-plane)** | Edge security for webhooks & APIs — WAF, Workers, Terraform |
| **quant-system** *(private)* | Multi-asset platform: 8+ data feeds, backtesting, paper/live execution with OMS/RMS split → [architecture docs](./docs/architecture/quant-system-overview.md) |

```mermaid
flowchart LR
  A[Pine signal] --> B[Backtest]
  B --> C[RMS gate]
  C --> D[OMS / live]
```

Most teams treat ads measurement and trade execution as separate worlds. I work at the overlap — where **attribution lag** looks a lot like **bar lag**, and **budget caps** look a lot like **position limits**.

→ [MarTech → Quant series](./docs/community/martech-to-quant.md) · [OMS / kill-switch design](./docs/architecture/oms-rms-kill-switch.md)

---

## Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-PostgreSQL-4479A1?style=flat-square&logo=postgresql&logoColor=white)
![GCP](https://img.shields.io/badge/GCP-4285F4?style=flat-square&logo=googlecloud&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazonaws&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-844FBA?style=flat-square&logo=terraform&logoColor=white)

BigQuery · dbt · Polars · ML / forecasting · DeFi · Cloudflare Workers

---

## Activity

<!-- PULSE:START -->
See [public changelog](./docs/CHANGELOG-PUBLIC.md) for weekly repository activity (auto-generated).
<!-- PULSE:END -->

![GitHub followers](https://img.shields.io/github/followers/LouisLetcher?style=flat-square)
![quant-pine stars](https://img.shields.io/github/stars/LouisLetcher/quant-pine?style=flat-square)

---

## Connect

[![Medium](https://img.shields.io/badge/Medium-@louisletcher-000000?style=flat-square&logo=medium)](https://medium.com/@louisletcher)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Manuel%20H.-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/feed?nis=true)
[![Collaborate](https://img.shields.io/badge/Collaborate-open%20issue-238636?style=flat-square&logo=github)](https://github.com/LouisLetcher/LouisLetcher/issues/new?template=collaboration.yml)

Quant infra, data pipelines, Pine Script, or MarTech measurement — [open an issue](https://github.com/LouisLetcher/LouisLetcher/issues/new?template=collaboration.yml) to start a conversation.

---

> “Data is a tool for empowerment, not just measurement.”
