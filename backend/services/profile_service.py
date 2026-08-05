from __future__ import annotations

from backend.models.user import User
from backend.models.user_profile import UserProfile
from backend.repositories.profile_repository import ProfileRepository
from backend.repositories.user_repository import UserRepository


class ProfileService:
    def __init__(
        self,
        profile_repository: ProfileRepository | None = None,
        user_repository: UserRepository | None = None,
    ) -> None:
        self.profile_repository = profile_repository or ProfileRepository()
        self.user_repository = user_repository or UserRepository()

    def get_profile_for_user(self, user_id: int) -> UserProfile | None:
        return self.profile_repository.find_by_user_id(user_id)

    def is_username_available(self, username: str, current_user_id: int | None = None) -> bool:
        profile = self.profile_repository.find_by_username(username)
        if profile is None:
            return True
        return current_user_id is not None and profile.user_id == current_user_id

    def create_profile(self, user_id: int, payload: dict) -> UserProfile:
        user = self._get_user_or_raise(user_id)
        existing_profile = self.profile_repository.find_by_user_id(user_id)
        if existing_profile is not None:
            raise ValueError("Profile already exists for this user.")

        username = payload["username"].strip().lower()
        if not self.is_username_available(username):
            raise ValueError("Username already taken.")

        profile = UserProfile(
            user_id=user.id,
            full_name=payload["full_name"].strip(),
            username=username,
            college=payload["college"].strip(),
            course=payload["course"].strip(),
            organization=(payload.get("organization") or None),
            country=payload["country"].strip(),
            bio=payload["bio"].strip(),
            avatar=payload.get("avatar"),
            preferred_theme=payload["preferred_theme"],
        )
        return self.profile_repository.save(profile)

    def update_profile(self, user_id: int, payload: dict) -> UserProfile:
        profile = self.profile_repository.find_by_user_id(user_id)
        if profile is None:
            raise ValueError("Profile not found.")

        username = payload["username"].strip().lower()
        if not self.is_username_available(username, current_user_id=user_id):
            raise ValueError("Username already taken.")

        profile.full_name = payload["full_name"].strip()
        profile.username = username
        profile.college = payload["college"].strip()
        profile.course = payload["course"].strip()
        profile.organization = (payload.get("organization") or None)
        profile.country = payload["country"].strip()
        profile.bio = payload["bio"].strip()
        profile.avatar = payload.get("avatar")
        profile.preferred_theme = payload["preferred_theme"]
        return self.profile_repository.save(profile)

    def _get_user_or_raise(self, user_id: int) -> User:
        user = self.user_repository.find_by_id(user_id)
        if user is None:
            raise ValueError("User not found.")
        return user
