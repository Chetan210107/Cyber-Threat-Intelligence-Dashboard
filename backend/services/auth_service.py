from __future__ import annotations

from datetime import datetime, timezone

from backend.extensions import db
from backend.models.audit_log import AuditLog
from backend.models.refresh_token import RefreshToken
from backend.models.role import Role
from backend.models.user import User
from backend.repositories.token_repository import TokenRepository
from backend.repositories.user_repository import UserRepository
from backend.security.passwords import hash_password, verify_password
from backend.security.tokens import hash_token


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository | None = None,
        token_repository: TokenRepository | None = None,
    ) -> None:
        self.user_repository = user_repository or UserRepository()
        self.token_repository = token_repository or TokenRepository()

    def register_user(self, email: str, password: str, full_name: str, role_name: str = "analyst") -> User:
        existing_user = self.user_repository.find_by_email(email)
        if existing_user is not None:
            raise ValueError("A user with this email already exists.")

        role = Role.query.filter_by(name=role_name).one_or_none() or Role(name=role_name)
        user = User(
            email=email.lower(),
            password_hash=hash_password(password),
            full_name=full_name,
            roles=[role],
        )
        self.user_repository.save(user)
        self._log_event("auth.register", user.id, {"email": user.email})
        return user

    def authenticate_user(self, email: str, password: str) -> User:
        user = self.user_repository.find_by_email(email)
        if user is None or not user.is_active:
            raise ValueError("Invalid credentials.")
        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials.")

        user.last_login_at = datetime.now(timezone.utc)
        self.user_repository.save(user)
        self._log_event("auth.login", user.id, {"email": user.email})
        return user

    def record_refresh_token(self, user_id: int, jti: str, refresh_token: str, expires_at: datetime) -> RefreshToken:
        token = RefreshToken(
            user_id=user_id,
            jti=jti,
            token_hash=hash_token(refresh_token),
            expires_at=expires_at,
        )
        return self.token_repository.save_refresh_token(token)

    def logout(self, jti: str | None) -> None:
        if jti:
            self.token_repository.revoke_refresh_token(jti)
            self._log_event("auth.logout", None, {"jti": jti})

    def _log_event(self, action: str, actor_user_id: int | None, metadata: dict[str, str]) -> None:
        db_log = AuditLog(action=action, actor_user_id=actor_user_id, metadata_json=metadata)
        db.session.add(db_log)
        db.session.commit()
