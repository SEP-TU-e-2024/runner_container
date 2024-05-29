import socket

from protocol import Protocol
from protocol.commands import Commands


class JudgeProtocol(Protocol):
    
    @staticmethod
    def send_command(sock: socket.socket, command: Commands, **kwargs):
        """ """
        message = {"command": command.value, "args": kwargs}
        Protocol.send(sock, message)
        
        
        # command.value.response(sock)
