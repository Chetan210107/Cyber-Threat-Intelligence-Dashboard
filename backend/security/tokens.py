from __future__ import annotations

import hashlib
import secrets

from flask_jwt_extended import decode_token


def generate_secure_token() -> str:
    return secrets.token_urlsafe(48)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def extract_jti(token: str) -> str:
    return str(decode_token(token)["jti"])


def extract_expiration(token: str):
    return decode_token(token)["exp"]
