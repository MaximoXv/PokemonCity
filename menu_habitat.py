import pygame

from image_button import ImageButton


class MenuHabitat:

    def __init__(self, world):

        self.world = world

        self.visible = False

        self.selected_habitat = None

        self.feed_buttons = []

        self.close_button = ImageButton(
            925,
            25,
            "assets/x.png",
            "assets/x_hover.png",
            self.close,
            50
        )

    def open(self, habitat):

        self.visible = True

        self.selected_habitat = habitat

        self.feed_buttons.clear()

        for i, pokemon in enumerate(habitat.pokemons[:9]):

            x = 50 + (i % 3) * 300
            y = 170 + (i // 3) * 150

            self.feed_buttons.append(
                ImageButton(
                    x,
                    y,
                    "assets/btn_alimentar.png",
                    "assets/btn_alimentar_hover.png",
                    lambda p=pokemon: self.open_feed_menu(p),
                    120
                )
            )

    def close(self):

        self.visible = False
    
        self.selected_habitat = None
    
        self.feed_buttons.clear()

    def open_feed_menu(self, pokemon):
        self.close()

        self.world.menu_feed.open(pokemon)

    def handle_click(self, mx, my):

        if not self.visible:
            return False

        if self.close_button.handle_click(mx, my):
            return True

        for button in self.feed_buttons:

            if button.handle_click(mx, my):
                return True

        return False
    
    def draw(self, screen):

        if not self.visible:
            return
    
        pygame.draw.rect(
            screen,
            (100, 200, 150),
            screen.get_rect()
        )
    
        for i, pokemon in enumerate(
            self.selected_habitat.pokemons[:9]
        ):
    
            x = 50 + (i % 3) * 300
            y = 40 + (i // 3) * 150
    
            pokemon_rect = pygame.Rect(
                x,
                y,
                100,
                100
            )
    
            pokemon.draw(
                screen,
                pokemon_rect
            )
    
        for button in self.feed_buttons:
            button.draw(screen)
    
        self.close_button.draw(screen)