# Verified Track Record — Integrity Methodology

Public hub for **how** performance is measured — not marketing Sharpe ratios without context.

## Goals

1. Prevent lookahead and overfitting narratives in public claims
2. Enable third-party replay of **methodology** (not proprietary alpha)
3. Timestamp reports for audit trail

## Report bundle (per promotion gate)

Each walk-forward or paper promotion produces a bundle:

```
reports/
  {run_id}/
    manifest.json      # hashes, git sha, data snapshot ids
    metrics.json       # Sharpe, max DD, turnover (redacted symbols optional)
    config.yaml        # lag, fees, slippage model (no secrets)
    signature.asc      # optional GPG signature
```

## manifest.json schema

```json
{
  "run_id": "wf-2026-06-01-a1b2",
  "created_at": "2026-06-10T15:00:00Z",
  "git_sha": "abc123",
  "data_snapshots": ["sha256:..."],
  "bar_lag": 1,
  "lookahead_checks_passed": true
}
```

## Lookahead checklist (automated)

- [ ] Feature timestamps ≤ decision bar close
- [ ] Train/test windows non-overlapping
- [ ] Corporate actions joined as-of
- [ ] No same-bar fill unless explicitly modeled

## Publication policy

| Allowed publicly | Not allowed |
| ---------------- | ----------- |
| Methodology docs | Live PnL curves with $ amounts |
| Redacted metric ranges | Exchange account screenshots |
| Signed manifest hashes | API keys |

## Future: timestamp authority

- RFC 3161 timestamping of `manifest.json` via public TSA
- On-chain hash anchor (optional, DeFi research thread)

## Related

- [Data pipeline patterns](./architecture/data-pipeline-patterns.md)
- [OMS / RMS / kill-switch](./architecture/oms-rms-kill-switch.md)
