from typing import TYPE_CHECKING
from multiprocessing import Process

if TYPE_CHECKING:
    from Server import Server
    from socket import socket


class ClientProcess:
    process: Process
    client_address: str
    client_connection: "socket"

    def __init__(self, client_connection: "socket", client_address: str):
        self.client_address = client_address
        self.client_connection = client_connection

    @staticmethod
    def connect_client(process: "ClientProcess", server: "Server"):
        with process.client_connection:
            while True:
                payload = process.client_connection.recv(1024).decode()

                if not payload:
                    break

                print(f"Received payload: {payload}")
                response_data = "Valid" if server.validate_complexity(payload) else "Invalid"

                process.client_connection.sendall(f"{response_data} payload".encode())

        server.clients_processes.remove(process)

    def start_process(self, server: "Server"):
        self.process = Process(target=ClientProcess.connect_client, args=(self, server))
        self.process.start()

    def kill_process(self):
        self.process.kill()
