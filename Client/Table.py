class Table:
    def __init__(self, id, name, curr_players, started):
        self.id = id
        self.name = name
        self.curr_players = curr_players
        self.players = []
        self.is_started = started