import pygame

from utils import resource_path


class ImageButton:

    def __init__(self,x,y,image_path,hover_image_path,callback,width=None,height=None):

        self.callback = callback

        self.normal_image = pygame.image.load(
            resource_path(image_path)
        ).convert_alpha()

        self.hover_image = pygame.image.load(
            resource_path(hover_image_path)
        ).convert_alpha()

        original_width = self.normal_image.get_width()
        original_height = self.normal_image.get_height()

        if width and not height:

            ratio = width / original_width
            height = int(original_height * ratio)

        elif height and not width:

            ratio = height / original_height
            width = int(original_width * ratio)

        elif not width and not height:

            width = original_width
            height = original_height

        self.normal_image = pygame.transform.smoothscale(
            self.normal_image,
            (width, height)
        )

        self.hover_image = pygame.transform.smoothscale(
            self.hover_image,
            (width, height)
        )

        self.rect = self.normal_image.get_rect(
            topleft=(x, y)
        )

    def is_hovered(self):

        mx, my = pygame.mouse.get_pos()

        return self.rect.collidepoint(
            mx,
            my
        )

    def handle_click(self, mx, my):

        if self.rect.collidepoint(mx, my):

            self.callback()

            return True

        return False

    def draw(self, screen):

        if self.is_hovered():

            screen.blit(
                self.hover_image,
                self.rect
            )

        else:

            screen.blit(
                self.normal_image,
                self.rect
            )