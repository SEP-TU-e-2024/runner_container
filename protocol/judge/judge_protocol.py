"""
This module contains the JudgeProtocol class.
"""

import threading
from queue import Queue

from custom_logger import main_logger
from protocol import Connection, Protocol

from .commands import Commands

logger = main_logger.getChild("protocol.judge")


class JudgeProtocol(Protocol):
    """
    The protocol class used by the judge server.
    """

    connection: Connection
    queue_dict_lock: threading.Lock
    queue_dict: dict[str, Queue[dict]]
    receiver_thread: threading.Thread

    def __init__(self, connection: Connection):
        self.connection = connection
        self.queue_dict_lock = threading.Lock()
        self.queue_dict: dict[str, Queue[dict]] = {}

        self.receiver_thread = threading.Thread(target=self._receiver, daemon=True)
        self.receiver_thread.start()

    def _receiver(self):
        """
        Receives and handles responses from the runner.
        """

        while True:
            message_id, response = self._receive_response()

            with self.queue_dict_lock:
                self.queue_dict[message_id].put(response)

    def send_command(self, command: Commands, block: bool = False, **kwargs):
        """
        Sends a given command with the given arguments to the runner specifed in the connection.
        """

        if block:
            self._send_command(command, **kwargs)
            return

        threading.Thread(
            target=self._send_command, args=(command,), kwargs=kwargs, daemon=True
        ).start()

    def _send_command(self, command: Commands, **kwargs):
        """
        Send command to the runner and wait for the response.
        """
        counter = self.connection.counter
        message = {"id": counter.generate(), "command": command.name, "args": kwargs}

        queue = Queue()
        with self.queue_dict_lock:
            self.queue_dict[message["id"]] = queue

        Protocol.send(self.connection, message)
        response = queue.get()

        command.value.response(response)

        with self.queue_dict_lock:
            del self.queue_dict[message["id"]]

    def _receive_response(self) -> tuple[str, dict]:
        """
        Receives a response from the runner.
        """

        message = Protocol.receive(self.connection)

        if message["response"] is None:
            raise ValueError("Received message with missing response!")

        response = message["response"]

        if message["id"] is None:
            raise ValueError("Received message with missing id!")

        message_id = message["id"]

        return message_id, response
