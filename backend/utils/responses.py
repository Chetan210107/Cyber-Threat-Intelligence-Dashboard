from __future__ import annotations

from typing import Any


def api_response(
    success: bool,
    message: str,
    data: dict[str, Any] | None = None,
    errors: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {"success": success, "message": message}
    if data is not None:
        payload["data"] = data
    if errors is not None:
        payload["errors"] = errors
    return payload
