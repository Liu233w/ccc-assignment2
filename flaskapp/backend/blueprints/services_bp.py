from flask import Blueprint, jsonify, request

service_bp = Blueprint('service_bp', __name__, url_prefix='/api/services')

