import pygame

from building import Building


class Farm(Building):

    def __init__(self):

        super().__init__(5)

        self.food_amount = 0

        self.production_timer = 0

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

        if self.state == "building":

            color = (100, 100, 100)

        elif self.state == "idle":

            color = (0, 200, 0)

        elif self.state == "growing":

            color = (255, 255, 0)

        elif self.state == "ready":

            color = (0, 255, 255)

        pygame.draw.rect(
            screen,
            color,
            rect
        )