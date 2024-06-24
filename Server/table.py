class Table:
    def __init__(self, id, owner):
        self.__id = id
        self.__name = f"{owner.nickname}'s table"
        self.__players = [owner]
        self.__is_started = False

    def get_id(self):
        return self.__id
    
    def get_name(self):
        return self.__name
    
    def get_players(self):
        return self.__players
    
    def add_player(self, player):
        self.__players.append(player)

    def remove_player(self, player):
        self.__players.remove(player)

    def get_is_started(self):
        return self.__is_started
    
    def set_is_started(self, is_started):
        self.__is_started = is_started