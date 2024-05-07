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
            response: str = c.client_socket.recv(1024).decode()
            self.print_coming_message(response, c)

            if response == "Disconnect":
                self.send_message("OKDISCONNECT", c)
                self.clients.remove(c)
                break

            elif response == "Tables":
                self.send_tables(c)
            elif response == "CreateTable":
                self.create_table(c)
            elif response.startswith("JoinTable"):
                _, id = response.split(";")
                self.join_or_leave_table(c, id, True)
            elif response.startswith("LeaveTable"):
                _, id = response.split(";")
                self.join_or_leave_table(c, id, False)
            elif response.startswith("DeleteTable"):
                _, id = response.split(";")
                self.delete_table(c, id)
        
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

    def delete_table(self, c, id):
        my_table = None
        for table in self.tables:
            if str(table.id) == id:
                my_table = table
        
        self.tables.remove(my_table)

        for client in self.clients:
            if client.current_menu == "ChooseTableMenu":
                message = f"DeleteTable;{my_table.id}"
                self.send_message(message, client)

        message = "TableDeleted"
        for player in my_table.players:
            self.send_message(message, player)


    def join_or_leave_table(self, c, id, is_joining):
        my_table = None
        for table in self.tables:
            if str(table.id) == id:
                my_table = table
        if is_joining:
            c.current_menu = f"Game;{my_table.id}"
            my_table.players.append(c) 
        else:
            c.current_menu = f"ChooseTableMenu"
            my_table.players.remove(c)
            self.send_tables(c)

        # Wyślij wszystkich aktualnych graczy do wszystkich przy stoliku
        self.send_players(my_table)

        # Wyślij do wszystkich w ChooseTable infomacje o zmianie stolika
        for client in self.clients:
            if client.current_menu == "ChooseTableMenu":
                message = f"Table;{my_table.id};{my_table.name};{len(my_table.players)}"
                self.send_message(message, client)

    def send_players(self, table):
        message = "PlayersList"
        for player in table.players:
            message += f";{str(player.id)};{player.nickname}"

        for client in self.clients:
            if client.current_menu == f"Game;{table.id}":
                self.send_message(message, client)


    def send_message(self, message: str, c: Client):
        print(f"Sending response to {c.client_socket} stating \"{message}\"")
        c.client_socket.sendall((str(message)+"$").encode())

    def print_coming_message(self, message, c: Client):
        print(f"Got response from {c.client_socket} stating \"{message}\"")



