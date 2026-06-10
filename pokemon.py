import pygame


class Pokemon:

    def __init__(self):

        self.level = 1

        self.food_eaten = 0

    def feed(self):

        self.food_eaten += 1

        if self.food_eaten >= 3:

            self.level += 1

            self.food_eaten = 0

    def draw(self, screen):

        pygame.draw.rect(
            screen,
            (100, 100, 100),
            (300, 100, 100, 100)
        )