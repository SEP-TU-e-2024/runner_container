from abc import ABC, abstractmethod


class Command(ABC):
    """
    Base abstract class for commands.
    """

    @staticmethod
    @abstractmethod
    def execute(args: dict):
        """
        Executes the command. It is recommended to call this in a separate thread.
        """
        pass
