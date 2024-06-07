#!/usr/bin/env python3.12
"""
The main class of the runner server. It handles the connection to the judge server.
"""

import socket
import threading
from time import sleep

from custom_logger import main_logger
from protocol import Connection
from protocol.runner import Protocol
from settings import JUDGE_HOST, JUDGE_PORT, RETRY_WAIT

logger = main_logger.getChild("runner")


class Runner:
    ip: str
    port: int
    debug: bool
    threads: list[threading.Thread]

    def __init__(self, ip, port, debug=False):
        self.ip = ip
        self.port = port
        self.debug = debug
        self.threads = []

    def start(self):
        """
        Starts the connection to the judge server. In case of a unexpected disconnection, it retries to connect.
        """

        logger.info(f"Trying to connect to the Judge server at {self.ip}:{self.port} ...")

        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.ip, self.port))
                self.connection = Connection(self.ip, self.port, sock, threading.Lock())
                self.protocol = Protocol(self.connection)
                self._handle_commands()

            except (ConnectionRefusedError, ConnectionResetError) as e:
                self.connection = None
                logger.info(f"Failed to connect to judge server. Retrying in 5 seconds... ({e})")
                sleep(RETRY_WAIT)

            finally:
                self.stop()

    def _handle_commands(self):
        """
        Handles the incoming commands from the judge server.
        """

        while True:
            command_id, command_name, command_args = self.protocol.receive_command()
            thread = threading.Thread(
                target=self.protocol.handle_command,
                args=(command_id, command_name, command_args),
                daemon=True,
            )
            thread.start()
            self.threads.append(thread)

    def stop(self):
        """
        Closes the connection to the judge server. Not used currently.
        """

        for thread in self.threads:
            thread.join(1)
            self.threads.clear()
        if self.connection is not None:
            sock = self.connection.sock
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
        self.connection = None


def main():
    """
    The main function of the runner server.
    """

    runner = Runner(JUDGE_HOST, JUDGE_PORT)
    try:
        runner.start()
    except KeyboardInterrupt:
        logger.info("Shutting down the runner server...")
        runner.stop()
        exit(0)


if __name__ == "__main__":
    main()
