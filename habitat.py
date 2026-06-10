import pygame


class Habitat:

    def __init__(self):

        self.gold_timer = 0

        self.stored_gold = 0

    def collect(self):

        gold = self.stored_gold

        self.stored_gold = 0

        return gold

    def update(self, dt):

        self.gold_timer += dt

        if self.gold_timer >= 1:

            self.gold_timer -= 1

            self.stored_gold += 1

    def draw(self, screen):

        pygame.draw.rect(
            screen,
            (100, 100, 0),
            (200, 100, 100, 100)
        )