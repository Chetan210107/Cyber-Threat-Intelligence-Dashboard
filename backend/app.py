from __future__ import annotations

import sys
from pathlib import Path
from sqlalchemy import select

from flask import Flask, jsonify
from marshmallow import ValidationError
from flask_restx import Api

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.config import DevelopmentConfig
from backend.extensions import cors, db, jwt, migrate
from backend.models.role import Role
from backend.models.user_profile import UserProfile
from backend.models.user import User
from backend.security.passwords import hash_password
from backend.routes.auth_routes import auth_namespace
from backend.routes.profile_routes import profile_namespace


def create_app(config_object: type[object] = DevelopmentConfig) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    api = Api(app, version="1.0", title="CTID API", doc="/api/docs")
    api.add_namespace(auth_namespace, path="/api/v1/auth")
    api.add_namespace(profile_namespace, path="/api/v1/profile")

    with app.app_context():
        db.create_all()
        for role_name in ("analyst", "manager", "admin"):
            existing_role = db.session.execute(select(Role).where(Role.name == role_name)).scalar_one_or_none()
            if existing_role is None:
                db.session.add(Role(name=role_name, description=f"Default {role_name} role", is_system=True))
        db.session.commit()

        demo_user_id = db.session.execute(select(User.id).where(User.email == "demo@ctid.local")).scalar_one_or_none()
        if demo_user_id is None:
            analyst_role = db.session.execute(select(Role).where(Role.name == "analyst")).scalar_one()
            demo_user = User(
                email="demo@ctid.local",
                password_hash=hash_password("CTIDDemo!2026"),
                full_name="Demo Analyst",
                roles=[analyst_role],
                is_active=True,
                mfa_enabled=False,
            )
            db.session.add(demo_user)
            db.session.commit()

    @app.errorhandler(ValueError)
    def handle_value_error(error: ValueError):
        return jsonify({"success": False, "message": str(error)}), 400

    @app.errorhandler(ValidationError)
    def handle_validation_error(error: ValidationError):
        return jsonify({"success": False, "message": "Validation failed.", "errors": error.messages}), 400

    @app.errorhandler(PermissionError)
    def handle_permission_error(error: PermissionError):
        return jsonify({"success": False, "message": str(error)}), 403

    @app.get("/health")
    def health_check() -> tuple[dict[str, str], int]:
        return jsonify({"status": "ok", "service": "ctid-backend"}), 200

    return app


app = create_app()


if __name__ == "__main__":
    app.run()
