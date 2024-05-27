import json
import socket


def send(message: dict, sock: socket.socket):
    """
    Sends a json message.
    """
    json_message = json.dumps(message)
    data = json_message.encode()
    data_size = len(data)
    print(data_size)
    sock.sendall(data_size.to_bytes(4, byteorder="big"))
    sock.sendall(data)

    pass


def receive(sock: socket.socket, timeout: int = 0) -> dict:
    """
    Receive a json message.
    """

    sock.settimeout(timeout)
    data_size = int.from_bytes(sock.recv(4), byteorder="big")
    sock.settimeout(0)

    print(data_size)

    data = sock.recv(data_size)
    message = json.loads(data.decode())

    return message


def send_init(sock: socket.socket):
    message = {"status": "ready"}
    send(message, sock)


def receive_init(sock: socket.socket):
    message = receive(sock, 5)

    if message["status"] is None:
        raise ValueError("Received message with missing status!")

    status = message["status"]

    if status != "ready":
        raise ValueError(f'Unexpected respone! Expected "ready" and got "{status}"')
