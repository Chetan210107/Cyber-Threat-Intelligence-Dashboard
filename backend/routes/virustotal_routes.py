from __future__ import annotations

from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from backend.controllers.virustotal_controller import VirusTotalController

virustotal_namespace = Namespace("virustotal", description="VirusTotal indicator intelligence")
virustotal_controller = VirusTotalController()


@virustotal_namespace.route("/ip/<string:indicator>")
class VirusTotalIPResource(Resource):
    @jwt_required()
    def get(self, indicator: str):
        return virustotal_controller.lookup_ip(indicator)


@virustotal_namespace.route("/domain/<string:indicator>")
class VirusTotalDomainResource(Resource):
    @jwt_required()
    def get(self, indicator: str):
        return virustotal_controller.lookup_domain(indicator)


@virustotal_namespace.route("/hash/<string:indicator>")
class VirusTotalHashResource(Resource):
    @jwt_required()
    def get(self, indicator: str):
        return virustotal_controller.lookup_hash(indicator)
