from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path

import httpx
import pytest
import respx

from profile_ops.link_checker import (
    LinkReference,
    check_links,
    extract_links,
    resolve_local_path,
)


def test_extract_links_finds_markdown_urls(tmp_path: Path) -> None:
    doc = tmp_path / "README.md"
    doc.write_text("[ok](./docs/a.md)\n[skip](mailto:x@y.com)\n[ext](https://example.com)\n")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "a.md").write_text("# A")

    refs = extract_links(tmp_path)
    urls = {r.url for r in refs}
    assert "./docs/a.md" in urls
    assert "https://example.com" in urls
    assert "mailto:x@y.com" not in urls


def test_resolve_local_relative_path(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    target = tmp_path / "docs" / "x.md"
    target.write_text("hi")
    resolved = resolve_local_path(tmp_path, "./docs/x.md", Path("README.md"))
    assert resolved is not None
    assert resolved.exists()


def test_resolve_local_missing_returns_none(tmp_path: Path) -> None:
    assert resolve_local_path(tmp_path, "./missing.md", Path("README.md")) is None


@respx.mock
def test_check_links_local_and_external(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "ok.md").write_text("# OK")
    (tmp_path / "README.md").write_text("[local](./docs/ok.md)\n[bad](./docs/nope.md)\n")
    respx.get("https://good.example/").mock(return_value=httpx.Response(200))
    respx.head("https://good.example/").mock(return_value=httpx.Response(200))
    respx.get("https://bad.example/").mock(return_value=httpx.Response(404))
    respx.head("https://bad.example/").mock(return_value=httpx.Response(404))
    (tmp_path / "links.md").write_text("[g](https://good.example/)\n[b](https://bad.example/)\n")

    results = check_links(tmp_path)
    by_url = {r.url: r for r in results}
    assert by_url["./docs/ok.md"].ok is True
    assert by_url["./docs/nope.md"].ok is False
    assert by_url["https://good.example/"].ok is True
    assert by_url["https://bad.example/"].ok is False


def test_check_links_idempotent_same_result(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text("[x](./b.md)\n")
    (tmp_path / "b.md").write_text("b")
    first = check_links(tmp_path, check_external=False)
    second = check_links(tmp_path, check_external=False)
    assert first == second


def test_check_links_skip_external(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text("[ext](https://unreachable.test/)\n")
    results = check_links(tmp_path, check_external=False)
    assert len(results) == 1
    assert results[0].ok is True


def test_extract_links_empty_repo(tmp_path: Path) -> None:
    assert extract_links(tmp_path) == []


def test_should_skip_template_placeholders() -> None:
    from profile_ops.link_checker import _should_skip

    assert _should_skip("{{ statics.style_css }}") is True
    assert _should_skip("https://example.com") is False


def test_link_reference_frozen() -> None:
    ref = LinkReference(source=Path("a.md"), url="u", line=1)
    with pytest.raises(FrozenInstanceError):
        ref.url = "other"  # type: ignore[misc]
