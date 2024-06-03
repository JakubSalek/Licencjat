import SETTINGS as S

class Card:
    def __init__(self, splitted):
        self.card_type = splitted[0]
        self.name = splitted[1]
        self.description = splitted[2]

        self.player_count = 0
        self.amount_taken = 0
        self.amount_received = 0
        self.count = 0

        if self.card_type == "ATTACK":
            self.player_count = splitted[3]
            self.amount_taken = splitted[4]
            self.amount_received = splitted[5]
        elif self.card_type == "GAIN":
            self.count = splitted[3]
        elif self.card_type == "MOVE":
            self.count = splitted[3]

    def clear_card(self):
        self.card_type = "NONE"
        self.name = "Error"
        self.description = "Something went wrong :/"
        self.player_count = 0
        self.amount_taken = 0
        self.amount_received = 0
        self.count = 0
