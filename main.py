"""
The main class of the runner server. It handles the connection to the judge server.
"""

import socket
import sys
from time import sleep

from custom_logger import main_logger
from protocol.runner import RunnerProtocol
from settings import JUDGE_HOST, JUDGE_PORT, RETRY_WAIT

logger = main_logger.getChild("runner")


def _connect(sock: socket):
    logger.info(f"Trying to connect to the Judge server at {JUDGE_HOST}:{JUDGE_PORT} ...")

    while True:
        try:
            sock.connect((JUDGE_HOST, JUDGE_PORT))
            break
        except Exception as e:
            logger.info(
                f"{e}. Failed to connect to judge server. Retrying in 5 seconds...", file=sys.stderr
            )
            sleep(RETRY_WAIT)


def _handle_requests(sock: socket):
    while True:
        RunnerProtocol.receive_command(sock)


def _stop(sock: socket.socket):
    """
    Closes the connection to the judge server.
    """
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()


def main():
    """
    Connect the runner to the judge server and.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    _connect(sock)
    _handle_requests(sock)
    _stop(sock)


if __name__ == "__main__":
    main()
