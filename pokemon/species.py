class Species:

    def __init__(self, name, data):

        self.name = name

        self.type = data["type"]
        self.base_hp = data["base_hp"]

        self.sprites = data["sprites"]

        self.attacks = data["attacks"]

        self.evolution = data.get("evolution", None)