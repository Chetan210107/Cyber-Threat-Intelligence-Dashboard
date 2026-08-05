from __future__ import annotations

from flask import request
from flask_jwt_extended import get_jwt_identity
from marshmallow import ValidationError

from backend.schemas.profile_schemas import (
    ProfileCreateSchema,
    ProfileResponseSchema,
    ProfileUpdateSchema,
    UsernameAvailabilitySchema,
)
from backend.services.profile_service import ProfileService
from backend.utils.responses import api_response


class ProfileController:
    def __init__(self, profile_service: ProfileService | None = None) -> None:
        self.profile_service = profile_service or ProfileService()
        self.create_schema = ProfileCreateSchema()
        self.update_schema = ProfileUpdateSchema()
        self.availability_schema = UsernameAvailabilitySchema()
        self.response_schema = ProfileResponseSchema()

    def get_my_profile(self) -> tuple[dict, int]:
        user_id = self._current_user_id()
        profile = self.profile_service.get_profile_for_user(user_id)
        if profile is None:
            return api_response(False, "Profile not found."), 404
        return api_response(True, "Profile retrieved successfully.", self._serialize_profile(profile)), 200

    def create_profile(self) -> tuple[dict, int]:
        user_id = self._current_user_id()
        payload = self._load_json(self.create_schema)
        profile = self.profile_service.create_profile(user_id, payload)
        return api_response(True, "Profile created successfully.", self._serialize_profile(profile)), 201

    def update_profile(self) -> tuple[dict, int]:
        user_id = self._current_user_id()
        payload = self._load_json(self.update_schema)
        profile = self.profile_service.update_profile(user_id, payload)
        return api_response(True, "Profile updated successfully.", self._serialize_profile(profile)), 200

    def check_username_availability(self) -> tuple[dict, int]:
        user_id = self._current_user_id()
        data = request.args.to_dict(flat=True)
        try:
            payload = self.availability_schema.load(data)
        except ValidationError as error:
            raise ValueError(error.messages) from error

        available = self.profile_service.is_username_available(payload["username"], current_user_id=user_id)
        return api_response(True, "Username availability checked.", {"username": payload["username"], "available": available}), 200

    @staticmethod
    def _current_user_id() -> int:
        return int(get_jwt_identity())

    def _serialize_profile(self, profile) -> dict:
        return self.response_schema.dump(
            {
                "id": profile.id,
                "user_id": profile.user_id,
                "full_name": profile.full_name,
                "username": profile.username,
                "college": profile.college,
                "course": profile.course,
                "organization": profile.organization,
                "country": profile.country,
                "bio": profile.bio,
                "avatar": profile.avatar,
                "preferred_theme": profile.preferred_theme,
                "email": profile.user.email,
                "roles": [role.name for role in profile.user.roles],
                "member_since": profile.created_at,
            }
        )

    @staticmethod
    def _load_json(schema):
        data = request.get_json(silent=True) or {}
        try:
            return schema.load(data)
        except ValidationError as error:
            raise ValueError(error.messages) from error
