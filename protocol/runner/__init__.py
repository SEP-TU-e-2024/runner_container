import socket

from protocol import Protocol


class RunnerProtocol(Protocol):
    
    @staticmethod
    def receive_command(sock: socket.socket):
        """
        """
        message = Protocol.receive(sock)

        command_name = message["command"]
        command_args = message["args"]

        #command = Commands[command_name]
        #command.value.execute(sock, **command_args)