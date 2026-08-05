from __future__ import annotations

from backend.extensions import db
from backend.models.user_profile import UserProfile


class ProfileRepository:
    def find_by_user_id(self, user_id: int) -> UserProfile | None:
        return UserProfile.query.filter_by(user_id=user_id).one_or_none()

    def find_by_username(self, username: str) -> UserProfile | None:
        return UserProfile.query.filter_by(username=username.lower()).one_or_none()

    def save(self, profile: UserProfile) -> UserProfile:
        db.session.add(profile)
        db.session.commit()
        return profile
