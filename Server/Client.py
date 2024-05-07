class Client:
    def __init__(self, id, client_socket, client_address):
        self.id = id
        self.client_socket = client_socket
        self. client_address = client_address
        self.nickname = ''
        self.current_menu = "NONEED"