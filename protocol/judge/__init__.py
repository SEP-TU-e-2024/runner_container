from abc import ABC, abstractmethod
from enum import Enum

from protocol import Connection, Protocol


class Commands(Enum):
    CHECK = "CHECK"
    START = "START"
    STOP = "STOP"


class Command(ABC):
    @staticmethod
    @abstractmethod
    def response(message: dict):
        pass


class StartCommand(Command):
    @staticmethod
    def response(message: dict):
        pass


class CheckCommand(Command):
    @staticmethod
    def response(message: dict):
        if message["status"] is None:
            raise ValueError("Received message with missing status!")

        status = message["status"]

        if status != "ok":
            raise ValueError(f'Unexpected respone! Expected "ok" and got "{status}"')


class JudgeProtocol(Protocol):
    @staticmethod
    def send_command(connection: Connection, command: Commands, **kwargs):
        """
        Sends a given command with the given arguemtents to the runner specifed in the connection.
        """
        message = {"command": command.value, "args": kwargs}
        Protocol.send(connection, message)
