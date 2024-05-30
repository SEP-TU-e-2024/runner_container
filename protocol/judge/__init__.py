"""
This module contains the parts of the protocol used by the judge.
"""

from abc import ABC, abstractmethod
from enum import Enum

from protocol import Connection, Protocol


class Command(ABC):
    """
    Base abstract class for commands.
    """

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


class Commands(Enum):
    START = StartCommand()
    CHECK = CheckCommand()


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
