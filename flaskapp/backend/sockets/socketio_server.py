from functools import partial
from flask_socketio import SocketIO
from flaskapp.backend.models.constants import EventKey


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

    def emit_event(self, topic, payload):
        # frontend will only listen to "serviceEvent" handler, but the topic will be unique for different events
        self.emit(EventKey.ServiceEvent, {EventKey.Topic: topic, EventKey.Payload: payload})
