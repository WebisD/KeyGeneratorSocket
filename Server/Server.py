from multiprocessing import Process
from socket import socket, AF_INET, SOCK_STREAM

from ClientProcess import ClientProcess


class Server:
    host: str
    port: int

    clientsProcesses: list[ClientProcess] = []

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def validate_complexity(self, payload: str):
        initial_code, n = (int(value) for value in payload.split())
        return initial_code > 10000000 and 5000 < n < 15000

    def run(self) -> None:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.bind((self.host, self.port))
            sock.listen(5)
            print("Listening at {}:{}".format(self.host, self.port))

            while True:
                connection, address = sock.accept()
                newClientProcess = ClientProcess(connection, address)
                process = Process(target=lambda: ClientProcess.client_connection(newClientProcess, self))

                self.clientsProcesses.append(newClientProcess)
