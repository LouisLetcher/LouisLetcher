"""CLI entrypoint for profile_ops."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from profile_ops.link_checker import check_links
from profile_ops.logging_config import configure_logging, get_logger
from profile_ops.pulse_generator import generate_pulse_file
from profile_ops.telemetry import init_tracer

logger = get_logger("cli")


def _cmd_check_links(args: argparse.Namespace) -> int:
    tracer = init_tracer()
    root = Path(args.root).resolve()
    with tracer.start_as_current_span("cli.check_links"):
        results = check_links(root, check_external=not args.skip_external)
    failed = [r for r in results if not r.ok]
    for item in failed:
        logger.error("link failed: %s (%s)", item.url, item.error)
    if failed:
        logger.error("link check failed", extra={"failed_count": len(failed)})
        return 1
    logger.info("link check passed", extra={"checked": len(results)})
    return 0


def _cmd_generate_pulse(args: argparse.Namespace) -> int:
    tracer = init_tracer()
    output = Path(args.output).resolve()
    with tracer.start_as_current_span("cli.generate_pulse"):
        generate_pulse_file(output)
    return 0


def main(argv: list[str] | None = None) -> int:
    configure_logging()
    parser = argparse.ArgumentParser(prog="profile-ops")
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check-links", help="Validate local and external links")
    check.add_argument("--root", default=".", help="Repository root")
    check.add_argument("--skip-external", action="store_true", help="Skip HTTP checks")
    check.set_defaults(func=_cmd_check_links)

    pulse = sub.add_parser("generate-pulse", help="Update CHANGELOG-PUBLIC.md pulse section")
    pulse.add_argument("--output", default="docs/CHANGELOG-PUBLIC.md")
    pulse.set_defaults(func=_cmd_generate_pulse)

    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
