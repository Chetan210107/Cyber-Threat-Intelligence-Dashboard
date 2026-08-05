from __future__ import annotations

from functools import wraps

from flask_jwt_extended import get_jwt, verify_jwt_in_request


def require_roles(*required_roles: str):
    def decorator(view_function):
        @wraps(view_function)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            token_roles = set(claims.get("roles", []))
            if not token_roles.intersection(required_roles):
                raise PermissionError("Insufficient privileges.")
            return view_function(*args, **kwargs)

        return wrapper

    return decorator
