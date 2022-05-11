from multiprocessing import Process
from socket import socket, AF_INET, SOCK_STREAM
from time import perf_counter
import time

class Client:
    execution_time_counter = 0
    count = 0
    clients_amount = 5
    process_list: list[Process] = []

    @staticmethod
    def send_random_payload(sock: socket, process_index: int) -> None:
        with open("random.txt", "r") as file:
            file_lines = file.readlines()

            # map initial code and n as string separated by space
            payloads = [f"{line.split()[0]} {line.split()[1]}" for line in file_lines]

            rows_amount = len(file_lines)//Client.clients_amount

        start_list_index = rows_amount*process_index
        end_list_index = start_list_index + rows_amount

        print(start_list_index, end_list_index)
        for payload in payloads[start_list_index:end_list_index]:

            sock.sendall(payload.encode())
            response = sock.recv(64)
            print(f"Server response: {response.decode()}")

            
            with open("../Statistics/timesAllLUT.txt", 'a') as times_file:
                times_file.write(f'{time.time() - Client.execution_time_counter}\n')

    @staticmethod
    def handle_connection(host: str, port: int, process_index: int) -> None:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect((host, port))
            Client.send_random_payload(sock, process_index)

    def connect_multiple_clients(self, host='localhost', port=8080) -> None:
        Client.execution_time_counter = time.time()

        for process_index in range(Client.clients_amount):
            client_process = Process(target=Client.handle_connection, args=(host, port, process_index))
            Client.process_list.append(client_process)
            client_process.start()

        [process.join() for process in Client.process_list if process.is_alive()]