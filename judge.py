"""
Judge module used for testing the protocol between the judge and a runner (or possibly multiple ones).
"""

import errno
import socket
import threading

from custom_logger import main_logger
from protocol import Connection
from protocol.judge import Commands, Protocol
from settings import JUDGE_PORT

HOST = "localhost"  # Replace with local IP of the judge machine
PORT = JUDGE_PORT  # Find a nicer port number

logger = main_logger.getChild("judge")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1000)


def _handle_connections(client_socket: socket.socket, addr: tuple[str, int]):
    """
    Sends commands to the runners.
    """

    ip, port = addr
    connection = Connection(ip, port, client_socket, threading.Lock())
    disconnected = False
    protocol = Protocol(connection)

    try:
        # The first command is the first command that should be sent. It tests if the runner is connected correctly.
        protocol.send_command(Commands.CHECK, block=True)

        # Test multiple commands running at the same time
        protocol.send_command(Commands.CHECK)
        protocol.send_command(Commands.CHECK)
        protocol.send_command(Commands.CHECK)
        protocol.send_command(Commands.START)
        protocol.send_command(Commands.START)
        protocol.send_command(Commands.START)
        protocol.send_command(Commands.START)
        protocol.send_command(Commands.CHECK)
        protocol.send_command(Commands.CHECK)
        protocol.send_command(Commands.CHECK)

        # TODO: Run until the runner or the judge closes the connection
        while True:
            pass

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
    The main function of the test judge.
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
