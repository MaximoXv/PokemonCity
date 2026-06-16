import pygame

from utils import resource_path


class Sprite:

    def __init__(self,x,y,image_path,width=None,height=None):

        self.image = pygame.image.load(
            resource_path(image_path)
        ).convert_alpha()

        original_width = self.image.get_width()
        original_height = self.image.get_height()

        # mantener proporción si solo uno está definido
        if width and not height:

            ratio = width / original_width
            height = int(original_height * ratio)

        elif height and not width:

            ratio = height / original_height
            width = int(original_width * ratio)

        elif not width and not height:

            width = original_width
            height = original_height

        self.image = pygame.transform.smoothscale(
            self.image,
            (width, height)
        )

        self.rect = self.image.get_rect(
            topleft=(x, y)
        )

    def draw(self, screen):

        screen.blit(
            self.image,
            self.rect
        )
