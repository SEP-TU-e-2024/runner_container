from abc import ABC, abstractmethod

from protocol import Connection


class Command(ABC):
    """
    Base abstract class for commands.
    """

    @staticmethod
    @abstractmethod
    def execute(connection: Connection, args: dict):
        """
        Executes the command. It is recommended to call this in a separate thread.
        """
        pass