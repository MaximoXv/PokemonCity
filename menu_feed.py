import pygame

from image_button import ImageButton


class MenuFeed:

    def __init__(self, world):

        self.world = world

        self.visible = False
        self.selected_pokemon = None

        self.buttons = [
            ImageButton(200, 400, "assets/alimentar_10.png", "assets/alimentar_10_hover.png", self.feed_10, 250),
            ImageButton(500, 400, "assets/alimentar_100.png", "assets/alimentar_100_hover.png", self.feed_100, 250),
            ImageButton(200, 500, "assets/alimentar_1000.png", "assets/alimentar_1000_hover.png", self.feed_1000, 250),
            ImageButton(500, 500, "assets/alimentar_10000.png", "assets/alimentar_10000_hover.png", self.feed_10000, 250),

            ImageButton(925, 25, "assets/x.png", "assets/x_hover.png", self.close, 50),
        ]

    def open(self, pokemon):

        self.visible = True
        self.selected_pokemon = pokemon

    def close(self):

        self.visible = False
        self.selected_pokemon = None

    def try_feed(self, amount):

        if self.selected_pokemon is None:
            return

        if self.world.food < amount:
            print("No hay comida")
            return

        self.world.food -= amount
        self.selected_pokemon.feed(amount)

    def feed_10(self):
        self.try_feed(10)

    def feed_100(self):
        self.try_feed(100)

    def feed_1000(self):
        self.try_feed(1000)

    def feed_10000(self):
        self.try_feed(10000)

    def handle_click(self, mx, my):

        if not self.visible:
            return False

        for b in self.buttons:
            if b.handle_click(mx, my):
                return True

        return False

    def draw(self, screen):

        if not self.visible:
            return

        if self.selected_pokemon is None:
            return

        pygame.draw.rect(screen, (100, 200, 150), screen.get_rect())

        pokemon_rect = pygame.Rect(400, 80, 180, 180)

        self.selected_pokemon.draw(screen, pokemon_rect)

        font = pygame.font.SysFont("Arial", 28)

        level_text = font.render(
            "Lv " + str(self.selected_pokemon.level),
            True,
            (255, 255, 0)
        )

        screen.blit(level_text, (400, 300))

        name_text = font.render(
            self.selected_pokemon.get_name(),
            True,
            (255, 255, 255)
        )

        screen.blit(name_text, (500, 300))

        for b in self.buttons:
            b.draw(screen)