from socket import socket, AF_INET, SOCK_STREAM

class Server:
    host: str
    port: int

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

                with connection:
                    print(f"New client connected to the server: {address}")

                    while True:
                        payload = connection.recv(1024)

                        if not payload:
                            break

                        payload = payload.decode()

                        print(f"Received payload: {payload}")
                        response_data = "Valid" if self.validate_complexity(payload) else "Invalid"

                        connection.sendall(f"{response_data} payload".encode())