import json
from socket import socket, AF_INET, SOCK_STREAM, SHUT_RD, SHUT_WR

def main():
    # listen for web requests

    PORT = 12345  # change this later

    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(("localhost", PORT))
    sock.listen(1)

    while True:
        client_sock, addr = sock.accept()
        client_sock.settimeout(5)

        databuffer = bytearray()

        recv_data = 1
        while recv_data:
            recv_data = client_sock.recv(1024)
            databuffer = databuffer + recv_data

        client_sock.shutdown(SHUT_RD)

        databuffer = databuffer.decode()
        json_obj = json.loads(databuffer)

        print(json_obj)

        databuffer = bytearray()
        result = {"Sigma" : "YES", "test" : [1, 2, 3]}

        json_obj = json.dumps(result)

        client_sock.send(json_obj.encode())

        client_sock.shutdown(SHUT_WR)
        client_sock.close()


if __name__ == "__main__":
    main()
