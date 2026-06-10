import pygame

from farm import Farm
from menu_build import MenuBuild
from plot import Plot


class World:

    def __init__(self):

        self.food = 0

        self.plots = [
            Plot(100, 100),
            Plot(250, 100),
            Plot(400, 100)
        ]

        self.menu_build = MenuBuild(self.build)

    def handle_click(self, mx, my):

        # UI primero
        if self.menu_build.handle_click(mx, my):
            return

        # Mundo
        for plot in self.plots:

            if plot.rect.collidepoint(mx, my):

                if plot.building is None:
                    self.menu_build.open(plot)

                    return
            
                building = plot.building



                # si el plot al que se le hizo click es una granja
                if isinstance(building, Farm):

                    if building.state == "idle":
                        # Aca abriría el menú

                        building.plant(
                            amount=100,
                            duration=10
                        )

                    elif building.state == "ready":

                        gained = building.collect()

                        self.food += gained

                        print(
                            f"Food: {self.food}"
                        )

    def build(self, building_class, plot):

        plot.building = building_class()

        self.menu_build.close()

    def update(self, dt):

        for plot in self.plots:

            if plot.building:
                plot.building.update(dt)

    def draw(self, screen):

        for plot in self.plots:

            pygame.draw.rect(
                screen,
                (60, 60, 60),
                plot.rect
            )

            pygame.draw.rect(
                screen,
                (255, 255, 255),
                plot.rect,
                2
            )

            if plot.building:

                plot.building.draw(
                    screen,
                    plot.rect
                )

        self.menu_build.draw(screen)