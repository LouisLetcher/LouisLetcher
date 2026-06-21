# Contributing

Thanks for your interest in this profile hub and its `profile_ops` tooling.
Most collaboration starts with a conversation — open a
[collaboration issue](https://github.com/LouisLetcher/LouisLetcher/issues/new?template=collaboration.yml)
before sending a large change.

## Local setup

Requires Python 3.12+.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Quality gates

CI runs these on every pull request; run them locally first:

```bash
ruff check tools tests          # lint + import order
mypy tools/profile_ops          # static type check
pytest -q --cov=profile_ops     # tests (coverage gate: 80%)
python -m profile_ops.cli check-links --root . --skip-external   # local link gate
```

The full external link sweep runs on a schedule, not on PRs — see
`.github/workflows/link-check-external.yml`.

## Pull requests

- Branch off `main`; keep changes focused and the diff readable.
- Match the surrounding style; add tests for new behavior in `profile_ops`.
- Make sure all quality gates above pass before requesting review.

## Security

Please do **not** open public issues for security-sensitive reports — follow
[`SECURITY.md`](./SECURITY.md). Pull requests that add secrets (API keys,
credentials, wallet keys) will be rejected.
