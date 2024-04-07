import socket
import threading
from Client import Client

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients_id = 0
        self.tables = []
        self.clients = []

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server running on ({self.host}, {self.port})")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"New connection from: {client_address}")
            client = Client(id, client_socket, client_address)
            self.clients.append(client)
            threading.Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, c: Client):
        self.send_message("Connected", c)
        response = "Connected"
        c.client_socket.sendall(b"Connected")
        response = c.client_socket.recv(1024).decode()
        self.print_coming_message(response, c)
        c.nickname = response

        while True:
            pass

    def client_wants_table(self, c):
        if len(self.tables) == 0:
            self.print_sent_message(b"No Tables", c.client_socket)
            c.client_socket.sendall(b"No Tables")
        else:
            self.print_sent_message(b"Tables", c.client_socket)
            c.client_socket.sendall(b"Tables")
            for table in self.tables:
                self.print_sent_message(f"Table {table.id}: {len(table.players)}/4 graczy\n".encode())
                c.client_socket.sendall(f"Table {table.id}: {len(table.players)}/4 graczy\n".encode()) 

    def send_message(self, message: str, c: Client):
        print(f"Sending response to {c.client_socket} stating \"{message}\"")
        c.client_socket.sendall(message.encode())

    def print_coming_message(self, message, c: Client):
        print(f"Got response from {c.client_socket} stating \"{message}\"")



