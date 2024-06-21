import socket
import random
import threading
import SETTINGS as S
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
        response = c.get_client_socket().recv(1024).decode()
        self.print_coming_message(response, c)
        c.nickname = response
        self.send_message(c.get_id(), c)

        while True:
            response: str = c.get_client_socket().recv(1024).decode()
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
                self.delete_table(id)

            elif response.startswith("StartGame"):
                _, id = response.split(";")
                self.start_game(id)
            elif response.startswith("ThrowDice"):
                _, table_id, player_id = response.split(";")
                self.throw_dice(table_id, player_id)
            elif response.startswith("Card"):
                _, material, table_id, player_id, count = response.split(";")
                self.change_material(table_id, player_id, material, count)
            elif response.startswith("EndTurn"):
                self.next_turn(table_id)

            elif response == "ChooseTableMenu":
                c.current_menu = response
                self.send_tables(c)
            elif response == "NONEED":
                c.current_menu = response

    # Wyślij informację o wszystkich stolikach
    def send_tables(self, c):
        for table in self.tables:
            message = f"Table;{table.get_id()};{table.get_name()};{len(table.players)};{1 if table.is_started else 0}"
            self.send_message(message, c)
    
    # Utwórz nowy stolik
    def create_table(self, c):
        # Stworzenie stolika
        table = Table(self.tables_id, c)
        self.tables_id += 1
        self.tables.append(table)
        
        # Informacja zwrotna
        message = f"CreateTable;{table.get_id()};{table.get_name()}"
        self.send_message(message, c)
        c.current_menu = f"Game;{table.id}"
        
        # Wysłanie informacji do wszystkich pozostałych w tym menu
        for client in self.clients:
            if client.current_menu == "ChooseTableMenu":
                message = f"Table;{table.get_id()};{table.get_name()};{len(table.players)};{1 if table.is_started else 0}"
                self.send_message(message, client)

    # Usuń stolik
    def delete_table(self, id):
        my_table = None
        for table in self.tables:
            if str(table.get_id()) == id:
                my_table = table
        
        self.tables.remove(my_table)

        for client in self.clients:
            if client.current_menu == "ChooseTableMenu":
                message = f"DeleteTable;{my_table.get_id()}"
                self.send_message(message, client)

        message = "DeletedTable"
        for player in my_table.players:
            self.send_message(message, player)

    # Dołącz lub opuść stolik
    def join_or_leave_table(self, c, id, is_joining):
        my_table = None
        for table in self.tables:
            if str(table.get_id()) == id:
                my_table = table
        if is_joining:
            c.current_menu = f"Game;{my_table.get_id()}"
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
                message = f"Table;{my_table.get_id()};{my_table.get_name()};{len(my_table.players)};{1 if my_table.is_started else 0}"
                self.send_message(message, client)

    # Wyślij informację o wszystkich graczach
    def send_players(self, table):
        message = "PlayersList"
        for player in table.players:
            message += f";{str(player.get_id())};{player.nickname}"

        for client in self.clients:
            if client.current_menu == f"Game;{table.get_id()}":
                self.send_message(message, client)

    # Roześlij informację o rozpoczęciu gry
    def start_game(self, id):
        my_table = None
        for table in self.tables:
            if str(table.get_id()) == id:
                my_table = table
        
        for client in self.clients:
            if client.current_menu == "ChooseTableMenu":
                message = f"StartTable;{my_table.get_id()}"
                self.send_message(message, client)

        message = "StartGame"
        for player in my_table.players:
            self.send_message(message, player)

    def throw_dice(self, table_id, player_id):
        # Rzut kostką
        move = random.randint(1, 6)

        message = f"DiceThrown;{player_id};{move}"
        for client in self.clients:
            if client.current_menu == f"Game;{table_id}":
                self.send_message(message, client)

        # Losowanie karty
        with open(S.CARDS, 'r', encoding='utf-8') as plik:
            lines = plik.readlines()
            
            self.chosen_line = random.randint(0, len(lines) - 1)
            random_card = lines[self.chosen_line]
        
        message = "Card;" + random_card.strip()
        for client in self.clients:
            if client.current_menu == f"Game;{table_id}":
                self.send_message(message, client)

    def change_material(self, table_id, player_id, material, count):
        message = f"ChangeMaterial;{player_id};{material};{count}"

        for client in self.clients:
            if client.current_menu == f"Game;{table_id}":
                self.send_message(message, client)

    def next_turn(self, table_id):
        message = f"NextTurn"

        for client in self.clients:
            if client.current_menu == f"Game;{table_id}":
                self.send_message(message, client)


    # Wyślij wiadomość do klienta
    def send_message(self, message: str, c: Client):
        print(f"Sending response to {c.get_client_socket()} stating \"{message}\"")
        c.get_client_socket().sendall((str(message)+"$").encode())

    # Wyświetl przychodzącą wiadomość
    def print_coming_message(self, message, c: Client):
        print(f"Got response from {c.get_client_socket()} stating \"{message}\"")



