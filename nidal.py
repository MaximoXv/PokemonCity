import pygame

from building import Building
from pokemon import Pokemon
from utils import resource_path


class Nidal(Building):

    def __init__(self):

        super().__init__(5)

        self.egg = None
        self.egg_type = None

        self.hatch_timer = 0

        self.sprites = {
            "idle": pygame.image.load(resource_path("assets/nidal.png")).convert_alpha(),
            "building": pygame.image.load(resource_path("assets/nidal_building.png")).convert_alpha(),

            "hatching_fire": pygame.image.load(resource_path("assets/nidal_fire_hatching.png")).convert_alpha(),
            "hatching_water": pygame.image.load(resource_path("assets/nidal_water_hatching.png")).convert_alpha(),
            "hatching_nature": pygame.image.load(resource_path("assets/nidal_nature_hatching.png")).convert_alpha(),

            "ready_fire": pygame.image.load(resource_path("assets/nidal_fire_ready.png")).convert_alpha(),
            "ready_water": pygame.image.load(resource_path("assets/nidal_water_ready.png")).convert_alpha(),
            "ready_nature": pygame.image.load(resource_path("assets/nidal_nature_ready.png")).convert_alpha(),
        }


    def buy_egg(self, name, pokemon_type, duration):

        if self.state != "idle":
            return

        self.egg = Pokemon(name, pokemon_type)

        self.egg.state = "hatching"
        self.egg.hatch_timer = duration

        self.egg_type = pokemon_type

        self.state = "hatching"
        self.hatch_timer = duration

    def collect(self):

        if self.state != "ready":
            return None

        pokemon = self.egg

        pokemon.state = "idle"

        self.egg = None
        self.egg_type = None

        self.state = "idle"
        self.hatch_timer = 0

        return pokemon


    def update(self, dt):

        super().update(dt)

        if self.state == "hatching":

            self.hatch_timer -= dt

            if self.egg:
                self.egg.update(dt)

            if self.hatch_timer <= 0:

                self.state = "ready"

    def draw(self, screen, rect):

        if self.state == "hatching":
            key = f"hatching_{self.egg_type}"

        elif self.state == "ready":
            key = f"ready_{self.egg_type}"

        else:
            key = self.state

        image = self.sprites.get(key, self.sprites["idle"])

        image = pygame.transform.smoothscale(image, rect.size)

        screen.blit(image, rect.topleft)