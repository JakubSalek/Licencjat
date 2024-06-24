class Client:
    def __init__(self, id, client_socket):
        self.__id = id
        self.__client_socket = client_socket
        self.__nickname = ''
        self.__current_menu = "NONEED"

    def get_id(self):
        return self.__id
    
    def get_client_socket(self):
        return self.__client_socket
    
    def set_nickname(self, nickname):
        self.__nickname = nickname

    def get_nickname(self):
        return self.__nickname
    
    def set_current_menu(self, current_menu):
        self.__current_menu = current_menu

    def get_current_menu(self):
        return self.__current_menu