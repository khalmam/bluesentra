"""Response envelope renderer (ADR-013).

Successful responses are wrapped as ``{"success": true, "data": ..., "meta": {}}``.
Views that return raw GeoJSON opt out by setting ``raw_geojson = True``.
"""

from collections.abc import Mapping
from typing import Any

from rest_framework.renderers import JSONRenderer


def is_envelope(data: Any) -> bool:
    """Return True when the payload is already an envelope."""
    return isinstance(data, dict) and isinstance(data.get("success"), bool)


class EnvelopeJSONRenderer(JSONRenderer):
    """Wrap successful JSON responses in the standard envelope."""

    def render(
        self,
        data: Any,
        accepted_media_type: str | None = None,
        renderer_context: Mapping[str, Any] | None = None,
    ) -> bytes:
        context = renderer_context or {}
        view = context.get("view")
        response = context.get("response")

        if response is None or data is None or getattr(view, "raw_geojson", False):
            return super().render(data, accepted_media_type, renderer_context)
        if is_envelope(data):
            return super().render(data, accepted_media_type, renderer_context)

        envelope = {"success": True, "data": data, "meta": {}}
        return super().render(envelope, accepted_media_type, renderer_context)
