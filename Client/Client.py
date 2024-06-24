import socket
import threading
import SETTINGS as S

class Client(threading.Thread):
    def __init__(self, queue):
        super().__init__()

        self.__nickname = ""
        self.__id = -1
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__is_connected = False
        self.__is_running = False
        self.__message_queue = queue

    def connect(self):
        if not self.__is_connected:
            result = self.__client_socket.connect_ex((S.HOST, S.PORT))
            if not result:
                response = self.__client_socket.recv(1024).decode()
                if response == "Connected$":
                    self.__is_connected = True
                    print(f"DEBUG: {response}") if S.DEBUG else None
                    response = self.__nickname
                    self.__client_socket.sendall(response.encode())
                    response = self.__client_socket.recv(1024).decode()
                    self.__id, _ = response.split('$')
                    self.start()
                    return 0
            else:
                return -1
        else:
            return 1

    def run(self):
        self.__is_running = True
        while self.__is_running:
            response = self.__client_socket.recv(1024).decode()
            messages = response.split('$')
            for message in messages:
                if message != "":
                    self.__message_queue.put_nowait(message)
                    print(f"DEBUG: Got message \"{message}\"") if S.DEBUG else None
                    if message == "OKDISCONNECT":
                        self.__is_running = False
        self.__client_socket.close()

    def get_is_running(self):
        return self.__is_running
    
    def get_id(self):
        return self.__id

    def set_nickname(self, nickname):
        self.__nickname = nickname

    def get_nickname(self):
        return self.__nickname

    def send_message(self, message):
        self.__client_socket.sendall((str(message)+"$").encode())

    def create_table(self):
        self.send_message("CreateTable")

    def join_table(self, table):
        self.send_message(f"JoinTable;{table.get_id()}")
    
    def leave_table(self, table):
        self.send_message(f"LeaveTable;{table.get_id()}")

    def delete_table(self, table):
        self.send_message(f"DeleteTable;{table.get_id()}")

    def start_game(self, table):
        self.send_message(f"StartGame;{table.get_id()}")

    def send_menu(self, menu):
        self.send_message(menu)

    def send_disconnect(self):
        self.send_message("Disconnect")

    def throw_dice(self, table):
        self.send_message(f"ThrowDice;{table.get_id()};{self.__id}")

    def card_confirm(self, table, card):
        type = card.get_type()
        if type == "GAIN":
            self.send_message(f"Card;Gold;{table.get_id()};{self.__id};{card.get_material_count()}")
        elif type == "MOVE":
            self.send_message(f"Card;Progress;{table.get_id()};{self.__id};{card.get_material_count()}")
        self.end_turn()

    def attack_player(self, table, player_id, card):
        if card.get_type() == "ATTACK":
            attack_material = card.get_attack_material()
            self.send_message(f"Card;{attack_material};{table.get_id()};{player_id};{card.get_amount_taken()}")
            self.send_message(f"Card;{attack_material};{table.get_id()};{self.__id};{card.get_amount_received()}")

    def end_turn(self):
        self.send_message("EndTurn")