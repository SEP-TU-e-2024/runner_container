"""
Judge module used for testing the protocol between the judge and a runner (or possibly multiple ones).
"""

import errno
import socket
import threading

from custom_logger import main_logger
from protocol import Connection
from protocol.judge import Commands, Protocol

HOST = "localhost"
PORT = 12345  # Find a nicer port number

runners = []

logger = main_logger.getChild("judge")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1000)


def _receiver(connection: Connection, reponses: dict[str, dict]):
    while True:
        # Protocol.receive_command(connection)
        pass


def _handle_connections(client_socket: socket.socket, addr: tuple[str, int]):
    """
    Sends commands to the runners.
    """

    ip, port = addr
    connection = Connection(ip, port, client_socket, threading.Lock())
    disconnected = False

    # commands_sent = []
    responses_received = []

    receiver_thread = threading.Thread(target=_receiver, args=(connection, responses_received))
    receiver_thread.daemon = True
    receiver_thread.start()

    try:
        logger.info(
            f"Checking if the runner with IP {ip} on port {port} is initialized correctly..."
        )
        Protocol.send_command(connection, Commands.CHECK)
        logger.info(f"Runner with IP {ip} on port {port} initialized.")

        Protocol.send_command(connection, Commands.START)

    except socket.timeout:
        logger.error(f"Runner with IP {ip} on port {port} timed out.")

    except ValueError as e:
        logger.error(f"Runner with IP {ip} on port {port} sent invalid init message. {e}")

    except OSError as e:
        if e.errno == errno.ENOTCONN:
            disconnected = True
            logger.error(f"Runner with IP {ip} on port {port} disconnected.")

    except Exception as e:
        logger.error(f"Unexpected error occured: {e}")

    finally:
        if not disconnected:
            client_socket.shutdown(socket.SHUT_RDWR)
            client_socket.close()
        pass


def main():
    """
    The main function.
    """
    logger.info(f"Judge server started on {HOST}:{PORT}.")

    while True:
        client_socket, addr = sock.accept()

        logger.info(f"Incoming connection from {addr[0]} on port {addr[1]}.")
        thread = threading.Thread(target=_handle_connections, args=(client_socket, addr))
        thread.daemon = True
        thread.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Shutting down the judge server...")
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        exit(0)
