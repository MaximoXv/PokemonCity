import pygame

from image_button import ImageButton
from farm import Farm
from habitat import Habitat
from nidal import Nidal
from sprite import Sprite


class MenuBuild:

    def __init__(self, on_build):

        self.visible = False
        self.selected_plot = None

        self.buttons = [
            # Button( 100, 200, 100, 100, "Farm", lambda: on_build(Farm, self.selected_plot)),
            ImageButton(25, 350,"assets/btn_comprar.png","assets/btn_comprar_hover.png",lambda: on_build(Farm, self.selected_plot),150),
            ImageButton(225, 350,"assets/btn_comprar.png","assets/btn_comprar_hover.png",lambda: on_build(Habitat, self.selected_plot, "fire"),150),
            ImageButton(425, 350,"assets/btn_comprar.png","assets/btn_comprar_hover.png",lambda: on_build(Habitat, self.selected_plot, "water"),150),
            ImageButton(625, 350,"assets/btn_comprar.png","assets/btn_comprar_hover.png",lambda: on_build(Habitat, self.selected_plot, "nature"),150),
            ImageButton(825, 350,"assets/btn_comprar.png","assets/btn_comprar_hover.png",lambda: on_build(Nidal, self.selected_plot),150),
            ImageButton(925, 25,"assets/x.png","assets/x_hover.png",self.close,50),
        ]

        self.images = [
            Sprite(25,200, "assets/farm.png",150),
            Sprite(225,200, "assets/fire_habitat.png",150),
            Sprite(425,200, "assets/water_habitat.png",150),
            Sprite(625,150, "assets/nature_habitat.png",150),
            Sprite(825,200, "assets/nidal.png",150),
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

        for image in self.images:
            image.draw(screen)