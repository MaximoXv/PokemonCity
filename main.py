import pygame

from world import World


class PokemonCity:

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Pokemon City")

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

            self.screen.fill((30, 30, 30))

            self.world.draw(self.screen)

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":

    game = PokemonCity()

    game.run_game()