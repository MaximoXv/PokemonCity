import pygame

from building import Building
from utils import resource_path


class Farm(Building):

    def __init__(self):

        super().__init__(5)

        self.food_amount = 0

        self.production_timer = 0

        self.sprites = {
            "building":  pygame.image.load(resource_path("assets/farm_building.png")).convert_alpha(),
            "idle":  pygame.image.load(resource_path("assets/farm.png")).convert_alpha(),
            "growing":  pygame.image.load(resource_path("assets/farm_growing.png")).convert_alpha(),
            "ready":  pygame.image.load(resource_path("assets/farm_ready.png")).convert_alpha(),
        }

    def plant(self, amount, duration):

        if self.state != "idle":
            return

        self.food_amount = amount

        self.production_timer = duration

        self.state = "growing"

    def collect(self):

        if self.state != "ready":
            return 0

        amount = self.food_amount

        self.food_amount = 0

        self.state = "idle"

        return amount

    def update(self, dt):

        super().update(dt)

        if self.state == "growing":

            self.production_timer -= dt

            if self.production_timer <= 0:

                self.state = "ready"

    def draw(self, screen, rect):

        image = pygame.transform.smoothscale(
            self.sprites[self.state],
            rect.size
        )

        screen.blit(
            image,
            rect.topleft
        )