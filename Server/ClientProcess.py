import socket
from typing import Any

from Server import Server


class ClientProcess:
    client_address: str
    client_connection: Any()

    def __init__(self, client_connection: Any(), client_address: str):
        self.client_connection = client_connection
        self.client_address = client_address

    @staticmethod
    def connect_client(process: "ClientProcess", server: Server):
        with process.client_connection:
            while True:
                payload = process.client_connection.recv(1024).decode()

                if not payload:
                    break

                print(f"Received payload: {payload}")
                response_data = "Valid" if server.validate_complexity(payload) else "Invalid"

                process.client_connection.sendall(f"{response_data} payload".encode())
