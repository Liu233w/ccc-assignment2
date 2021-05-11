import json
from pathlib import Path
from sockets.socketio_server import SocketIOServer
from models.constants import EventKey


class MsgParserSocketIOServer(SocketIOServer):
    def __init__(self, socketio, namespace, application_path):
        super().__init__(socketio, namespace)
        # application path: ~/backend
        application_path = application_path
        self.configuration_file_path = Path(application_path) / "configuration"

        self.on_event("connect", self._connect)
        self.on_event("getProjectInfo", self._get_project_info)
        self.on_event("eventEmitExample", self._event_emit_example)

    def _connect(self):
        print(f"established connection with front end")
        return

    def _get_project_info(self):
        """
        received request from frontend for project info
        return course name, project title, members name and project description
        retrieved from configuration/project_info.json to frontend
        :param payload: None
        :return: dict
        """
        project_info_json_path = str(self.configuration_file_path / "project_info.json")
        with open(project_info_json_path, "r") as f:
            data = json.load(f)
        # return response to frontend
        return json.dumps(data)

    def _event_emit_example(self, payload):
        """
        Emit event to frontend
        :return:
        """
        print(f"event emit example payload from front end: {payload}")
        self.emit_event(topic="eventEmitExample", payload=payload)
        return
