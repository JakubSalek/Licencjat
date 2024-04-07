import socket
import SETTINGS as s

class Client:
    def __init__(self):
        self.nickname = ""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __del__(self):
        self.client_socket.close()

    def connect(self):
        result = self.client_socket.connect_ex((s.HOST, s.PORT))
        if not result:
            response = self.client_socket.recv(1024).decode()
            if response == "Connected":
                print(f"DEBUG: {response}")
                response = self.nickname
                self.client_socket.sendall(response.encode())
        else:
            print("Can't connect to server!")
            exit()

            