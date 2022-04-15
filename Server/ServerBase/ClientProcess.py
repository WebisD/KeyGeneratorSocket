from collections import Callable
from socket import socket
from multiprocessing import Process


class ClientProcess(Process):
    client_address: str
    client_connection: "socket"
    on_stop_process: Callable[["ClientProcess"], None]

    def __init__(self, client_address: str, client_connection: "socket", **kwargs):
        super().__init__(**kwargs)
        self.client_address = client_address
        self.client_connection = client_connection

    def run(self):
        print(f"Client with address {self.client_address} has been connected")
        super().run()
        print(f"Client {self.client_address} has been disconnected\n")

    def shutdown_process(self) -> None:
        self.terminate()
        self.join()
