"""
The main class of the runner server. It handles the connection to the judge server.
"""

import socket
import threading
from time import sleep

from custom_logger import main_logger
from protocol import Connection
from protocol.runner import RunnerProtocol
from settings import JUDGE_HOST, JUDGE_PORT, RETRY_WAIT

logger = main_logger.getChild("runner")


class Runner:
    ip: str
    port: int
    debug: bool
    connection: Connection

    def __init__(self, ip, port, debug=False):
        self.ip = ip
        self.port = port
        self.debug = debug

    def start(self):
        logger.info(f"Trying to connect to the Judge server at {self.ip}:{self.port} ...")

        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.ip, self.port))
                self.connection = Connection(self.ip, self.port, sock, threading.Lock())
                self._handle_commands()

            except (ConnectionRefusedError, ConnectionResetError) as e:
                logger.info(f"{e}. Failed to connect to judge server. Retrying in 5 seconds...")
                sleep(RETRY_WAIT)

            finally:
                self.stop()

    def _handle_commands(self):
        while True:
            RunnerProtocol.receive_command(self.connection)

    def stop(self):
        """
        Closes the connection to the judge server.
        """
        if self.connection is not None:
            sock = self.connection.sock
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
        self.connection = None


def main():
    runner = Runner(JUDGE_HOST, JUDGE_PORT)
    try:
        runner.start()
    except KeyboardInterrupt:
        logger.info("Shutting down the runner server...")
        runner.stop()
        exit(0)


if __name__ == "__main__":
    main()
