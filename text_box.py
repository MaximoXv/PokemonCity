import pygame


class TextBox:

    def __init__(self,x,y,width, height,text):

        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.text = text

        self.font = pygame.font.SysFont(
            None,
            30
        )

    def draw(self, screen):

        pygame.draw.rect(
            screen,
            (80, 80, 80),
            self.rect
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            self.rect,
            2
        )

        text_surface = self.font.render(
            self.text,
            True,
            (255, 255, 255)
        )

        text_rect = text_surface.get_rect(
            center=self.rect.center
        )

        screen.blit(
            text_surface,
            text_rect
        )
