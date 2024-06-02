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

        return command_name, command_args

    @staticmethod
    def handle_command(connection: Connection, command_name: str, args: dict) -> None:
        """
        Handles the incoming commands from the judge server.
        """
        command = Commands[command_name].value
        response = command.execute(args)
        message = {"command": command_name, "response": response}
        Protocol.send(connection, message)

        main_logger.info(f"Sent response: {response}")
