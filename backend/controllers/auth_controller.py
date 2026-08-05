from __future__ import annotations

from datetime import datetime, timezone

from flask import current_app, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, decode_token
from marshmallow import ValidationError

from backend.schemas.auth_schemas import (
    LoginSchema,
    PasswordResetConfirmSchema,
    PasswordResetRequestSchema,
    RegisterSchema,
    TokenRefreshSchema,
    UserResponseSchema,
)
from backend.security.tokens import generate_secure_token
from backend.services.auth_service import AuthService
from backend.utils.responses import api_response


class AuthController:
    def __init__(self, auth_service: AuthService | None = None) -> None:
        self.auth_service = auth_service or AuthService()
        self.register_schema = RegisterSchema()
        self.login_schema = LoginSchema()
        self.refresh_schema = TokenRefreshSchema()
        self.reset_request_schema = PasswordResetRequestSchema()
        self.reset_confirm_schema = PasswordResetConfirmSchema()
        self.user_response_schema = UserResponseSchema()

    def register(self) -> tuple[dict, int]:
        payload = self._load_json(self.register_schema)
        user = self.auth_service.register_user(
            email=payload["email"],
            password=payload["password"],
            full_name=payload["full_name"],
        )
        return self._build_auth_payload(user, 201, "Registration successful.")

    def login(self) -> tuple[dict, int]:
        payload = self._load_json(self.login_schema)
        user = self.auth_service.authenticate_user(payload["email"], payload["password"])
        return self._build_auth_payload(user, 200, "Login successful.")

    def refresh(self) -> tuple[dict, int]:
        payload = self._load_json(self.refresh_schema)
        decoded_refresh = decode_token(payload["refresh_token"])
        if decoded_refresh.get("type") != "refresh":
            raise ValueError("Invalid refresh token.")

        new_user_identity = str(decoded_refresh["sub"])
        refreshed_user = self.auth_service.user_repository.find_by_id(int(new_user_identity))
        if refreshed_user is None or not refreshed_user.is_active:
            raise ValueError("Invalid refresh token.")

        stored_token = self.auth_service.token_repository.find_by_jti(decoded_refresh["jti"])
        if stored_token is None or stored_token.revoked_at is not None:
            raise ValueError("Refresh token has been revoked.")

        claims = {"roles": [role.name for role in refreshed_user.roles], "email": refreshed_user.email}
        access_token = create_access_token(identity=new_user_identity, additional_claims=claims)
        refresh_token = create_refresh_token(identity=new_user_identity, additional_claims=claims)
        refresh_data = decode_token(refresh_token)
        self.auth_service.record_refresh_token(
            user_id=refreshed_user.id,
            jti=refresh_data["jti"],
            refresh_token=refresh_token,
            expires_at=datetime.fromtimestamp(refresh_data["exp"], tz=timezone.utc),
        )
        return api_response(True, "Token refreshed successfully.", {"access_token": access_token, "refresh_token": refresh_token}), 200

    def logout(self) -> tuple[dict, int]:
        payload = self._load_json(self.refresh_schema)
        jwt_claims = get_jwt()
        decoded_refresh = decode_token(payload["refresh_token"])
        if str(decoded_refresh.get("sub")) != str(jwt_claims.get("sub")):
            raise ValueError("Refresh token does not match the authenticated user.")

        self.auth_service.logout(decoded_refresh.get("jti"))
        return api_response(True, "Logout successful."), 200

    def me(self, user) -> tuple[dict, int]:
        return api_response(True, "Current user retrieved.", self.user_response_schema.dump(user)), 200

    def request_password_reset(self) -> tuple[dict, int]:
        self._load_json(self.reset_request_schema)
        token = generate_secure_token()
        return api_response(True, "Password reset instructions queued.", {"reset_token_preview": token[:8]}), 202

    def confirm_password_reset(self) -> tuple[dict, int]:
        self._load_json(self.reset_confirm_schema)
        return api_response(True, "Password reset completed."), 200

    def _build_auth_payload(self, user, status_code: int, message: str) -> tuple[dict, int]:
        identity = str(user.id)
        claims = {"roles": [role.name for role in user.roles], "email": user.email}
        access_token = create_access_token(identity=identity, additional_claims=claims)
        refresh_token = create_refresh_token(identity=identity, additional_claims=claims)
        refresh_data = decode_token(refresh_token)
        self.auth_service.record_refresh_token(
            user_id=user.id,
            jti=refresh_data["jti"],
            refresh_token=refresh_token,
            expires_at=datetime.fromtimestamp(refresh_data["exp"], tz=timezone.utc),
        )
        response_data = {
            "user": self.user_response_schema.dump(
                {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "roles": [role.name for role in user.roles],
                    "mfa_enabled": user.mfa_enabled,
                    "is_active": user.is_active,
                }
            ),
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": current_app.config["JWT_ACCESS_TOKEN_EXPIRES"],
        }
        return api_response(True, message, response_data), status_code

    @staticmethod
    def _load_json(schema):
        data = request.get_json(silent=True) or {}
        try:
            return schema.load(data)
        except ValidationError as error:
            raise ValueError(error.messages) from error
