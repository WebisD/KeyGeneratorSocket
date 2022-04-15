from abc import ABC, abstractmethod
from socket import socket, AF_INET, SOCK_STREAM
from Server.ServerBase.ClientProcess import ClientProcess


class ServerBase(ABC):
    host: str
    port: int

    clients_processes: list[ClientProcess]

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.clients_processes = []

    @abstractmethod
    def start_client_process(self, client_address: str, client_connection: "socket") -> None:
        pass

    def run(self) -> None:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.bind((self.host, self.port))
            sock.listen(5)
            print("Listening at {}:{}".format(self.host, self.port))

            while True:
                client_connection, client_address = sock.accept()

                client_ip, client_port = client_address
                client_address = f"{client_ip}:{client_port}"

                self.start_client_process(client_address, client_connection)

                print(self.clients_processes)
