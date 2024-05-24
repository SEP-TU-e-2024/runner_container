import json
import sys
from socket import AF_INET, SHUT_RD, SHUT_RDWR, SHUT_WR, SOCK_STREAM, socket
from time import sleep

JUDGE_HOST = "localhost"  # TODO: change this to the judge IP
PORT = 12345  # TODO: find a nice port to use


def _connect(sock: socket):
    while True:
        try:
            sock.connect((JUDGE_HOST, PORT))
            break
        except Exception as e:
            print(
                f"{e}. Failed to connect to judge server. Retrying in 5 seconds...", file=sys.stderr
            )
            sleep(5)


def _handle_requests(sock: socket):
    message = {"status": "ready"}
    data = json.dumps(message)
    sock.send(data.encode())

    while True:
        databuffer = bytearray()

        recv_data = 1
        while recv_data:
            recv_data = sock.recv(1024)
            databuffer = databuffer + recv_data

        databuffer = databuffer.decode()

    pass


def _stop(sock: socket):
    """
    Closes the connection to the judge server.
    """
    sock.shutdown(SHUT_RDWR)
    sock.close()


def main():
    """
    Connect the runner to the judge server and.
    """
    sock = socket(AF_INET, SOCK_STREAM)
    # sock.settimeout(5)

    _connect(sock)
    _handle_requests(sock)
    _stop(sock)


if __name__ == "__main__":
    main()
