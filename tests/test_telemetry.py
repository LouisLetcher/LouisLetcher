from __future__ import annotations

import json
import logging

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from profile_ops.logging_config import TraceJsonFormatter, configure_logging, get_trace_id
from profile_ops.telemetry import init_tracer


def test_trace_id_from_active_span() -> None:
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer("test")
    with tracer.start_as_current_span("span-a"):
        tid = get_trace_id()
        assert len(tid) == 32
        assert tid != "0" * 32


def test_json_formatter_includes_trace_id() -> None:
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer("test")
    record = logging.LogRecord("n", logging.INFO, "", 0, "hello", (), None)
    with tracer.start_as_current_span("log-span"):
        line = TraceJsonFormatter().format(record)
        payload = json.loads(line)
        assert payload["message"] == "hello"
        assert "trace_id" in payload
        assert len(payload["trace_id"]) == 32


def test_init_tracer_singleton() -> None:
    a = init_tracer("profile-ops-test")
    b = init_tracer("profile-ops-test")
    assert a is b


def test_configure_logging_emits_json(capsys) -> None:
    configure_logging()
    log = logging.getLogger("profile_ops.test_emit")
    log.info("structured")
    captured = capsys.readouterr()
    assert "trace_id" in captured.err
