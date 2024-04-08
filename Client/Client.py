import socket
import SETTINGS as s

class Client:
    def __init__(self):
        self.nickname = ""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False

    def __del__(self):
        self.client_socket.close()

    def connect(self):
        if not self.is_connected:
            result = self.client_socket.connect_ex((s.HOST, s.PORT))
            if not result:
                response = self.client_socket.recv(1024).decode()
                if response == "Connected":
                    self.is_connected = True
                    print(f"DEBUG: {response}")
                    response = self.nickname
                    self.client_socket.sendall(response.encode())
                    return 0
            else:
                return -1
        else:
            return -1

            