from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


class ComplexityServer:
    host: str
    port: int

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    @staticmethod
    def validate_complexity(payload: str) -> bool:
        initial_code, n = (int(value) for value in payload.split())
        return initial_code > 10000000 and 5000 < n < 15000

    @staticmethod
    def connect_client(client_address: str, client_connection: "socket"):
        with client_connection:
            while True:
                payload = client_connection.recv(64).decode()
                if not payload:
                    break
                print(f"Received payload: {payload}")
                is_valid_payload = ComplexityServer.validate_complexity(payload)
                if is_valid_payload:
                    with socket(AF_INET, SOCK_STREAM) as key_generator_sock:
                        key_generator_sock.connect(('localhost', 8081))
                        key_generator_sock.sendall(payload.encode())
                        generated_key = key_generator_sock.recv(64).decode()
                        client_connection.sendall(f"Generated key from {payload} is {generated_key}".encode())
                else:
                    client_connection.sendall(f"{payload} is an invalid payload".encode())

        print(f"Client {client_address} has been disconnected\n")

    def start_client_thread(self, client_address: str, client_connection: "socket"):
        client_thread = Thread(
            target=ComplexityServer.connect_client,
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
