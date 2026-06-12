import pygame

from pokemon import Pokemon
from image_button import ImageButton

class MenuFeed:
    def __init__(self,world):

        self.world = world

        self.visible = False
        self.selected_pokemon: Pokemon | None = None

        self.buttons = [
            ImageButton(150, 450, "assets/alimentar_10.png", "assets/alimentar_10_hover.png", self.feed_10, 250),
            ImageButton(450, 450, "assets/alimentar_100.png", "assets/alimentar_100_hover.png", self.feed_100, 250),
            ImageButton(750, 450, "assets/alimentar_1000.png", "assets/alimentar_1000_hover.png", self.feed_1000, 250),
            ImageButton(300, 600, "assets/alimentar_10000.png", "assets/alimentar_10000_hover.png", self.feed_10000, 250),

            ImageButton(925, 25, "assets/x.png", "assets/x_hover.png", self.close, 50),
        ]

    def open(self, pokemon):

        self.visible = True
        self.selected_pokemon = pokemon

    def close(self):
        self.visible = False

    def _try_feed(self, amount):

        if not self.selected_pokemon:
            return

        if self.world.food < amount:
            print("No hay comida")
            return

        self.world.food -= amount
        self.selected_pokemon.feed(amount)

    def feed_10(self):
        self._try_feed(10)

    def feed_100(self):
        self._try_feed(100)

    def feed_1000(self):
        self._try_feed(1000)

    def feed_10000(self):
        self._try_feed(10000)

    def handle_click(self, mx, my):
        if not self.visible:
            return False
        
        for button in self.buttons:
            if button.handle_click(mx,my):
                return True
            
        return False

    def draw(self, screen):

        if not self.visible:
            return
        
        if not self.selected_pokemon:
            return

        pygame.draw.rect(
            screen,
            (100, 200, 150),
            screen.get_rect()
        )
    
        if self.selected_pokemon:

            pokemon_rect = pygame.Rect(
                400,
                80,
                180,
                180
            )

            self.selected_pokemon.draw(
                screen,
                pokemon_rect
            )

            font = pygame.font.SysFont("Arial", 28)

            level_text = font.render(
                f"Lv {self.selected_pokemon.level}",
                True,
                (255, 255, 0)
            )

            screen.blit(
                level_text,
                (450, 270)
            )

            # NOMBRE (opcional pero útil)
            name_text = font.render(
                self.selected_pokemon.name,
                True,
                (255, 255, 255)
            )

            screen.blit(
                name_text,
                (420, 300)
            )


        for button in self.buttons:
            button.draw(screen)
