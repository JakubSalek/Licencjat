class Table:
    def __init__(self, id):
        self.id = id
        self.players = []

    def add_player(self, player):
        if len(self.players) < 4:
            self.players.append(player)
            return True
        else:
            return False