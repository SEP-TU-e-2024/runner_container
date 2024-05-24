import json
from socket import AF_INET, SHUT_WR, SOCK_STREAM, socket


def main():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(("localhost", 12345))
    sock.listen(10)
    sock.accept()
    
    
    
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
