from socket import socket, AF_INET, SOCK_STREAM
from sympy import isprime
from multiprocessing import Process
from time import perf_counter
import meissel_lehmer_algorithm

class KeyServer:
    host: str
    port: int

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    @staticmethod
    def generate_key(payload: str) -> str:
        start_time = perf_counter()

        initial_code, n = (int(value) for value in payload.split())

        result = meissel_lehmer_algorithm.find_thprime(initial_code, n)

        finish_time = perf_counter()

        return str(result) + f" Time: {(finish_time-start_time):.6f}"

    @staticmethod
    def connect_client(client_address: str, client_connection: "socket") -> None:
        with client_connection:
            while True:
                payload = client_connection.recv(1024).decode()

                if not payload:
                    break

                print(f"Received payload: {payload}")

                generated_key = KeyServer.generate_key(payload)
                client_connection.sendall(generated_key.encode())

        print(f"Client {client_address} has been disconnected\n")

    def start_client_process(self, client_address: str, client_connection: "socket") -> None:
        client_process = Process(
            target=KeyServer.connect_client,
            args=(client_address, client_connection)
        )
        client_process.start()

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
                self.start_client_process(client_address, client_connection)

