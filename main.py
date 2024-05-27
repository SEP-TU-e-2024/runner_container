import socket
import sys
from time import sleep

import protocol
from custom_logger import main_logger

JUDGE_HOST = "localhost"  # TODO: change this to the judge local IP
PORT = 12345  # TODO: find a nice port to use

logger = main_logger.getChild("runner")


def _connect(sock: socket):
    logger.info(f"Trying to connect to the Judge server at {JUDGE_HOST}:{PORT} ...")
    
    while True:
        try:
            sock.connect((JUDGE_HOST, PORT))
            break
        except Exception as e:
            logger.info(
                f"{e}. Failed to connect to judge server. Retrying in 5 seconds...", file=sys.stderr
            )
            sleep(5)


def _handle_requests(sock: socket):
    
    protocol.send_init(sock)

    # while True:
    #     databuffer = bytearray()

    #     recv_data = 1
    #     while recv_data:
    #         recv_data = sock.recv(1024)
    #         databuffer = databuffer + recv_data

    #     databuffer = databuffer.decode()

    pass


def _stop(sock: socket):
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
