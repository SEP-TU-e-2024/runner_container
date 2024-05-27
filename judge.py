import errno
import socket
import threading

import protocol
from custom_logger import main_logger

logger = main_logger.getChild("judge")
sock_lock = threading.Lock()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 12345))
sock.listen(1000)


def _handle_requests(client_socket: socket.socket, addr: tuple[str, int]):
    ip, port = addr
    disconnected = False

    logger.info(f"Waiting for initalization message of the runner with IP {ip} on port {port}.")
    try:
        protocol.receive_init(client_socket)
        logger.info(f"Runner with IP {ip} on port {port} initialized.")

    except socket.timeout:
        logger.error(f"Runner with IP {ip} on port {port} timed out.")

    except ValueError as e:
        logger.error(f"Runner with IP {ip} on port {port} sent invalid init message. {e}")

    except OSError as e:
        if e.errno == errno.ENOTCONN:
            disconnected = True
            logger.error(f"Runner with IP {ip} on port {port} disconnected.")

    finally:
        if not disconnected:
            client_socket.shutdown(socket.SHUT_RDWR)
            client_socket.close()
        pass


def main():
    while True:
        client_socket, addr = sock.accept()

        logger.info(f"Incoming connection from {addr[0]} on port {addr[1]}.")
        thread = threading.Thread(target=_handle_requests, args=(client_socket, addr))
        thread.daemon = True
        thread.start()

    # json_obj = {"Question": "What the sigma?"}
    # data = json.dumps(json_obj)

    # sock.send(data.encode())
    # sock.shutdown(SHUT_WR)

    # databuffer = bytearray()
    # recv_data = 1
    # while recv_data:
    #     recv_data = sock.recv(1024)
    #     databuffer = databuffer + recv_data

    # json_obj = json.loads(databuffer.decode())

    # print(json_obj)
    # sock.close()


if __name__ == "__main__":
    main()
