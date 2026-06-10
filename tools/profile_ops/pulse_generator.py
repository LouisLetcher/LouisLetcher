"""Weekly public activity pulse — idempotent, no future-dated events."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import httpx
from opentelemetry import trace

from profile_ops.logging_config import get_logger

logger = get_logger("pulse_generator")
tracer = trace.get_tracer("profile_ops.pulse_generator")

PULSE_START = "<!-- PULSE-AUTO:START -->"
PULSE_END = "<!-- PULSE-AUTO:END -->"

PUBLIC_REPOS = (
    "LouisLetcher",
    "quant-pine",
    "cloudflare-control-plane",
)


@dataclass(frozen=True)
class RepoActivity:
    name: str
    description: str
    stars: int
    pushed_at: datetime
    html_url: str


def _parse_github_ts(value: str) -> datetime:
    """Parse GitHub ISO timestamp; always timezone-aware UTC."""
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value).astimezone(UTC)


def fetch_repo_activity(
    owner: str,
    repos: tuple[str, ...],
    *,
    now: datetime | None = None,
    client: httpx.Client | None = None,
) -> list[RepoActivity]:
    """
    Fetch public repo metadata. Filters out events after `now` to prevent
    lookahead bias when testing with frozen clocks.
    """
    now = now or datetime.now(tz=UTC)
    with tracer.start_as_current_span("pulse_generator.fetch_repo_activity") as span:
        span.set_attribute("owner", owner)
        span.set_attribute("repo_count", len(repos))
        owns_client = client is None
        http = client or httpx.Client(timeout=20.0)
        activities: list[RepoActivity] = []
        try:
            for repo in repos:
                with tracer.start_as_current_span("pulse_generator.fetch_one") as child:
                    child.set_attribute("repo", repo)
                    token = os.environ.get("GITHUB_TOKEN")
                    headers = {"Accept": "application/vnd.github+json"}
                    if token:
                        headers["Authorization"] = f"Bearer {token}"
                    url = f"https://api.github.com/repos/{owner}/{repo}"
                    response = http.get(url, headers=headers)
                    response.raise_for_status()
                    data = response.json()
                    pushed_at = _parse_github_ts(data["pushed_at"])
                    if pushed_at > now:
                        logger.warning(
                            "skipping future pushed_at (lookahead guard)",
                            extra={"repo": repo, "pushed_at": data["pushed_at"]},
                        )
                        continue
                    activities.append(
                        RepoActivity(
                            name=data["name"],
                            description=data.get("description") or "",
                            stars=int(data.get("stargazers_count", 0)),
                            pushed_at=pushed_at,
                            html_url=data["html_url"],
                        )
                    )
        finally:
            if owns_client:
                http.close()
        span.set_attribute("activities", len(activities))
        return activities


def render_pulse_section(activities: list[RepoActivity], *, generated_at: datetime) -> str:
    week_label = generated_at.strftime("%Y-%m-%d")
    lines = [
        f"_Last updated: {generated_at.strftime('%Y-%m-%d %H:%M UTC')} (automated)._",
        "",
        f"## Week of {week_label}",
        "",
    ]
    for item in sorted(activities, key=lambda a: a.name):
        lines.extend(
            [
                f"### [{item.name}]({item.html_url})",
                f"- {item.description or 'No description'}",
                f"- Stars: {item.stars} · Last push: {item.pushed_at.strftime('%Y-%m-%d')}",
                "",
            ]
        )
    return "\n".join(lines).rstrip()


def upsert_pulse_markers(content: str, section: str) -> str:
    """Idempotent: replacing existing auto block yields stable output."""
    block = f"{PULSE_START}\n{section}\n{PULSE_END}"
    pattern = re.compile(
        re.escape(PULSE_START) + r".*?" + re.escape(PULSE_END),
        flags=re.DOTALL,
    )
    if pattern.search(content):
        return pattern.sub(block, content, count=1)
    return content.rstrip() + "\n\n" + block + "\n"


def generate_pulse_file(
    output: Path,
    *,
    owner: str | None = None,
    repos: tuple[str, ...] = PUBLIC_REPOS,
    now: datetime | None = None,
    client: httpx.Client | None = None,
) -> str:
    owner = owner or os.environ.get("GITHUB_REPOSITORY_OWNER", "LouisLetcher")
    now = now or datetime.now(tz=UTC)
    with tracer.start_as_current_span("pulse_generator.generate_pulse_file") as span:
        span.set_attribute("output", str(output))
        activities = fetch_repo_activity(owner, repos, now=now, client=client)
        section = render_pulse_section(activities, generated_at=now)
        existing = output.read_text(encoding="utf-8") if output.exists() else "# Public Changelog\n"
        updated = upsert_pulse_markers(existing, section)
        output.write_text(updated, encoding="utf-8")
        logger.info("pulse written", extra={"path": str(output), "repos": len(activities)})
        return updated
