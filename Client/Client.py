import socket
import threading
import sys
import SETTINGS as S

class Client(threading.Thread):
    def __init__(self, queue):
        super().__init__()

        self.nickname = ""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False
        self.is_running = False
        self.message_queue = queue

    def connect(self):
        if not self.is_connected:
            result = self.client_socket.connect_ex((S.HOST, S.PORT))
            if not result:
                response = self.client_socket.recv(1024).decode()
                if response == "Connected$":
                    self.is_connected = True
                    print(f"DEBUG: {response}") if S.DEBUG else None
                    response = self.nickname
                    self.client_socket.sendall(response.encode())
                    self.start()
                    return 0
            else:
                return -1
        else:
            return 1

    def create_table(self):
        message = "CreateTable"
        self.client_socket.sendall(message.encode())

    def send_menu(self, menu):
        message = menu
        self.client_socket.sendall(message.encode())

    def send_disconnect(self):
        self.client_socket.sendall("Disconnect".encode())

    def run(self):
        self.is_running = True
        while self.is_running:
            message = self.client_socket.recv(1024).decode()
            messages = message.split('$')
            for mess in messages:
                if mess != "":
                    self.message_queue.put_nowait(mess)
                    print(f"DEBUG: Got message \"{mess}\"") if S.DEBUG else None
                    if mess == "OKDISCONNECT":
                        self.is_running = False

        self.client_socket.close()