import uuid

from protocol import Connection, Protocol

from .commands import Commands


class JudgeProtocol(Protocol):
    @staticmethod
    def send_command(connection: Connection, command: Commands, **kwargs):
        """
        Sends a given command with the given arguemtents to the runner specifed in the connection.
        """
        message = {"id": uuid.uuid4().hex, "command": command.name, "args": kwargs}
        Protocol.send(connection, message)
        response = Protocol.receive(connection, 5)
        command.value.response(response)
