from flaskapp.backend.sockets.socketio_server import SocketIOServer


class MsgParserSocketIOServer(SocketIOServer):

    def __init__(self, socketio, namespace, application_path):
        super().__init__(socketio, namespace)
        self.application_path = application_path

        # listen to "connect" event handler from front-end
        self.on_event("connect", self._connect)

    def _connect(self):
        print(f"established connection with front end")
        return {"response": "connected"}
