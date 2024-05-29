import socket
from abc import ABC, abstractmethod


class Command(ABC):
    @staticmethod
    @abstractmethod
    def execute(sock, **kwargs):
        """
        Excute the command according to the given arguments.
        """
        pass

    @staticmethod
    @abstractmethod
    def response(sock: socket.socket):
        pass
