import socket
import threading

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.tables = []
        self.clients = []

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server running on: {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"New connection from: {client_address}")
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def client_wants_table(self, client_socket):
        if len(self.tables) == 0:
            self.print_sent_message(b"No Tables", client_socket)
            client_socket.sendall(b"No Tables")
        else:
            self.print_sent_message(b"Tables", client_socket)
            client_socket.sendall(b"Tables")
            for table in self.tables:
                self.print_sent_message(f"Table {table.id}: {len(table.players)}/4 graczy\n".encode())
                client_socket.sendall(f"Table {table.id}: {len(table.players)}/4 graczy\n".encode()) 

    def handle_client(self, client_socket):
        client_socket.sendall(b"Connected!\n")

        while True:
            response = client_socket.recv(1024)
            if response == b"Active Tables":
                self.print_coming_message(response, client_socket)
                self.client_wants_table(client_socket)
            # client_socket.sendall(b"Dostepne stoliki:\n")
            # for table in self.tables:
            #     client_socket.sendall(f"Stolik {table.id}: {len(table.players)}/4 graczy\n".encode())

            # choice = client_socket.recv(1024).decode().strip()

            # try:
            #     table_id = int(choice)
            #     if 0 <= table_id < len(self.tables):
            #         if self.tables[table_id].add_player(client_socket):
            #             client_socket.sendall(f"Dolaczono do stolika {table_id}\n".encode())
            #             break
            #         else:
            #             client_socket.sendall(b"Stolik pelny, wybierz inny.\n")
            #     else:
            #         client_socket.sendall(b"Niepoprawny numer stolika, wybierz ponownie.\n")
            # except ValueError:
            #     client_socket.sendall(b"Niepoprawny wybor, wybierz numer stolika.\n")

        client_socket.close()
    
    def print_coming_message(self, message, client_socket):
        print(f"Got response from {client_socket} stating \"{message}\"")
    
    def print_sent_message(self, message, client_socket):
        print(f"Sending response to {client_socket} stating \"{message}\"")


