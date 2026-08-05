from __future__ import annotations

from datetime import datetime, timezone

from backend.extensions import db
from backend.models.refresh_token import RefreshToken


class TokenRepository:
    def find_by_jti(self, jti: str) -> RefreshToken | None:
        return RefreshToken.query.filter_by(jti=jti).one_or_none()

    def save_refresh_token(self, refresh_token: RefreshToken) -> RefreshToken:
        db.session.add(refresh_token)
        db.session.commit()
        return refresh_token

    def revoke_refresh_token(self, jti: str) -> RefreshToken | None:
        token = RefreshToken.query.filter_by(jti=jti).one_or_none()
        if token is None:
            return None
        token.revoked_at = datetime.now(timezone.utc)
        db.session.commit()
        return token
