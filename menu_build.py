import pygame

from button import Button
from farm import Farm


class MenuBuild:

    def __init__(self, on_build):

        self.visible = False
        self.selected_plot = None

        self.buttons = [
            Button(
                100, 200, 100, 100,
                "Farm",
                lambda: on_build(Farm, self.selected_plot)
            )
        ]

    def open(self, plot):

        self.visible = True
        self.selected_plot = plot

    def close(self):

        self.visible = False
        self.selected_plot = None

    def handle_click(self, mx, my):

        if not self.visible:
            return False

        for button in self.buttons:

            if button.handle_click(mx, my):
                return True

        return False

    def draw(self, screen):

        if not self.visible:
            return

        pygame.draw.rect(
            screen,
            (70, 40, 140),
            screen.get_rect()
        )

        for button in self.buttons:
            button.draw(screen)