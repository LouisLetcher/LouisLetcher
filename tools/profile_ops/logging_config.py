"""Structured logging with trace_id correlation for profile_ops."""

from __future__ import annotations

import json
import logging
import sys
from typing import Any

from opentelemetry import trace


def get_trace_id() -> str:
    span = trace.get_current_span()
    ctx = span.get_span_context()
    if ctx.trace_id:
        return format(ctx.trace_id, "032x")
    return "0" * 32


class TraceJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "trace_id": get_trace_id(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=True)


def configure_logging(level: int = logging.INFO) -> None:
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(TraceJsonFormatter())
    root = logging.getLogger("profile_ops")
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)
    root.propagate = False


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"profile_ops.{name}")
