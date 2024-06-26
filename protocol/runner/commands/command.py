"""
This module contains the Command class.
"""

from abc import ABC, abstractmethod


class Command(ABC):
    """
    Base abstract class for commands.
    """
    
    @abstractmethod
    def execute(self, args: dict) -> dict:
        """
        Executes the command. It is recommended to call this in a separate thread.
        """
        pass
