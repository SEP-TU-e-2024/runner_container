import threading


def main():
    # listen for web requests

    main.start()
    
    while True:
        main.await_request()
        threading.Thread(target=None).start()
        
        
        pass
    
    # sock.listen(1)

    # while True:
    #     client_sock, _ = sock.accept()
    #     client_sock.settimeout(5)

    #     databuffer = bytearray()

    #     recv_data = 1
    #     while recv_data:
    #         recv_data = client_sock.recv(1024)
    #         databuffer = databuffer + recv_data

    #     client_sock.shutdown(SHUT_RD)

    #     databuffer = databuffer.decode()
    #     json_obj = json.loads(databuffer)

    #     print(json_obj)

    #     databuffer = bytearray()
    #     result = {"Sigma" : "YES", "test" : [1, 2, 3]}

    #     json_obj = json.dumps(result)

    #     client_sock.send(json_obj.encode())

    #     client_sock.shutdown(SHUT_WR)
    #     client_sock.close()


if __name__ == "__main__":
    main()
