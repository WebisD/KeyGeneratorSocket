import multiprocessing
from socket import socket, AF_INET, SOCK_STREAM

from ClientProcess import ClientProcess
from ServerBase import ServerBase


class ComplexityServer(ServerBase):
    def __init__(self, host: str, port: int):
        super().__init__(host, port)

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
        process = ClientProcess(
            client_address,
            client_connection,
            target=ComplexityServer.connect_client,
            args=(client_connection,)
        )
        process.start()

        self.clients_processes.append(process)


try:
    ComplexityServer('localhost', 8080).run()
except Exception as ex:
    print(f"\nUnexpected error occurred: {str(ex)}")
finally:
    print("Shutting down server")
    for process in multiprocessing.active_children():
        print(f"Shutting down process {process.pid}")
        process.terminate()
        process.join()
