import pygame

from utils import resource_path
from world import World


class PokemonCity:

    def __init__(self):

        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Pokemon City")

        self.background = pygame.image.load(resource_path("assets/background.png")).convert()
        self.background = pygame.transform.scale(
            self.background,
            self.screen.get_size()
        )

        self.world = World()

        self.clock = pygame.time.Clock()

        self.running = True

    def run_game(self):

        while self.running:

            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:

                    mx, my = pygame.mouse.get_pos()

                    self.world.handle_click(mx, my)

            self.world.update(dt)

            self.screen.blit(self.background, (0,0))

            self.world.draw(self.screen)

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":

    game = PokemonCity()

    game.run_game()
    