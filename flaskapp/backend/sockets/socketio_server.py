from functools import partial
from flask_socketio import SocketIO


class SocketIOServer:
    """ A Socket.IO server class defines how messages can be communicated between
    backend and frontend
    """

    def __init__(self, socketio, namespace):
        self.socketio = socketio
        self.namespace = namespace

        # partial application of SocketIO methods hard-wiring the socket and the namespace
        self.emit = partial(SocketIO.emit, self.socketio, namespace=self.namespace)
        self.broadcast = partial(SocketIO.emit, self.socketio, namespace=self.namespace, broadcast=True)
        self.on_event = partial(SocketIO.on_event, self.socketio, namespace=self.namespace)
