import pygame


class Plot:

    def __init__(self, x, y, width=150, height=150):

        self.rect = pygame.Rect(x, y, width, height)

        self.building = None