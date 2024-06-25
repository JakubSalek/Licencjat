import SETTINGS as S

class Player:
    def __init__(self, id, nickname, color):
        self.__id = id
        self.__nickname = nickname
        self.__found = False
        self.__color = color
        self.__progress = 0
        self.__gold = 5

    def move_player(self, offset) -> bool:
        self.__progress += offset
        
        if self.__progress < 0:
            self.__progress = 0
        
        if self.__progress >= S.TILE_COUNT - 1:
            self.__progress = S.TILE_COUNT - 1
            return True
        return False
    
    def change_gold(self, offset):
        self.__gold += offset

        if self.__gold < 0:
            self.__gold = 0

    def get_progress(self):
        return self.__progress
    
    def get_gold(self):
        return self.__gold
    
    def get_id(self):
        return self.__id
    
    def get_nickname(self):
        return self.__nickname
    
    def get_color(self):
        return self.__color
    
    def get_found(self):
        return self.__found
    
    def set_found(self, found):
        self.__found = found