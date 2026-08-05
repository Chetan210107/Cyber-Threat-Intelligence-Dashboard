from __future__ import annotations

from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from backend.controllers.profile_controller import ProfileController

profile_namespace = Namespace("profile", description="User profile and onboarding operations")
profile_controller = ProfileController()


@profile_namespace.route("/me")
class MyProfileResource(Resource):
    @jwt_required()
    def get(self):
        return profile_controller.get_my_profile()

    @jwt_required()
    def post(self):
        return profile_controller.create_profile()

    @jwt_required()
    def put(self):
        return profile_controller.update_profile()


@profile_namespace.route("/username-availability")
class UsernameAvailabilityResource(Resource):
    @jwt_required()
    def get(self):
        return profile_controller.check_username_availability()
