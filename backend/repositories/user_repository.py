from __future__ import annotations

from backend.extensions import db
from backend.models.user import User


class UserRepository:
    def find_by_email(self, email: str) -> User | None:
        return User.query.filter_by(email=email.lower()).one_or_none()

    def find_by_id(self, user_id: int) -> User | None:
        return db.session.get(User, user_id)

    def save(self, user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user
