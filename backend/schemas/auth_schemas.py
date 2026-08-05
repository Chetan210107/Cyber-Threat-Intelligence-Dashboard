from __future__ import annotations

from marshmallow import Schema, ValidationError, fields, validates


class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
    full_name = fields.String(required=True)

    @validates("password")
    def validate_password(self, value: str, **kwargs) -> None:
        if len(value) < 12:
            raise ValidationError("Password must be at least 12 characters long.")


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)


class TokenRefreshSchema(Schema):
    refresh_token = fields.String(required=True)


class PasswordResetRequestSchema(Schema):
    email = fields.Email(required=True)


class PasswordResetConfirmSchema(Schema):
    token = fields.String(required=True)
    password = fields.String(required=True, load_only=True)

    @validates("password")
    def validate_password(self, value: str, **kwargs) -> None:
        if len(value) < 12:
            raise ValidationError("Password must be at least 12 characters long.")


class UserResponseSchema(Schema):
    id = fields.Int(required=True)
    email = fields.Email(required=True)
    full_name = fields.String(required=True)
    roles = fields.List(fields.String(), required=True)
    mfa_enabled = fields.Boolean(required=True)
    is_active = fields.Boolean(required=True)
