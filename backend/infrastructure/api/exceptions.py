"""Standard error envelope (ADR-013).

Errors are returned as ``{"success": false, "error": {"code", "message", "details"}}``
with meaningful HTTP status codes. Unhandled exceptions stay as server errors.
"""

from typing import Any

from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def api_exception_handler(exc: Exception, context: dict[str, Any]) -> Response | None:
    """Convert DRF exceptions to the BlueSentra error envelope."""
    response = drf_exception_handler(exc, context)
    if response is None:
        return None

    if isinstance(exc, ValidationError):
        code = "validation_error"
        message = "Validation failed."
        details: Any = response.data
    else:
        code = exc.default_code if isinstance(exc, APIException) else "error"
        data = response.data
        message = (
            str(data.get("detail", "Request failed."))
            if isinstance(data, dict)
            else "Request failed."
        )
        details = {}

    response.data = {
        "success": False,
        "error": {"code": code, "message": message, "details": details},
    }
    return response
