from os import path
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from blueprints.services_bp import service_bp
from sockets.msg_parser_socketio_server import MsgParserSocketIOServer
from helpers import register_blueprints
import flasgger
from flask_cors import CORS

from pathlib import Path


def _main():
    # application_path: ~/backend/
    application_path = Path(path.abspath(__file__)).parent
    dist_folder = str(Path(application_path, "dist"))

    serve_port = 9797

    # creates the Flask application instance
    app = Flask(__name__, static_folder=dist_folder, template_folder=dist_folder)

    register_blueprints(app, 'blueprints', ['./blueprints'])

    app.config.update({'DEBUG': False})

    @app.route('/')
    def index():
        """
        index.html is located in dist/index.html;
        after executing "npm run build", dist folder will be automatically generated in backend/dist
        this setting is configured in vue.config.js, which deploys dist folder to backend/dist
        if frontend has been changed, please remember to run "npm run build"
        please do not change anything manually in dist folder or the location of it
        """
        return render_template("index.html")

    @app.errorhandler(Exception)
    def handle_all_exception(e: Exception):
        print(e)
        return jsonify({
            'error': True,
            'message': type(e).__name__ + ': ' + str(e),
        }), 500

    app.config['SWAGGER'] = {
        'title': 'API of CCC Assignment 2',
        'swagger_version': '2.0',
    }
    swagger = flasgger.Swagger(app)

    # allow cors on all domains. we just ignore security issue
    CORS(app)

    # creates the Socket.IO socket instance
    socket_io = SocketIO(app, cors_allowed_origins="*")
    socketio_server = {'msg-parser': MsgParserSocketIOServer(
        socketio=socket_io, namespace='/msg-parser', application_path=application_path)}

    try:
        print(f'Launch browser into http://localhost:{serve_port}')

        socket_io.run(app, host='0.0.0.0', port=serve_port, debug=False)
    except KeyboardInterrupt:
        return 0


if __name__ == '__main__':
    _main()
