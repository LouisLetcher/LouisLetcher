# Security Policy

## Supported Versions

This repository is a public profile and documentation hub. Security updates apply to the `main` branch.

| Version | Supported |
| ------- | --------- |
| main    | Yes       |

## Reporting a Vulnerability

**Do not** open a public GitHub issue for security-sensitive reports.

1. Open a [private security advisory](https://github.com/LouisLetcher/LouisLetcher/security/advisories/new) on this repository, **or**
2. Contact via [GitHub Discussions — Security](https://github.com/LouisLetcher/LouisLetcher/discussions/categories/security) if advisories are unavailable.

Include:

- Description and impact
- Steps to reproduce
- Affected URLs or files
- Suggested remediation (optional)

**Response target:** acknowledgment within 72 hours; triage within 7 days.

## Scope

In scope:

- This repository (`LouisLetcher/LouisLetcher`)
- Documentation and automation under `.github/workflows/` and `tools/profile_ops/`
- GitHub Pages content served from `/docs`

Out of scope:

- Private repositories (e.g. `VollcomDigital/quant-system`) — report through org channels
- Third-party services (TradingView, Cloudflare, GitHub Stats mirrors)

## Safe Collaboration

- Never commit API keys, exchange credentials, or wallet private keys
- Pull requests that add secrets will be rejected
- Link integrity is validated in CI on every push to `main`
