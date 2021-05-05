from flask import Blueprint, jsonify, request
from models.constants import EventKey

service_bp = Blueprint('service_bp', __name__, url_prefix='/api/services')


@service_bp.route('/post-example', methods=['POST'])
def post_example():
    print(f"/post-example url triggered: request method: {request.method}")
    requested_data = request.json
    print(f"requested_data: {requested_data}")
    return jsonify({
        EventKey.Response: "POST request is successful"
    })


@service_bp.route('/get-example', methods=['GET'])
def get_example():
    print(f"/get-example url triggered: request method: {request.method}")
    content = request.args.get('id')
    print(f"requested_data: {content}")
    return jsonify({
        EventKey.Response: f"GET request is successful, received payload: {content}"
    })

@service_bp.route('/exception-example', methods=['GET'])
def exception_example():
    raise IOError('Anything')