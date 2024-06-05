"""
This module containes the RunnerProtocol class.
"""

from custom_logger import main_logger
from protocol import Connection, Protocol

from .commands import Commands
from .commands.command import Command

logger = main_logger.getChild("protocol.runner")


class RunnerProtocol(Protocol):
    def __init__(self, connection: Connection):
        self.connection = connection

    def receive_command(self) -> tuple[Command, dict]:
        """
        Handles the incoming commands from the judge server.
        """

        message = Protocol.receive(self.connection)

        command_id = message["id"]
        command_name = message["command"]
        command_args = message["args"]

        main_logger.info(f"Received command: {command_name} with args: {command_args}")

        return command_id, command_name, command_args

    def handle_command(self, command_id: str, command_name: str, args: dict) -> None:
        """
        Handles the incoming commands from the judge server.
        """

        command = Commands[command_name].value
        response = command.execute(args)
        message = {"id": command_id, "response": response}
        Protocol.send(self.connection, message)

        main_logger.info(f"Sent response: {response}")
