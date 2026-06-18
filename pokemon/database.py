import json
import random

from pokemon.attack import Attack
from pokemon.species import Species



class Database:

    def __init__(self):
        self.pokemon_data = {}
        self.attack_data = {}
        self.egg_data = {}

    def load(self):

        self.pokemon_data = self._load_file("data/pokemon.json")
        self.attack_data = self._load_file("data/attacks.json")
        self.egg_data = self._load_file("data/eggs.json")

    def _load_file(self, path):

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_species(self, name):

        data = self.pokemon_data[name]
        return Species(name, data)

    def get_attack(self, name):

        data = self.attack_data[name]

        return Attack(
            name,
            data["label"],
            data["damage"],
            data["type"]
        )

    def get_random_from_egg(self, egg_type):

        pool = self.egg_data[egg_type]

        roll = random.uniform(0, 100)
        acc = 0

        for item in pool:

            acc += item["chance"]

            if roll <= acc:
                return item["pokemon"]

        return pool[0]["pokemon"]