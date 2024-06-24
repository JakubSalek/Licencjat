class Table:
    def __init__(self, id, name, player_count, started):
        self.__id = id
        self.__name = name
        self.__player_count = player_count
        self.__players = []
        self.__started = started

    def get_id(self):
        return self.__id
    
    def get_name(self):
        return self.__name
    
    def get_player_count(self):
        return self.__player_count
    
    def set_player_count(self, player_count):
        self.__player_count = player_count
    
    def get_players(self):
        return self.__players()
    
    def get_started(self):
        return self.__started
    
    def set_started(self, started):
        self.__started = started