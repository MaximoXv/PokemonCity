import pygame

from button import Button
from farm import Farm


class MenuBuild:
    def __init__(self, on_build):

        self.visible = False

        self.buttons = [
            Button(100,200,100,100,"comprar 1",lambda: on_build(Farm)),
            Button(250,200,100,100,"comprar 2",lambda: on_build(Farm)),
            Button(400,200,100,100,"comprar 3",lambda: on_build(Farm)),
            Button(550,200,100,100,"comprar 4",lambda: on_build(Farm)),
        ]

    def open(self):
        self.visible = True

    def close(self):
        self.visible = False

    def handle_click(self, mx, my):

        if not self.visible:
            return False

        for button in self.buttons:
            if button.handle_click(mx,my):
                return True
            
        return False

    def draw(self,screen):

        if not self.visible:
            return

        pygame.draw.rect(
            screen,
            (70, 40, 140),
            screen.get_rect()
        )
        for button in self.buttons:
            button.draw(screen)