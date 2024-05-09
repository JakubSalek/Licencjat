class Table:
    def __init__(self, id, owner):
        self.id = id
        self.name = f"{owner.nickname}'s table"
        self.players = [owner]
        self.is_started = False