from __future__ import annotations

from datetime import datetime, timezone

from backend.extensions import db


class UserProfile(db.Model):
    __tablename__ = "user_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True, index=True)
    full_name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(40), nullable=False, unique=True, index=True)
    college = db.Column(db.String(150), nullable=False)
    course = db.Column(db.String(150), nullable=False)
    organization = db.Column(db.String(150), nullable=True)
    country = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(500), nullable=False)
    avatar = db.Column(db.Text, nullable=True)
    preferred_theme = db.Column(db.String(20), nullable=False, default="dark")
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user = db.relationship("User", back_populates="profile")
