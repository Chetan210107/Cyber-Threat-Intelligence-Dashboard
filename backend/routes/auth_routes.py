from __future__ import annotations

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource

from backend.controllers.auth_controller import AuthController

auth_namespace = Namespace("auth", description="Authentication operations")
auth_controller = AuthController()


@auth_namespace.route("/register")
class RegisterResource(Resource):
    def post(self):
        return auth_controller.register()


@auth_namespace.route("/login")
class LoginResource(Resource):
    def post(self):
        return auth_controller.login()


@auth_namespace.route("/refresh")
class RefreshResource(Resource):
    def post(self):
        return auth_controller.refresh()


@auth_namespace.route("/logout")
class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        return auth_controller.logout()


@auth_namespace.route("/me")
class MeResource(Resource):
    @jwt_required()
    def get(self):
        current_identity = get_jwt_identity()
        return {"success": True, "message": "Current identity retrieved.", "data": {"user_id": current_identity}}, 200
