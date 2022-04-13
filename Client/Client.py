from socket import socket, AF_INET, SOCK_STREAM


class Client:
    def send_random_payload(self, sock: socket) -> None:
        with open("random.txt", "r") as file:
            # map to string with format initial code and n separated by space
            payloads = [f"{line.split()[0]} {line.split()[1]}" for line in file.readlines()]

        for payload in payloads:
            sock.sendall(payload.encode())
            response = sock.recv(1024)
            print(f"Server response: {response.decode()}")

    def connect(self, host='localhost', port=8080) -> None:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect((host, port))
            print(sock)
            self.send_random_payload(sock)
            # sock.sendall()
            # response = sock.recv(1024)
            # print(f"Server response: {response.decode()}")
