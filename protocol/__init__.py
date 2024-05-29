"""
This module containes the protocol used for communication between the judge server and the runner.
"""

import json
import socket

from custom_logger import main_logger

# from .commands import Commands

logger = main_logger.getChild("protocol")


class Protocol:
    VERSION = "0.0.1"

    @staticmethod
    def send(sock: socket.socket, message: dict):
        """
        Sends a json message.
        """
        message.update({"version": Protocol.VERSION})
        json_message = json.dumps(message)
        data = json_message.encode()
        data_size = len(data)
        sock.sendall(data_size.to_bytes(4, byteorder="big"))
        sock.sendall(data)

    @staticmethod
    def receive(sock: socket.socket, timeout: int | None = None) -> dict:
        """
        Receive a json message.
        """
        ip = sock.getpeername()[0]
        port = sock.getpeername()[1]

        data = sock.recv(4)

        if len(data) == 0:
            raise OSError(f"The connection was closed by the peer with ip {ip} on port {port}!")

        sock.settimeout(timeout)
        data_size = int.from_bytes(data, byteorder="big")
        sock.settimeout(None)

        if data_size == 0:
            raise ValueError(f"The upcoming message from {ip} on {port} is of size 0!")

        sock.settimeout(timeout)
        data = sock.recv(data_size)
        sock.settimeout(None)
        logger.info(f"Received message {data} of size {data_size} bytes from {ip} on port {port}.")
        message = json.loads(data)

        if message["version"] is None:
            raise ValueError("The sent message is missing the version of the protocol!")

        if message["version"] != Protocol.VERSION:
            raise ValueError(
                f"Received message with version {message["version"]} but expected {Protocol.VERSION}!"
            )

        return message
