from socket import socket, SOCK_STREAM, AF_INET, SHUT_WR
import json


def main():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(("localhost", 12345))

    json_obj = {"Question": "What the sigma?"}
    data = json.dumps(json_obj)

    sock.send(data.encode())
    sock.shutdown(SHUT_WR)

    databuffer = bytearray()
    recv_data = 1
    while recv_data:
        recv_data = sock.recv(1024)
        databuffer = databuffer + recv_data

    json_obj = json.loads(databuffer.decode())

    print(json_obj)
    sock.close()


if __name__ == "__main__":
    main()
