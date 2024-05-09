import SETTINGS as S

class Player:
    def __init__(self, id, nickname, color):
        self.id = id
        self.nickname = nickname
        self.found = False
        self.color = color
        self.progress = 0
        self.gold = 5

    def move_player(self, offset) -> bool:
        self.progress += offset
        
        if self.progress < 0:
            self.progress = 0
        
        if self.progress > S.TILE_COUNT - 1:
            self.progress = S.TILE_COUNT - 1
            return True
        return False
    
    def change_gold(self, offset):
        self.gold += offset

        if self.gold < 0:
            self.gold = 0