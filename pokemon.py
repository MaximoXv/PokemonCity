import pygame


class Pokemon:

    HATCHING = "hatching"
    IDLE = "idle"
    DEAD = "dead"

    def __init__(self, name, pokemon_type):

        self.name = name
        self.type = pokemon_type

        self.level = 1

        self.max_hp = 100
        self.hp = self.max_hp

        self.food = 0

        self.state = Pokemon.HATCHING

        self.hatch_timer = 30

        self.habitat = None

        sprite_name = name.lower()

        self.sprites = {
            "base": pygame.image.load(
                f"assets/{sprite_name}_1.png"
            ).convert_alpha(),

            "evo1": pygame.image.load(
                f"assets/{sprite_name}_2.png"
            ).convert_alpha(),

            "evo2": pygame.image.load(
                f"assets/{sprite_name}_3.png"
            ).convert_alpha(),
        }

    def food_required(self):

        if self.level > 3:
            return 10 ** 4
        return 10 ** self.level

    def feed(self, amount):

        if self.state == Pokemon.DEAD:
            return

        self.food += amount

        while self.food >= self.food_required():

            self.food -= self.food_required()

            self.level += 1

    def take_damage(self, damage):

        if self.state == Pokemon.DEAD:
            return

        self.hp -= damage

        if self.hp <= 0:

            self.hp = 0

            self.state = Pokemon.DEAD

            if self.habitat:
                self.habitat.remove_pokemon(self)

    def heal(self, amount):

        if self.state == Pokemon.DEAD:
            return

        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def update(self, dt):

        if self.state == Pokemon.HATCHING:

            self.hatch_timer -= dt

            if self.hatch_timer <= 0:

                self.state = Pokemon.IDLE

    def get_sprite(self):

        if self.level >= 30:
            return self.sprites["evo2"]

        if self.level >= 10:
            return self.sprites["evo1"]

        return self.sprites["base"]

    def draw(self, screen, rect):

        image = pygame.transform.smoothscale(
            self.get_sprite(),
            rect.size
        )

        screen.blit(
            image,
            rect.topleft
        )