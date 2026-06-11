import pygame

from farm import Farm
from habitat import Habitat
from menu_build import MenuBuild
from menu_farm import MenuFarm
from menu_nidal import MenuNidal
from nidal import Nidal
from plot import Plot


class World:

    def __init__(self):

        self.food = 0
        self.gold = 15000

        self.selected_pokemon = None

        self.plots = [
            Plot(100, 400),
            Plot(300, 400),
            Plot(500, 400),
            Plot(100, 200),
            Plot(300, 200),
            Plot(500, 200),
        ]



        self.menu_build = MenuBuild(self.build)
        self.menu_farm = MenuFarm(self)
        self.menu_nidal = MenuNidal(self)

    def handle_click(self, mx, my):

        if self.menu_build.handle_click(mx, my):
            return
        
        if self.menu_farm.handle_click(mx, my):
            return
        
        if self.menu_nidal.handle_click(mx, my):
            return

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
                        self.menu_farm.open(building)
                        return


                    elif building.state == "ready":

                        gained = building.collect()

                        self.food += gained

                        print(
                            f"Food: {self.food}"
                        )

                if isinstance(building,Nidal):
                    if building.state == "idle":
                        self.menu_nidal.open(building)
                        return
                    
                    elif building.state == "ready":
                        if self.selected_pokemon:
                            return
                        
                        pokemon = building.collect()
                        self.selected_pokemon = pokemon

                if isinstance(building, Habitat):
                    if self.selected_pokemon:
                        success = building.add_pokemon(self.selected_pokemon)

                        if(success):
                            self.selected_pokemon = None
                            print("pokemon en habitat")

                        return
                    
                    if building.state == "idle":
                        # Aca abriría el menú
                        # self.menu_habitat.open(building)
                        return

                    if building.state == "ready":
                        gold = building.collect()
                        self.gold += gold
                        
                        print(
                            f"Gold: {self.gold}"
                        )
                    


    def build(self, building_class, plot, habitat_type=None):

        if habitat_type:
            plot.building = building_class(habitat_type)
        else:
            plot.building = building_class()

        self.menu_build.close()

    def draw_hud(self, screen):

        font = pygame.font.SysFont("Arial", 24)

        gold_text = font.render(f"Gold: {self.gold}", True, (255, 255, 255))
        food_text = font.render(f"Food: {self.food}", True, (255, 255, 255))

        screen.blit(gold_text, (20, 20))
        screen.blit(food_text, (20, 50))

        if self.selected_pokemon:

            pokemon_text = font.render(
                f"Selected: {self.selected_pokemon.name}",
                True,
                (255, 255, 0)
            )

            screen.blit(pokemon_text, (20, 80))

    def update(self, dt):

        for plot in self.plots:

            if plot.building:
                plot.building.update(dt)

    def draw(self, screen):

        for plot in self.plots:

            if plot.building:

                plot.building.draw(
                    screen,
                    plot.rect
                )
            else:

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

        self.menu_build.draw(screen)
        self.menu_farm.draw(screen)
        self.menu_nidal.draw(screen)
        self.draw_hud(screen)