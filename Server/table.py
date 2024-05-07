class Table:
    def __init__(self, id, owner):
        self.id = id
        self.name = f"{owner.nickname}'s table"
        self.players = [owner]

    def add_player(self, player):
        if len(self.players) < 4:
            self.players.append(player)
            return True
        else:
            return False