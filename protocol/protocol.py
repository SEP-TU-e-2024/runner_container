"""
This module containes the protocol used for communication between the judge server and the runner.
"""

import json

from custom_logger import main_logger

from .connection import Connection

logger = main_logger.getChild("protocol")


class Protocol:
    VERSION = "0.0.2"

    @staticmethod
    def send(connection: Connection, message: dict):
        """
        Sends a JSON message. This function is thread-safe and locks the socket mutex.
        """

        ip = connection.ip
        port = connection.port
        sock = connection.sock
        sock_lock = connection.sock_lock

        message.update({"version": Protocol.VERSION})
        json_message = json.dumps(message)
        data = json_message.encode()
        data_size = len(data)

        with sock_lock:
            logger.info(
                f"Sending message {data} of size {data_size} bytes from {ip} on port {port}."
            )
            sock.sendall(data_size.to_bytes(4, byteorder="big"))
            sock.sendall(data)

    @staticmethod
    def receive(connection: Connection, timeout: int | None = None) -> dict:
        """
        Receives a JSON message.
        """

        sock = connection.sock
        ip = connection.ip
        port = connection.port

        data = sock.recv(4)

        if len(data) == 0:
            raise ConnectionResetError(
                f"The connection was closed by the peer with ip {ip} on port {port}!"
            )

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

        version = message["version"]

        if version != Protocol.VERSION:
            raise ValueError(
                f"Received message with version {version} but expected {Protocol.VERSION}!"
            )

        return message
