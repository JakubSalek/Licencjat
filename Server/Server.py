import socket
import threading
from Client import Client
from Table import Table

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients_id = 0
        self.tables_id = 1
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
            client = Client(self.clients_id, client_socket, client_address)
            self.clients_id += 1
            self.clients.append(client)
            threading.Thread(target=self.handle_client, args=(client,)).start()

    def handle_client(self, c: Client):
        response = "Connected"
        self.send_message(response, c)
        response = c.client_socket.recv(1024).decode()
        self.print_coming_message(response, c)
        c.nickname = response
        self.send_message(c.id, c)

        while True:
            response = c.client_socket.recv(1024).decode()
            self.print_coming_message(response, c)

            if response == "Disconnect":
                self.send_message("OKDISCONNECT", c)
                self.clients.remove(c)
                break

            elif response == "Tables":
                self.send_tables(c)
            elif response == "CreateTable":
                self.create_table(c)
        
            elif response == "ChooseTableMenu":
                c.current_menu = response
                self.send_tables(c)

    def send_tables(self, c):
        for table in self.tables:
            message = f"Table;{table.id};{table.name};{len(table.players)}"
            self.send_message(message, c)
    
    # Utwórz nowy stolik
    def create_table(self, c):
        # Stworzenie stolika
        table = Table(self.tables_id, c)
        self.tables_id += 1
        self.tables.append(table)
        
        # Informacja zwrotna
        message = f"CreateTable;{table.id};{table.name}"
        self.send_message(message, c)
        c.current_menu = f"Game;{table.id}"
        
        # Wysłanie informacji do wszystkich pozostałych w tym menu
        for client in self.clients:
            if client.current_menu == "ChooseTableMenu":
                message = f"Table;{table.id};{table.name};{len(table.players)}"
                self.send_message(message, client)


    def send_message(self, message: str, c: Client):
        print(f"Sending response to {c.client_socket} stating \"{message}\"")
        c.client_socket.sendall((str(message)+"$").encode())

    def print_coming_message(self, message, c: Client):
        print(f"Got response from {c.client_socket} stating \"{message}\"")



