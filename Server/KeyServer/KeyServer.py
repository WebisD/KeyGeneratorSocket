from socket import socket, AF_INET, SOCK_STREAM
from sympy import isprime
from multiprocessing import Process
from time import perf_counter


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

        upper_prime = lower_prime = initial_code
        upper_primes_counter = lower_primes_counter = 0

        while upper_primes_counter < n or lower_primes_counter < n:
            if upper_primes_counter < n:
                upper_prime += 1

                if isprime(upper_prime):
                    upper_primes_counter += 1

            if lower_primes_counter < n:
                lower_prime -= 1

                if isprime(lower_prime):
                    lower_primes_counter += 1

        print(upper_prime, upper_primes_counter)
        print(lower_prime, lower_primes_counter)

        finish_time = perf_counter()

        return str(lower_prime * upper_prime) + f" Time: {(finish_time-start_time):.6f}"

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

