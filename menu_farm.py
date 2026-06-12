import pygame

from farm import Farm
from image_button import ImageButton
from sprite import Sprite

class MenuFarm:
    def __init__(self,world):

        self.world = world

        self.visible = False
        self.selected_farm: Farm | None = None

        self.buttons = [
            ImageButton(25, 300,"assets/btn_cultivar.png","assets/btn_cultivar_hover.png",self.plant_100,200),
            ImageButton(275, 300,"assets/btn_cultivar.png","assets/btn_cultivar_hover.png",self.plant_500,200),
            ImageButton(525, 300,"assets/btn_cultivar.png","assets/btn_cultivar_hover.png",self.plant_2000,200),
            ImageButton(775, 300,"assets/btn_cultivar.png","assets/btn_cultivar_hover.png",self.plant_10000,200),
            ImageButton(925, 25,"assets/x.png","assets/x_hover.png",self.close,50),
        ]

        self.images = [
            Sprite(25,150, "assets/food1.png",200),
            Sprite(275,150, "assets/food2.png",200),
            Sprite(525,150, "assets/food3.png",200),
            Sprite(775,150, "assets/food4.png",200),
        ]

    def open(self, farm):

        self.visible = True
        self.selected_farm = farm

    def close(self):
        self.visible = False

    def _try_plant(self, amount, duration, cost):

        if not self.selected_farm:
            return

        if self.world.gold < cost:
            print("No hay oro")
            return

        self.world.gold -= cost
        self.selected_farm.plant(amount, duration)
        self.close()

    def plant_100(self):
        self._try_plant(100, 5, 1000)

    def plant_500(self):
        self._try_plant(500, 10, 2000)

    def plant_2000(self):
        self._try_plant(2000, 20, 5000)

    def plant_10000(self):
        self._try_plant(10000, 45, 20000)

    def handle_click(self, mx, my):
        if not self.visible:
            return False
        
        for button in self.buttons:
            if button.handle_click(mx,my):
                return True
            
        return False

    def draw(self,screen):
        if not self.visible:
            return
        
        pygame.draw.rect(
            screen,
            (100,200,150),
            screen.get_rect()
        )

        for button in self.buttons:
            button.draw(screen)
        
        for image in self.images:
            image.draw(screen)
