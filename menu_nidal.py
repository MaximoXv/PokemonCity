import pygame

from image_button import ImageButton
from sprite import Sprite
from text_box import TextBox


class MenuNidal:

    def __init__(self, world, db):

        self.world = world
        self.db = db

        self.visible = False
        self.selected_nidal = None

        self.buttons = [
            ImageButton(100, 300, "assets/btn_comprar.png", "assets/btn_comprar_hover.png", self.buy_fire, 150),
            ImageButton(300, 300, "assets/btn_comprar.png", "assets/btn_comprar_hover.png", self.buy_water, 150),
            ImageButton(500, 300, "assets/btn_comprar.png", "assets/btn_comprar_hover.png", self.buy_nature, 150),
            ImageButton(925, 25, "assets/x.png", "assets/x_hover.png", self.close, 50),
        ]

        self.images = [
            Sprite(100, 150, "assets/fire_egg.png", 150),
            Sprite(300, 150, "assets/water_egg.png", 150),
            Sprite(500, 150, "assets/nature_egg.png", 150),
        ]

        self.prices = [
            TextBox(100, 275, 150, 25, "$1000"),
            TextBox(300, 275, 150, 25, "$2000"),
            TextBox(500, 275, 150, 25, "$3000"),
        ]

    def open(self, nidal):

        self.visible = True
        self.selected_nidal = nidal

    def close(self):

        self.visible = False
        self.selected_nidal = None

    def try_buy(self, egg_type, cost, duration):

        if self.selected_nidal is None:
            return

        if self.world.gold < cost:
            print("No hay oro")
            return

        self.world.gold -= cost

        self.selected_nidal.buy_egg(
            egg_type,
            duration
        )

        self.close()

    def buy_fire(self):
        self.try_buy("fire", 1000, 20)

    def buy_water(self):
        self.try_buy("water", 2000, 25)

    def buy_nature(self):
        self.try_buy("nature", 3000, 30)

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

        for price in self.prices:
            price.draw(screen)

        for button in self.buttons:
            button.draw(screen)