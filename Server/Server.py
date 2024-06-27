import socket
import random
import threading
import SETTINGS as S
from Client import Client
from Table import Table

class Server:
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__clients_id = 0
        self.__tables_id = 1
        self.__tables = []
        self.__clients = []

    def start(self):
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.bind((self.__host, self.__port))
        self.__server_socket.listen(5)
        print(f"Server running on ({self.__host}, {self.__port})")

        while True:
            client_socket, client_address = self.__server_socket.accept()
            print(f"New connection from: {client_address}")
            client = Client(self.__clients_id, client_socket)
            self.__clients_id += 1
            self.__clients.append(client)
            threading.Thread(target=self.__handle_client, args=(client,)).start()

    def __handle_client(self, c: Client):
        response = "Connected"
        self.__send_message(response, c)
        response = c.get_client_socket().recv(1024).decode()
        self.__print_coming_message(response, c)
        c.set_nickname(response)
        self.__send_message(c.get_id(), c)
        client_online = True
        while client_online:
            response: str = c.get_client_socket().recv(1024).decode()
            messages = response.split("$")
            for message in messages:
                self.__print_coming_message(message, c)

                if message == "Disconnect":
                    self.__send_message("OKDISCONNECT", c)
                    self.__clients.remove(c)
                    client_online = False

                elif message == "Tables":
                    self.__send_tables(c)
                elif message == "CreateTable":
                    self.__create_table(c)
                elif message.startswith("JoinTable"):
                    _, id = message.split(";")
                    self.__join_or_leave_table(c, id, True)
                elif message.startswith("LeaveTable"):
                    _, id = message.split(";")
                    self.__join_or_leave_table(c, id, False)
                elif message.startswith("DeleteTable"):
                    _, id = message.split(";")
                    self.__delete_table(id)

                elif message.startswith("StartGame"):
                    _, id = message.split(";")
                    self.__start_game(id)
                elif message.startswith("ThrowDice"):
                    _, table_id, player_id = message.split(";")
                    self.__throw_dice(table_id, player_id)
                elif message.startswith("Card"):
                    _, material, table_id, player_id, count = message.split(";")
                    self.__change_material(table_id, player_id, material, count)
                elif message.startswith("EndTurn"):
                    self.__next_turn(table_id)

                elif message == "ChooseTableMenu":
                    c.set_current_menu(message)
                    self.__send_tables(c)
                elif message == "NONEED":
                    c.set_current_menu(message)

    # Wyślij informację o wszystkich stolikach
    def __send_tables(self, c):
        for table in self.__tables:
            message = (f"Table;{table.get_id()};{table.get_name()};"
                       f"{len(table.get_players())};"
                       f"{1 if table.get_is_started() else 0}")
            self.__send_message(message, c)
    
    # Utwórz nowy stolik
    def __create_table(self, c):
        # Stworzenie stolika
        table = Table(self.__tables_id, c)
        self.__tables_id += 1
        self.__tables.append(table)
        
        # Informacja zwrotna
        message = f"CreateTable;{table.get_id()};{table.get_name()}"
        self.__send_message(message, c)
        c.set_current_menu(f"Game;{table.get_id()}")
        
        # Wysłanie informacji do wszystkich pozostałych w tym menu
        for client in self.__clients:
            if client.get_current_menu() == "ChooseTableMenu":
                message = f"Table;{table.get_id()};{table.get_name()};{len(table.get_players())};{1 if table.get_is_started() else 0}"
                self.__send_message(message, client)

    # Usuń stolik
    def __delete_table(self, id):
        my_table = None
        for table in self.__tables:
            if str(table.get_id()) == id:
                my_table = table
        
        self.__tables.remove(my_table)

        for client in self.__clients:
            if client.get_current_menu() == "ChooseTableMenu":
                message = f"DeleteTable;{my_table.get_id()}"
                self.__send_message(message, client)

        message = "DeletedTable"
        for player in my_table.get_players():
            self.__send_message(message, player)

    # Dołącz lub opuść stolik
    def __join_or_leave_table(self, c, id, is_joining):
        my_table = None
        for table in self.__tables:
            if str(table.get_id()) == id:
                my_table = table
        if is_joining:
            c.set_current_menu(f"Game;{my_table.get_id()}")
            my_table.add_player(c)
        else:
            c.set_current_menu(f"ChooseTableMenu") 
            my_table.remove_player(c)
            self.__send_tables(c)

        # Wyślij wszystkich aktualnych graczy do wszystkich przy stoliku
        self.__send_players(my_table)

        # Wyślij do wszystkich w ChooseTable infomacje o zmianie stolika
        for client in self.__clients:
            if client.get_current_menu() == "ChooseTableMenu":
                message = f"Table;{my_table.get_id()};{my_table.get_name()};{len(my_table.get_players())};{1 if my_table.get_is_started() else 0}"
                self.__send_message(message, client)

    # Wyślij informację o wszystkich graczach
    def __send_players(self, table):
        message = "PlayersList"
        for player in table.get_players():
            message += f";{str(player.get_id())};{player.get_nickname()}"

        for client in self.__clients:
            if client.get_current_menu() == f"Game;{table.get_id()}":
                self.__send_message(message, client)

    # Roześlij informację o rozpoczęciu gry
    def __start_game(self, id):
        my_table = None
        for table in self.__tables:
            if str(table.get_id()) == id:
                my_table = table
        
        for client in self.__clients:
            if client.get_current_menu() == "ChooseTableMenu":
                message = f"StartTable;{my_table.get_id()}"
                self.__send_message(message, client)

        message = "StartGame"
        for player in my_table.get_players():
            self.__send_message(message, player)

    def __throw_dice(self, table_id, player_id):
        # Rzut kostką
        move = random.randint(1, 6)

        message = f"DiceThrown;{player_id};{move}"
        for client in self.__clients:
            if client.get_current_menu() == f"Game;{table_id}":
                self.__send_message(message, client)

        # Losowanie karty
        with open(S.CARDS, 'r', encoding='utf-8') as plik:
            lines = plik.readlines()
            
            chosen_line = random.randint(0, len(lines) - 1)
            random_card = lines[chosen_line]
        
        message = "Card;" + random_card.strip()
        for client in self.__clients:
            if client.get_current_menu() == f"Game;{table_id}":
                self.__send_message(message, client)

    def __change_material(self, table_id, player_id, material, count):
        message = f"ChangeMaterial;{player_id};{material};{count}"

        for client in self.__clients:
            if client.get_current_menu() == f"Game;{table_id}":
                self.__send_message(message, client)

    def __next_turn(self, table_id):
        message = f"NextTurn"

        for client in self.__clients:
            if client.get_current_menu() == f"Game;{table_id}":
                self.__send_message(message, client)


    # Wyślij wiadomość do klienta
    def __send_message(self, message: str, c: Client):
        print(f"Sending response to {c.get_client_socket()} stating \"{message}\"")
        c.get_client_socket().sendall((str(message)+"$").encode())

    # Wyświetl przychodzącą wiadomość
    def __print_coming_message(self, message, c: Client):
        print(f"Got response from {c.get_client_socket()} stating \"{message}\"")



