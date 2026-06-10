import pygame


class Plot:

    def __init__(self, x, y):

        self.rect = pygame.Rect(x, y, 100, 100)

        self.building = None