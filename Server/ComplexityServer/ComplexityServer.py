from multiprocessing import Process
from socket import socket, AF_INET, SOCK_STREAM


class ComplexityServer:
    host: int
    port: int
    clients_processes: list[Process]

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.clients_processes = []

    @staticmethod
    def validate_complexity(payload: str) -> bool:
        initial_code, n = (int(value) for value in payload.split())
        return initial_code > 10000000 and 5000 < n < 15000

    @staticmethod
    def connect_client(client_connection: "socket"):
        with client_connection:
            while True:
                payload = client_connection.recv(1024).decode()

                if not payload:
                    break

                print(f"Received payload: {payload}")
                is_valid_payload = ComplexityServer.validate_complexity(payload)

                if is_valid_payload:
                    with socket(AF_INET, SOCK_STREAM) as key_generator_sock:
                        key_generator_sock.connect(('localhost', 8081))
                        key_generator_sock.sendall(payload.encode())

                        generated_key = key_generator_sock.recv(1024).decode()
                        client_connection.sendall(f"Generated key from {payload} is {generated_key}".encode())
                else:
                    client_connection.sendall(f"{payload} is an invalid payload".encode())

    def start_client_process(self, client_address: str, client_connection: "socket"):
        client_process = Process(
            target=ComplexityServer.connect_client,
            args=(client_connection,)
        )
        client_process.start()

        self.clients_processes.append(client_process)

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

                print(self.clients_processes)
