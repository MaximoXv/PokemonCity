import pygame

from farm import Farm
from habitat import Habitat
from menu_build import MenuBuild
from menu_farm import MenuFarm
from menu_feed import MenuFeed
from menu_habitat import MenuHabitat
from menu_nidal import MenuNidal
from nidal import Nidal
from plot import Plot
from sprite import Sprite
from text_box import TextBox


class World:

    def __init__(self):

        self.food = 0
        self.gold = 1500000

        self.selected_pokemon = None

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
            Plot(575, 75),
            Plot(575, 250),
            Plot(575, 425),
            Plot(750, 75),
            Plot(750, 250),
            Plot(750, 425),

        ]



        self.menu_build = MenuBuild(self.build)
        self.menu_farm = MenuFarm(self)
        self.menu_nidal = MenuNidal(self)
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

                    if building.state == "idle" and self.selected_pokemon != None:
                        building.get_back(self.selected_pokemon)
                        self.selected_pokemon = None
                        return

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
                    

                    if building.state == "ready":
                        gold = building.collect()
                        self.gold += gold
                        
                        print(
                            f"Gold: {self.gold}"
                        )
                        return

                    if building.state == "idle":
                        # Aca abriría el menú
                        self.menu_habitat.open(building)
                        return


    def build(self, building_class, plot, habitat_type=None):

        if habitat_type:
            plot.building = building_class(habitat_type)
        else:
            plot.building = building_class()

        self.menu_build.close()

    def draw_hud(self, screen):

        text_gold = TextBox(50,0,100,50,f"{self.gold}")

        text_food = TextBox(325,0,100,50,f"{self.food}")

        text_gold.draw(screen)
        text_food.draw(screen)
        Sprite(0,0, "assets/gold.png",50).draw(screen),
        Sprite(275,0, "assets/berry2.png",50).draw(screen),


        if self.selected_pokemon:

            rect = pygame.Rect(700, -25, 100, 100)
            pokemon_text = TextBox(500,0,225,50,
                f"Seleccionado: {self.selected_pokemon.name}",
            )
            pokemon_text.draw(screen)
            self.selected_pokemon.draw(screen,rect)


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
                    (255, 255, 255),
                    plot.rect,
                    2
                )

        self.menu_build.draw(screen)
        self.menu_farm.draw(screen)
        self.menu_nidal.draw(screen)
        self.menu_habitat.draw(screen)
        self.menu_feed.draw(screen)
        self.draw_hud(screen)