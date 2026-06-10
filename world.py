import pygame

from menu_build import MenuBuild
from plot import Plot
from farm import Farm


class World:

    def __init__(self):

        self.food = 0
        
        self.selected_plot = None

        self.plots = [

            Plot(100, 100),
            Plot(250, 100),
            Plot(400, 100)

        ]

        self.menu_build = MenuBuild(self.build)

    def handle_click(self, mx, my):

        if self.menu_build.handle_click(mx, my):
            return

        for plot in self.plots:

            if not plot.rect.collidepoint(mx, my):
                continue

            if plot.building is None:
                self.selected_plot = plot

                self.menu_build.open()

                return

            # # parcela vacía, le asigno una(cambiar)
            # if plot.building is None:

            #     plot.building = Farm()
            #     self.menu_build_is_active = True
            #     return

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

    def build(self, building_class):
        if self.selected_plot is None:
            return

        self.selected_plot.building = building_class()
        self.menu_build.close()
        self.selected_plot = None

    def update(self, dt):

        for plot in self.plots:

            if plot.building:

                plot.building.update(dt)

    def draw(self, screen):

        for plot in self.plots:

            # parcela vacía
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
            if self.menu_build.visible:
                self.menu_build.draw(screen)