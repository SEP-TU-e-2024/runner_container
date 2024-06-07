"""
This module containes the RunnerProtocol class.
"""

from custom_logger import main_logger
from protocol import Connection, Protocol

from .commands import Commands
from .commands.command import Command

logger = main_logger.getChild("protocol.runner")


class RunnerProtocol(Protocol):
    """
    The protocol class used by the runners.
    """

    connection: Connection

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

        try:
            command = Commands[command_name].value
            response = command.execute(args)
            message = {"id": command_id, "response": response}
            Protocol.send(self.connection, message)

            main_logger.info(f"Sent response: {response}")

        except KeyError:
            main_logger.error(f"Received unknown command: {command_name}")

        except Exception as e:
            if e is ConnectionResetError or e is ConnectionAbortedError:
                raise e

            main_logger.error(
                f"An unexpected error has occured while trying to execute command {command_name}! ({e})"
            )
