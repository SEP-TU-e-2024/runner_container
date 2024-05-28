"""
Test judge module.
"""

import errno
import socket
import threading

import protocol
from custom_logger import main_logger
from protocol.commands import Commands

HOST = "localhost"
PORT = 12345

runners = []

logger = main_logger.getChild("judge")
sock_lock = threading.Lock()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1000)


def _handle_connections(client_socket: socket.socket, addr: tuple[str, int]):
    ip, port = addr
    disconnected = False

    try:
        logger.info(
            f"Checking if the runner with IP {ip} on port {port} is initialized correctly..."
        )
        protocol.send_command(client_socket, Commands.CHECK)
        logger.info(f"Runner with IP {ip} on port {port} initialized.")

        # logger.info(f"Trying to retrieve the type of the runner with IP {ip} on port {port}...")
        # protocol.send_command(client_socket, Commands.START)
        # logger.info(f"Runner with IP {ip} on port {port} is of type ... .")

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
    logger.info(f"Judge server started on {HOST}:{PORT}.")

    while True:
        client_socket, addr = sock.accept()

        logger.info(f"Incoming connection from {addr[0]} on port {addr[1]}.")
        thread = threading.Thread(target=_handle_connections, args=(client_socket, addr))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    main()
