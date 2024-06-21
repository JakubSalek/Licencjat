class Table:
    def __init__(self, id, owner):
        self.id = id
        self.name = f"{owner.nickname}'s table"
        self.players = [owner]
        self.is_started = False

    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_players(self):
        return self.players