from socket import socket, AF_INET, SOCK_STREAM
from multiprocessing import Process
from threading import Thread
from time import perf_counter

class KeyServer:
    host: str
    port: int
    file_indexHash = open("indexHash.txt")
    file_primeHash = open("primeHash.txt")
    indexHash_list = file_indexHash.readlines()
    primeHash_list = file_primeHash.readlines()

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    @staticmethod
    def generate_key(payload: str) -> str:
        #start_time = perf_counter()

        initial_code, n = (int(value) for value in payload.split())

        indexHash = int(KeyServer.indexHash_list[initial_code])
        lprimeHash = int(KeyServer.primeHash_list[indexHash-n+1])
        rprimeHash = int(KeyServer.primeHash_list[indexHash+n]) if initial_code != int(KeyServer.primeHash_list[indexHash+1]) else int(KeyServer.primeHash_list[indexHash+n+1])

        result = lprimeHash*rprimeHash

        #finish_time = perf_counter()

        #file = open("../../Statistics/times.txt", 'a')
        #file.write(f'{finish_time-start_time}\n')
        #file.close()

        return str(result)

    @staticmethod
    def connect_client(client_address: str, client_connection: "socket") -> None:
        with client_connection:
            while True:
                payload = client_connection.recv(64).decode()

                if not payload:
                    break

                print(f"Received payload: {payload}")

                generated_key = KeyServer.generate_key(payload)
                client_connection.sendall(generated_key.encode())

        print(f"Client {client_address} has been disconnected\n")

    def start_client_thread(self, client_address: str, client_connection: "socket") -> None:
        client_thread = Thread(
            target=KeyServer.connect_client,
            args=(client_address, client_connection)
        )
        client_thread.start()

    def run(self) -> None:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.bind((self.host, self.port))
            sock.listen(5)
            print("Listening at {}:{}".format(self.host, self.port))
            while True:
                client_connection, client_address = sock.accept()
                client_ip, client_port = client_address
                client_address = f"{client_ip}:{client_port}"

                print(f"Client with address {client_address} has been connected")
                self.start_client_thread(client_address, client_connection)

