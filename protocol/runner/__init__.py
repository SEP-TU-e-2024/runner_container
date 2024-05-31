"""
This module contains the parts of the protocol used by the runner.
"""

from custom_logger import main_logger
from protocol import Connection, Protocol

from .commands import Commands
from .commands.command import Command

main_logger = main_logger.getChild("protocol.runner")


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

        return Commands[command_name].value, command_args
