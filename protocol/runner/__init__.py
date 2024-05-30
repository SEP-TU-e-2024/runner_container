from abc import ABC, abstractmethod
from enum import Enum

from custom_logger import main_logger
from protocol import Connection, Protocol

main_logger = main_logger.getChild("protocol.runner")


class Command(ABC):
    @staticmethod
    @abstractmethod
    def execute(connection: Connection, args: dict):
        pass


class CheckCommand(Command):
    @staticmethod
    def execute(connection: Connection, args: dict):
        Protocol.send(connection, {"status": "ok"})


class Commands(Enum):
    CHECK = CheckCommand()


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
