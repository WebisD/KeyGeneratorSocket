from socket import socket
from sympy import nextprime, prevprime
from Server.ServerBase.ClientProcess import ClientProcess
from Server.ServerBase.ServerBase import ServerBase


class KeyServer(ServerBase):
    def __init__(self, host: str, port: int):
        super().__init__(host, port)

    @staticmethod
    def generate_key(payload: str) -> str:
        initial_code, n = (int(value) for value in payload.split())

        lower_prime = upper_prime = initial_code

        primes_counter = 0
        while primes_counter < n:
            lower_prime = prevprime(lower_prime)
            upper_prime = nextprime(upper_prime)
            primes_counter += 1
            print(f"lower_prime: {lower_prime}, upper_prime: {upper_prime}, counter: {primes_counter}")

        return str(lower_prime * upper_prime)

    @staticmethod
    def connect_client(client_connection: "socket") -> None:
        with client_connection:
            while True:
                payload = client_connection.recv(1024).decode()

                if not payload:
                    break

                print(f"Received payload: {payload}")

                generated_key = KeyServer.generate_key(payload)
                client_connection.sendall(generated_key.encode())

    def start_client_process(self, client_address: str, client_connection: "socket") -> None:
        process = ClientProcess(
            client_address,
            client_connection,
            target=KeyServer.connect_client,
            args=(client_connection,)
        )
        process.start()

        self.clients_processes.append(process)

