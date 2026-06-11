import pygame

from button import Button
from image_button import ImageButton
from sprite import Sprite
from nidal import Nidal


class MenuNidal:

    def __init__(self, world):

        self.world = world

        self.visible = False
        self.selected_nidal: Nidal | None = None

        self.buttons = [
            ImageButton(
                100, 300,
                "assets/btn_comprar.png",
                "assets/btn_comprar_hover.png",
                self.buy_fire,
                150
            ),

            ImageButton(
                300, 300,
                "assets/btn_comprar.png",
                "assets/btn_comprar_hover.png",
                self.buy_water,
                150
            ),

            ImageButton(
                500, 300,
                "assets/btn_comprar.png",
                "assets/btn_comprar_hover.png",
                self.buy_nature,
                150
            ),

            Button(1000, 100, 100, 100, "X", self.close),
        ]

        self.images = [
            Sprite(100, 150, "assets/fire_egg.png", 150),
            Sprite(300, 150, "assets/water_egg.png", 150),
            Sprite(500, 150, "assets/nature_egg.png", 150),
        ]


    def open(self, nidal):

        self.visible = True
        self.selected_nidal = nidal

    def close(self):

        self.visible = False
        self.selected_nidal = None

    def _try_buy(self, name, pokemon_type, cost, hatch_time):

        if not self.selected_nidal:
            return

        if self.world.gold < cost:
            print("No hay oro")
            return

        self.world.gold -= cost

        self.selected_nidal.buy_egg(
            name,
            pokemon_type,
            hatch_time
        )

        self.close()

    def buy_fire(self):

        self._try_buy(
            "torchic",
            "fire",
            1000,
            20
        )

    def buy_water(self):

        self._try_buy(
            "mudkip",
            "water",
            1200,
            25
        )

    def buy_nature(self):

        self._try_buy(
            "treecko",
            "nature",
            1500,
            30
        )

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
            (80, 120, 200),
            screen.get_rect()
        )

        for image in self.images:
            image.draw(screen)

        for button in self.buttons:
            button.draw(screen)