from protocol import Connection, Protocol

from .command import Command


class CheckCommand(Command):
    """
    Command used to check the status of the runner.
    """

    @staticmethod
    def execute(connection: Connection, args: dict):
        Protocol.send(connection, {"status": "ok"})