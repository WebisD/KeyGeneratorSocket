from multiprocessing import Process
from socket import socket, AF_INET, SOCK_STREAM

from ClientProcess import ClientProcess


class Server:
    host: str
    port: int

    clients_processes: list[ClientProcess]

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.clients_processes = []

    def validate_complexity(self, payload: str) -> bool:
        initial_code, n = (int(value) for value in payload.split())
        return initial_code > 10000000 and 5000 < n < 15000

    def run(self) -> None:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.bind((self.host, self.port))
            sock.listen(5)
            print("Listening at {}:{}".format(self.host, self.port))

            while True:
                connection, address = sock.accept()
                new_client_process = ClientProcess(connection, address)
                self.clients_processes.append(new_client_process)

                new_client_process.start_process(self)
