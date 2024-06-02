from custom_logger import main_logger
from protocol import Connection, Protocol

from .commands import Command, Commands

logger = main_logger.getChild("protocol.runner")


class RunnerProtocol(Protocol):
    @staticmethod
    def receive_command(connection: Connection) -> tuple[Command, dict]:
        """
        Handles the incoming commands from the judge server.
        """

        message = Protocol.receive(connection)

        command_name = message["command"]
        command_args = message["args"]

        main_logger.info(f"Received command: {command_name} with args: {command_args}")

        return Commands[""], command_args

    @staticmethod
    def send_response(connection: Connection, response: dict):
        """
        Sends a response to the judge server.
        """

        Protocol.send(connection, response)
