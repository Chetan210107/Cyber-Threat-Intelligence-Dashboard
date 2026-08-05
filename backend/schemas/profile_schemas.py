from __future__ import annotations

from marshmallow import Schema, ValidationError, fields, validates, validates_schema


class ProfileBaseSchema(Schema):
    full_name = fields.String(required=True, validate=lambda value: 2 <= len(value.strip()) <= 150)
    username = fields.String(required=True, validate=lambda value: 3 <= len(value.strip()) <= 40)
    college = fields.String(required=True, validate=lambda value: 2 <= len(value.strip()) <= 150)
    course = fields.String(required=True, validate=lambda value: 2 <= len(value.strip()) <= 150)
    organization = fields.String(required=False, allow_none=True, load_default=None, validate=lambda value: value is None or len(value.strip()) <= 150)
    country = fields.String(required=True, validate=lambda value: 2 <= len(value.strip()) <= 100)
    bio = fields.String(required=True, validate=lambda value: 10 <= len(value.strip()) <= 500)
    avatar = fields.String(required=False, allow_none=True, load_default=None)
    preferred_theme = fields.String(required=True)

    @validates("username")
    def validate_username(self, value: str, **kwargs) -> None:
        normalized = value.strip()
        if not normalized.replace("_", "").replace("-", "").isalnum():
            raise ValidationError("Username may contain letters, numbers, underscores, and hyphens only.")

    @validates("preferred_theme")
    def validate_preferred_theme(self, value: str, **kwargs) -> None:
        if value not in {"dark", "light", "system"}:
            raise ValidationError("Preferred theme must be dark, light, or system.")


class ProfileCreateSchema(ProfileBaseSchema):
    pass


class ProfileUpdateSchema(ProfileBaseSchema):
    pass


class UsernameAvailabilitySchema(Schema):
    username = fields.String(required=True)

    @validates("username")
    def validate_username(self, value: str, **kwargs) -> None:
        normalized = value.strip()
        if len(normalized) < 3:
            raise ValidationError("Username must be at least 3 characters long.")
        if not normalized.replace("_", "").replace("-", "").isalnum():
            raise ValidationError("Username may contain letters, numbers, underscores, and hyphens only.")


class ProfileResponseSchema(Schema):
    id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    full_name = fields.String(required=True)
    username = fields.String(required=True)
    college = fields.String(required=True)
    course = fields.String(required=True)
    organization = fields.String(allow_none=True)
    country = fields.String(required=True)
    bio = fields.String(required=True)
    avatar = fields.String(allow_none=True)
    preferred_theme = fields.String(required=True)
    email = fields.Email(required=True)
    roles = fields.List(fields.String(), required=True)
    member_since = fields.DateTime(required=True)
