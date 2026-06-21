"""Extract and validate markdown / HTML links from repository files."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

import httpx
from opentelemetry import trace

from profile_ops.logging_config import get_logger

logger = get_logger("link_checker")
tracer = trace.get_tracer("profile_ops.link_checker")

MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
HTML_LINK_RE = re.compile(r"""href=["']([^"']+)["']""", re.IGNORECASE)

SKIP_SCHEMES = {"", "#"}
SKIP_PREFIXES = ("mailto:", "javascript:")

# Some hosts reject requests without a User-Agent; identify the checker explicitly.
USER_AGENT = "profile-ops-link-checker/0.1 (+https://github.com/LouisLetcher/LouisLetcher)"


@dataclass(frozen=True)
class LinkReference:
    source: Path
    url: str
    line: int


@dataclass(frozen=True)
class LinkCheckResult:
    url: str
    ok: bool
    status_code: int | None
    error: str | None


def _is_external(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"}


def _should_skip(url: str) -> bool:
    if "{{" in url or "}}" in url:
        return True
    if url.startswith(SKIP_PREFIXES):
        return True
    if url.startswith("#"):
        return True
    parsed = urlparse(url)
    if parsed.scheme in SKIP_SCHEMES and not url.startswith("/"):
        return False
    # Skip non-web schemes (tel:, ftp:, etc.); keep http(s) and relative paths.
    return bool(parsed.scheme) and parsed.scheme not in {"http", "https", ""}


def extract_links(root: Path, extensions: frozenset[str] = frozenset({".md", ".html", ".yml"})) -> list[LinkReference]:
    with tracer.start_as_current_span("link_checker.extract_links") as span:
        span.set_attribute("root", str(root))
        refs: list[LinkReference] = []
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            if any(part in {".git", ".venv", "venv", "_site", "node_modules"} for part in path.parts):
                continue
            if path.suffix.lower() not in extensions:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for line_no, line in enumerate(text.splitlines(), start=1):
                for match in MARKDOWN_LINK_RE.finditer(line):
                    url = match.group(1).strip()
                    if not _should_skip(url):
                        refs.append(LinkReference(source=path.relative_to(root), url=url, line=line_no))
                for match in HTML_LINK_RE.finditer(line):
                    url = match.group(1).strip()
                    if not _should_skip(url):
                        refs.append(LinkReference(source=path.relative_to(root), url=url, line=line_no))
        span.set_attribute("link_count", len(refs))
        logger.info("extracted links", extra={"link_count": len(refs)})
        return refs


def resolve_local_path(root: Path, url: str, source: Path) -> Path | None:
    if _is_external(url):
        return None

    clean = url.split("#")[0].split("?")[0].strip()
    if not clean:
        return None

    root_resolved = root.resolve()
    if clean.startswith("/"):
        candidate = (root_resolved / clean.lstrip("/")).resolve()
    else:
        candidate = (root_resolved / source.parent / clean).resolve()

    try:
        candidate.relative_to(root_resolved)
    except ValueError:
        return None

    if candidate.is_file():
        return candidate
    if candidate.is_dir() and (candidate / "index.md").is_file():
        return candidate / "index.md"
    return None


def check_links(
    root: Path,
    client: httpx.Client | None = None,
    *,
    check_external: bool = True,
) -> list[LinkCheckResult]:
    """Idempotent link validation: same inputs produce same pass/fail set."""
    with tracer.start_as_current_span("link_checker.check_links") as span:
        refs = extract_links(root)
        unique_urls = sorted({r.url for r in refs})
        span.set_attribute("unique_urls", len(unique_urls))
        # Map each URL to its first source once (avoids an O(n^2) rescan per link).
        source_by_url: dict[str, Path] = {}
        for ref in refs:
            source_by_url.setdefault(ref.url, ref.source)
        results: list[LinkCheckResult] = []
        owns_client = client is None
        http = client or httpx.Client(
            follow_redirects=True,
            timeout=15.0,
            headers={"User-Agent": USER_AGENT},
        )
        try:
            for url in unique_urls:
                with tracer.start_as_current_span("link_checker.check_one") as child:
                    child.set_attribute("url", url)
                    if _is_external(url):
                        if not check_external:
                            results.append(LinkCheckResult(url=url, ok=True, status_code=None, error=None))
                            continue
                        try:
                            response = http.head(url)
                            if response.status_code >= 400:
                                response = http.get(url)
                            ok = response.status_code < 400
                            results.append(
                                LinkCheckResult(
                                    url=url,
                                    ok=ok,
                                    status_code=response.status_code,
                                    error=None if ok else f"HTTP {response.status_code}",
                                )
                            )
                        except httpx.HTTPError as exc:
                            results.append(LinkCheckResult(url=url, ok=False, status_code=None, error=str(exc)))
                    else:
                        source = source_by_url[url]
                        local = resolve_local_path(root, url, source)
                        ok = local is not None
                        results.append(
                            LinkCheckResult(
                                url=url,
                                ok=ok,
                                status_code=None,
                                error=None if ok else "local path not found",
                            )
                        )
                    logger.info(
                        "checked link",
                        extra={"url": url, "ok": results[-1].ok},
                    )
        finally:
            if owns_client:
                http.close()
        span.set_attribute("failed", sum(1 for r in results if not r.ok))
        return results
