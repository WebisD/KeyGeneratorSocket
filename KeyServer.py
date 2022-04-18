import multiprocessing
from socket import socket
from sympy import isprime
from ClientProcess import ClientProcess
from ServerBase import ServerBase
from time import perf_counter


class KeyServer(ServerBase):
    def __init__(self, host: str, port: int):
        super().__init__(host, port)

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


try:
    KeyServer('localhost', 8081).run()
except Exception as ex:
    print(f"\nUnexpected error occurred: {str(ex)}")
finally:
    print("Shutting down server")
    for process in multiprocessing.active_children():
        print(f"Shutting down process {process.pid}")
        process.terminate()
        process.join()
