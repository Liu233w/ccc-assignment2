from flask import Blueprint, jsonify, request
from models.constants import EventKey

service_bp = Blueprint('service_bp', __name__, url_prefix='/api/services')


@service_bp.route('/post-example', methods=['POST'])
def post_example():
    print(f"/post-example triggered: request method: {request.method}")
    if request.method == 'POST':
        try:
            requested_data = request.json
            print(f"requested_data: {requested_data}")
            return jsonify({
                EventKey.Response: "post request is successful"
            })
        except Exception as err:
            return jsonify({
                EventKey.Response: "post request failed"
            })