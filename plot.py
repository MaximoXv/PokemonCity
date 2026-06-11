import pygame


class Plot:

    def __init__(self, x, y):

        self.rect = pygame.Rect(x, y, 150, 150)

        self.building = None