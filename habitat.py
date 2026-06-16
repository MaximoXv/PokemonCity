import pygame

from building import Building
from pokemon import Pokemon
from utils import resource_path


class Habitat(Building):

    def __init__(self, habitat_type):

        super().__init__(5)

        self.type = habitat_type

        self.pokemons = []

        self.gold_timer = 0
        self.stored_gold = 0
        self.gold_cap = 10

        self.sprites = {
            "building": pygame.image.load(
                resource_path(f"assets/{habitat_type}_habitat_building.png")
            ).convert_alpha(),

            "idle": pygame.image.load(
                resource_path(f"assets/{habitat_type}_habitat.png")
            ).convert_alpha(),

            "ready": pygame.image.load(
                resource_path(f"assets/{habitat_type}_habitat_ready.png")
            ).convert_alpha(),
        }

    def add_pokemon(self, pokemon):

        if pokemon.state != Pokemon.IDLE:
            return False

        if pokemon.type != self.type:
            return False

        if pokemon.habitat:
            return False

        self.pokemons.append(pokemon)

        pokemon.habitat = self

        return True

    def remove_pokemon(self, pokemon):

        if pokemon in self.pokemons:

            self.pokemons.remove(pokemon)

            pokemon.habitat = None

    def collect(self):

        if self.state != "ready":
            return 0

        gold = self.stored_gold

        self.stored_gold = 0
        self.state = "idle"

        return gold

    def update(self, dt):

        super().update(dt)

        if self.state == "ready":
            return

        self.gold_timer += dt

        if self.gold_timer >= 1:

            self.gold_timer -= 1

            self.stored_gold += len(self.pokemons)

            if self.stored_gold >= self.gold_cap:

                self.stored_gold = self.gold_cap
                self.state = "ready"

    def draw(self, screen, rect):

        image = pygame.transform.smoothscale(
            self.sprites[self.state],
            rect.size
        )

        screen.blit(image, rect.topleft)

        pokemon_size = 40

        for i, pokemon in enumerate(self.pokemons[:6]):

            pokemon_rect = pygame.Rect(
                rect.x + 5 + (i % 3) * 45,
                rect.y + 5 + (i // 3) * 45,
                pokemon_size,
                pokemon_size
            )

            pokemon.draw(
                screen,
                pokemon_rect
            )
