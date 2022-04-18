from socket import socket, AF_INET, SOCK_STREAM


class Client:
    def send_random_payload(self, sock: socket) -> None:
        with open("random.txt", "r") as file:
            # map initial code and n as string separated by space
            payloads = [f"{line.split()[0]} {line.split()[1]}" for line in file.readlines()]

        for payload in payloads:
            sock.sendall(payload.encode())
            response = sock.recv(1024)
            print(f"Server response: {response.decode()}")

    def connect(self, host='localhost', port=8080) -> None:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect((host, port))

            self.send_random_payload(sock)
            while True:
                pass

print("oi")
Client().connect()
