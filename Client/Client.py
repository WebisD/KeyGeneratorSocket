from socket import socket, AF_INET, SOCK_STREAM
from time import perf_counter

class Client:
    def send_random_payload(self, sock: socket) -> None:
        with open("random.txt", "r") as file:
            # map initial code and n as string separated by space
            payloads = [f"{line.split()[0]} {line.split()[1]}" for line in file.readlines()]

        total = 0
        for payload in payloads:
            start_time = perf_counter()
            sock.sendall(payload.encode())
            response = sock.recv(1024)
            print(f"Server response: {response.decode()}")
            finish_time = perf_counter()

            total += finish_time-start_time
            if round(total) == 6:
                print(total)
                break
            file = open("../Statistics/timesAllLUT.txt", 'a')
            file.write(f'{finish_time-start_time}\n')
            file.close()

    
    def connect(self, host='localhost', port=8080) -> None:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect((host, port))

            self.send_random_payload(sock)
            while True:
                pass
