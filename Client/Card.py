class Card:
    def __init__(self, splitted):
        self.__type = splitted[0]
        self.__name = splitted[1]
        self.__description = splitted[2]

        self.__player_count = 0
        self.__amount_taken = 0
        self.__amount_received = 0
        self.__material_count = 0
        self.__attack_material = ""

        if self.__type == "ATTACK":
            self.__player_count = int(splitted[3])
            self.__amount_taken = splitted[4]
            self.__amount_received = splitted[5]
            self.__attack_material = splitted[6]
        elif self.__type == "GAIN":
            self.__material_count = splitted[3]
        elif self.__type == "MOVE":
            self.__material_count = splitted[3]

    def clear_card(self):
        self.__type = "NONE"
        self.__name = "Error"
        self.__description = "Something went wrong :/"
        self.__player_count = 0
        self.__amount_taken = 0
        self.__amount_received = 0
        self.__material_count = 0
        self.__attack_material = ""

    def get_type(self):
        return self.__type
    
    def get_name(self):
        return self.__name
    
    def get_description(self):
        return self.__description
    
    def get_player_count(self):
        return self.__player_count
    
    def get_amount_taken(self):
        return self.__amount_taken

    def get_amount_received(self):
        return self.__amount_received
    
    def get_material_count(self):
        return self.__material_count
    
    def get_attack_material(self):
        return self.__attack_material