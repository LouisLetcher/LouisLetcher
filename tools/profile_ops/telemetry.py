"""OpenTelemetry tracer setup for profile_ops CLI."""

from __future__ import annotations

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

_PROVIDER: TracerProvider | None = None


def init_tracer(service_name: str = "profile-ops") -> trace.Tracer:
    global _PROVIDER
    if _PROVIDER is None:
        resource = Resource.create({"service.name": service_name})
        _PROVIDER = TracerProvider(resource=resource)
        _PROVIDER.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
        trace.set_tracer_provider(_PROVIDER)
    return trace.get_tracer(service_name)
