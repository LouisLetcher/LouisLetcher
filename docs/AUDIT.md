# Repository Audit & Improvement Recommendations

_Audit date: 2026-06-21 · Scope: `LouisLetcher/LouisLetcher` (profile hub + `profile_ops` tooling)_

This document audits the repository's tooling, CI/CD, security posture, and
documentation, and recommends prioritized improvements. A subset of the
low-risk, high-value items has already been implemented in the same change set
(see [What changed in this PR](#what-changed-in-this-pr)).

## Executive summary

The repository is in good shape for a personal profile hub: the `profile_ops`
package is small, typed, tested (22 tests, ~92% coverage), and traced with
OpenTelemetry. The biggest gaps were in **developer-tooling enforcement**
(no linter/type-check gate), **supply-chain hygiene** (no dependency
automation, unpinned actions), and a few **correctness/reliability rough
edges** in the link checker and pulse generator. None are critical; most are
quick wins that match the "idempotent data, hard limits" rigor the profile
advertises.

Severity legend: 🔴 High · 🟠 Medium · 🟢 Low / polish

---

## Findings

### Tooling & code quality

- 🟠 **No lint or type-check gate in CI.** `pyproject.toml` configured pytest +
  coverage but no `ruff`/`mypy`, and no workflow enforced them. Two unused
  imports (`json` in `pulse_generator.py`, `io.StringIO` in
  `test_telemetry.py`) had already slipped in — exactly what a linter catches.
  _Status: fixed._
- 🟢 **O(n²) source lookup in `check_links`.** Each non-external URL did
  `next(r.source for r in refs if r.url == url)`, rescanning all refs per link.
  Replaced with a precomputed `dict`. _Status: fixed._
- 🟢 **Convoluted `_should_skip` control flow.** Simplified the trailing
  branch to a direct boolean return (behavior preserved, covered by tests).
  _Status: fixed._

### Reliability

- 🟠 **External link checks are bot-blocked / flaky.** `link-check.yml` runs the
  full external check on every push and PR to `main`. Requests were sent with
  no `User-Agent`, and the README links to hosts that reject anonymous
  automated requests (e.g. LinkedIn returns `999`, Medium can return `403`).
  This makes CI fail for reasons unrelated to the change under review.
  - _Partially fixed:_ requests now send an identifying `User-Agent`.
  - _Recommended next:_ treat transient/bot-block codes (`403`, `429`, `999`)
    as warnings rather than hard failures, add a small retry with backoff for
    `5xx`/timeouts, and consider running the **full external sweep on a
    schedule** while PR/push runs validate **local links only** (fast and
    deterministic). This keeps PR signal trustworthy.
- 🟢 **Telemetry always exports to the console.** `init_tracer` unconditionally
  installs a `ConsoleSpanExporter`, so every CLI run (including CI) prints span
  JSON to stdout. Consider gating the exporter behind an env var
  (`PROFILE_OPS_TRACE=1`) or supporting an OTLP endpoint, so default runs stay
  quiet.

### Security & supply chain

- 🟠 **No dependency automation.** No `dependabot.yml` meant pip deps and GitHub
  Actions were never updated automatically. _Status: fixed_ (weekly pip +
  github-actions updates).
- 🟠 **No code scanning.** For a profile that advertises edge-security work, a
  CodeQL workflow is table stakes. _Status: fixed_ (added `codeql.yml`).
- 🟢 **GitHub Actions pinned to mutable major tags** (`actions/checkout@v4`,
  etc.) rather than commit SHAs. Pinning to SHA (with Dependabot keeping them
  current) removes a tag-hijack vector. _Recommended._
- 🟢 **Unpinned Python dependencies** (`httpx>=0.27`, …) make builds
  non-reproducible. For a tool this small it is low risk, but a committed
  constraints/lock file (e.g. `uv.lock` or `pip-tools`) would make CI
  deterministic. _Recommended._
- 🟢 **`weekly-pulse.yml` pushes directly to `main`.** Works today, but if
  branch protection is ever enabled it will break silently. Consider opening a
  PR from the workflow (or a dedicated app token) instead of a direct push.

### Documentation

- 🟢 **Misleading changelog note.** `CHANGELOG-PUBLIC.md` claimed "older entries
  will append above this line," but `upsert_pulse_markers` **replaces** the
  marked block in place — no history is kept. _Status: fixed_ (note corrected).
- 🟢 **README pulse markers are inert.** The README has `PULSE:START/END`
  markers, but the generator only writes `PULSE-AUTO:START/END` in
  `docs/CHANGELOG-PUBLIC.md`. The README block is effectively static prose.
  This is fine as-is, but the markers invite confusion — either wire them up or
  drop them.
- 🟢 **No `LICENSE` file.** The repo is a public hub with reusable tooling but
  has no license, which by default means "all rights reserved" and discourages
  reuse. Recommend adding one explicitly (MIT or Apache-2.0 are common for this
  kind of tooling). _Left to the owner — license choice is a deliberate
  decision, not an automated one._
- 🟢 **No `CONTRIBUTING.md`.** The README and issue templates invite
  collaboration, but there is no contributor guide describing how to run
  `pytest`/`ruff`/`mypy` locally. A short guide would lower the bar.

---

## What changed in this PR

| Area | Change |
| ---- | ------ |
| Tooling | Added `ruff` + `mypy` config to `pyproject.toml` and a `lint.yml` workflow that runs both on push/PR |
| Tooling | Removed two unused imports flagged by `ruff` |
| Reliability | Link checker now sends an identifying `User-Agent`; `O(n²)` source lookup replaced with a map |
| Code quality | Simplified `_should_skip`; tightened the frozen-dataclass test to assert `FrozenInstanceError` |
| Security | Added `dependabot.yml` (pip + github-actions) and a CodeQL workflow |
| Docs | Corrected the misleading "append above" note in `CHANGELOG-PUBLIC.md`; added this audit |

All changes are covered by the existing suite: `ruff check`, `mypy`, and
`pytest` (22 passing, ~92% coverage) are green.

## Recommended next steps (prioritized)

1. 🟠 Split CI link checking: local links on every PR/push; full external sweep
   on a schedule, with retries and lenient handling of bot-block status codes.
2. 🟢 Add a `LICENSE` (owner decision) and a short `CONTRIBUTING.md`.
3. 🟢 Pin GitHub Actions to commit SHAs and let Dependabot bump them.
4. 🟢 Gate the OpenTelemetry console exporter behind an env var / OTLP endpoint.
5. 🟢 Add a committed lock/constraints file for reproducible installs.
