from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import httpx
import pytest
import respx

from profile_ops.pulse_generator import (
    PULSE_END,
    PULSE_START,
    fetch_repo_activity,
    generate_pulse_file,
    render_pulse_section,
    upsert_pulse_markers,
    _parse_github_ts,
)
from profile_ops.pulse_generator import RepoActivity


def test_parse_github_ts_z_suffix() -> None:
    ts = _parse_github_ts("2026-06-10T12:00:00Z")
    assert ts.tzinfo is not None
    assert ts.year == 2026


def test_upsert_pulse_markers_idempotent() -> None:
    base = f"{PULSE_START}\nold\n{PULSE_END}"
    once = upsert_pulse_markers(base, "new")
    twice = upsert_pulse_markers(once, "new")
    assert once == twice
    assert "new" in once
    assert "old" not in once


def test_upsert_pulse_appends_when_missing_markers() -> None:
    content = "# Title\n"
    out = upsert_pulse_markers(content, "section")
    assert PULSE_START in out
    assert PULSE_END in out
    assert "section" in out


def test_render_pulse_section_includes_repos() -> None:
    now = datetime(2026, 6, 10, 12, 0, tzinfo=UTC)
    activities = [
        RepoActivity(
            name="quant-pine",
            description="Pine scripts",
            stars=19,
            pushed_at=now,
            html_url="https://github.com/LouisLetcher/quant-pine",
        )
    ]
    text = render_pulse_section(activities, generated_at=now)
    assert "quant-pine" in text
    assert "19" in text


@respx.mock
def test_fetch_repo_activity_filters_future_pushed_at() -> None:
    frozen_now = datetime(2026, 6, 10, 12, 0, tzinfo=UTC)
    future = "2026-12-31T00:00:00Z"
    past = "2026-06-01T00:00:00Z"
    respx.get("https://api.github.com/repos/LouisLetcher/future-repo").mock(
        return_value=httpx.Response(
            200,
            json={
                "name": "future-repo",
                "description": "x",
                "stargazers_count": 0,
                "pushed_at": future,
                "html_url": "https://github.com/LouisLetcher/future-repo",
            },
        )
    )
    respx.get("https://api.github.com/repos/LouisLetcher/ok-repo").mock(
        return_value=httpx.Response(
            200,
            json={
                "name": "ok-repo",
                "description": "y",
                "stargazers_count": 1,
                "pushed_at": past,
                "html_url": "https://github.com/LouisLetcher/ok-repo",
            },
        )
    )
    with httpx.Client() as client:
        activities = fetch_repo_activity(
            "LouisLetcher",
            ("future-repo", "ok-repo"),
            now=frozen_now,
            client=client,
        )
    names = {a.name for a in activities}
    assert "ok-repo" in names
    assert "future-repo" not in names


@respx.mock
def test_generate_pulse_file_writes_markers(tmp_path: Path) -> None:
    out = tmp_path / "CHANGELOG-PUBLIC.md"
    out.write_text("# Public Changelog\n")
    respx.get("https://api.github.com/repos/LouisLetcher/LouisLetcher").mock(
        return_value=httpx.Response(
            200,
            json={
                "name": "LouisLetcher",
                "description": "profile",
                "stargazers_count": 0,
                "pushed_at": "2026-06-01T00:00:00Z",
                "html_url": "https://github.com/LouisLetcher/LouisLetcher",
            },
        )
    )
    respx.get("https://api.github.com/repos/LouisLetcher/quant-pine").mock(
        return_value=httpx.Response(
            200,
            json={
                "name": "quant-pine",
                "description": "pine",
                "stargazers_count": 19,
                "pushed_at": "2026-06-01T00:00:00Z",
                "html_url": "https://github.com/LouisLetcher/quant-pine",
            },
        )
    )
    respx.get("https://api.github.com/repos/LouisLetcher/cloudflare-control-plane").mock(
        return_value=httpx.Response(
            200,
            json={
                "name": "cloudflare-control-plane",
                "description": "cf",
                "stargazers_count": 0,
                "pushed_at": "2026-06-01T00:00:00Z",
                "html_url": "https://github.com/LouisLetcher/cloudflare-control-plane",
            },
        )
    )
    frozen = datetime(2026, 6, 10, tzinfo=UTC)
    generate_pulse_file(out, now=frozen)
    text = out.read_text()
    assert PULSE_START in text
    assert "quant-pine" in text


def test_fetch_repo_activity_raises_on_http_error() -> None:
    with respx.mock:
        respx.get("https://api.github.com/repos/o/r").mock(return_value=httpx.Response(500))
        with httpx.Client() as client:
            with pytest.raises(httpx.HTTPStatusError):
                fetch_repo_activity("o", ("r",), client=client)
