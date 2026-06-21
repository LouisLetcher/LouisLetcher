from __future__ import annotations

from pathlib import Path

import pytest

from profile_ops.cli import main


def test_cli_check_links_local_only(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "a.md").write_text("[ok](./b.md)\n")
    (tmp_path / "b.md").write_text("b")
    monkeypatch.chdir(tmp_path)
    assert main(["check-links", "--root", ".", "--skip-external"]) == 0


def test_cli_check_links_failure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / "a.md").write_text("[bad](./missing.md)\n")
    monkeypatch.chdir(tmp_path)
    assert main(["check-links", "--root", ".", "--skip-external"]) == 1
