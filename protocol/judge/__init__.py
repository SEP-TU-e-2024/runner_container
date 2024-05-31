"""
This module contains the parts of the protocol used by the judge.
"""

from protocol import Connection, Protocol

from .commands import Commands


class JudgeProtocol(Protocol):
    @staticmethod
    def send_command(connection: Connection, command: Commands, **kwargs):
        """
        Sends a given command with the given arguemtents to the runner specifed in the connection.
        """
        message = {"command": command.name, "args": kwargs}
        Protocol.send(connection, message)
        response = Protocol.receive(connection, 5)
        command.value.response(response)
