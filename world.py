import pygame

from farm import Farm
from habitat import Habitat
from nidal import Nidal

from menu_build import MenuBuild
from menu_farm import MenuFarm
from menu_feed import MenuFeed
from menu_habitat import MenuHabitat
from menu_nidal import MenuNidal

from plot import Plot
from sprite import Sprite
from text_box import TextBox

from pokemon.database import Database


class World:

    def __init__(self):

        self.food = 0
        self.gold = 1500000

        self.selected_pokemon = None

        self.db = Database()
        self.db.load()

        self.plots = [
            Plot(50, 75),
            Plot(50, 250),
            Plot(50, 425),
            Plot(225, 75),
            Plot(225, 250),
            Plot(225, 425),
            Plot(400, 75),
            Plot(400, 250),
            Plot(400, 425),
        ]

        self.menu_build = MenuBuild(self.build)
        self.menu_farm = MenuFarm(self)
        self.menu_nidal = MenuNidal(self, self.db)
        self.menu_habitat = MenuHabitat(self)
        self.menu_feed = MenuFeed(self)

    def handle_click(self, mx, my):

        if self.menu_build.handle_click(mx, my):
            return

        if self.menu_farm.handle_click(mx, my):
            return

        if self.menu_nidal.handle_click(mx, my):
            return

        if self.menu_habitat.handle_click(mx, my):
            return

        if self.menu_feed.handle_click(mx, my):
            return

        for plot in self.plots:

            if plot.rect.collidepoint(mx, my):

                if plot.building is None:
                    self.menu_build.open(plot)
                    return

                building = plot.building

                if isinstance(building, Farm):

                    if building.state == "idle":
                        self.menu_farm.open(building)
                        return

                    elif building.state == "ready":
                        self.food += building.collect()
                        return

                if isinstance(building, Nidal):

                    if building.state == "idle" and self.selected_pokemon is not None:
                        building.get_back(self.selected_pokemon)
                        self.selected_pokemon = None
                        return

                    if building.state == "idle":
                        self.menu_nidal.open(building)
                        return

                    elif building.state == "ready":

                        if self.selected_pokemon is not None:
                            return

                        self.selected_pokemon = building.collect()

                if isinstance(building, Habitat):

                    if self.selected_pokemon is not None:

                        ok = building.add_pokemon(self.selected_pokemon)

                        if ok:
                            self.selected_pokemon = None

                        return

                    if building.state == "ready":
                        self.gold += building.collect()
                        return

                    if building.state == "idle":
                        self.menu_habitat.open(building)
                        return

    def build(self, building_class, plot, habitat_type=None):

        if building_class == Nidal:
        
            plot.building = Nidal(self.db)
    
        elif habitat_type is not None:
        
            plot.building = building_class(habitat_type)
    
        else:
        
            plot.building = building_class()
    
        self.menu_build.close()
    
    def draw_hud(self, screen):

        gold_text = TextBox(50, 0, 100, 50, str(self.gold))
        food_text = TextBox(325, 0, 100, 50, str(self.food))

        gold_text.draw(screen)
        food_text.draw(screen)

        Sprite(0, 0, "assets/gold.png", 50).draw(screen)
        Sprite(275, 0, "assets/berry2.png", 50).draw(screen)

        if self.selected_pokemon is not None:

            rect = pygame.Rect(700, -25, 100, 100)

            text = TextBox(
                500, 0, 225, 50,
                "Seleccionado: " + self.selected_pokemon.get_name()
            )

            text.draw(screen)

            self.selected_pokemon.draw(screen, rect)

    def update(self, dt):

        for plot in self.plots:

            if plot.building is not None:
                plot.building.update(dt)

    def draw(self, screen):

        for plot in self.plots:

            if plot.building is not None:
                plot.building.draw(screen, plot.rect)
            else:
                pygame.draw.rect(screen, (255, 255, 255), plot.rect, 2)

        self.menu_build.draw(screen)
        self.menu_farm.draw(screen)
        self.menu_nidal.draw(screen)
        self.menu_habitat.draw(screen)
        self.menu_feed.draw(screen)

        self.draw_hud(screen)