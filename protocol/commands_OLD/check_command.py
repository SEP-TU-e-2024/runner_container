import socket

import protocol

from .command import Command


class CheckCommand(Command):
    @staticmethod
    def execute(sock: socket.socket, **kwargs):
        protocol.send(sock, {"status": "ok"})

    @staticmethod
    def response(sock: socket.socket):
        message = protocol.receive(sock, 5)

        if message["status"] is None:
            raise ValueError("Received message with missing status!")

        status = message["status"]

        if status != "ok":
            raise ValueError(f'Unexpected respone! Expected "ok" and got "{status}"')
