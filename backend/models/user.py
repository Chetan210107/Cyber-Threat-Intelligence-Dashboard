from __future__ import annotations

from datetime import datetime, timezone

from backend.extensions import db
from backend.models.role import user_roles


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True, index=True)
    mfa_enabled = db.Column(db.Boolean, nullable=False, default=False)
    last_login_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    roles = db.relationship("Role", secondary=user_roles, backref="users", lazy="joined")
    profile = db.relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")

