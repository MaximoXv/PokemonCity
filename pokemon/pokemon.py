import pygame
from utils import resource_path


class Pokemon:

    HATCHING = "hatching"
    IDLE = "idle"
    DEAD = "dead"

    def __init__(self, species, db):

        self.species = species
        self.db = db

        self.level = 1

        self.max_hp = species.base_hp
        self.hp = self.max_hp

        self.food = 0

        self.state = Pokemon.HATCHING

        self.hatch_timer = 30

        self.habitat = None

        self.load_sprites()

    def load_sprites(self):

        self.sprites = {}

        for key in self.species.sprites:

            path = self.species.sprites[key]

            self.sprites[key] = pygame.image.load(
                resource_path(path)
            ).convert_alpha()

    def get_sprite(self, mode):

        if mode in self.sprites:
            return self.sprites[mode]

        return list(self.sprites.values())[0]

    def draw(self, screen, rect, mode="front"):

        img = self.get_sprite(mode)

        img = pygame.transform.smoothscale(img, rect.size)

        screen.blit(img, rect.topleft)

    def get_name(self):
        return self.species.name

    def get_type(self):
        return self.species.type

    def get_attacks(self):

        attacks = []

        for atk in self.species.attacks:

            if self.level >= atk["level"]:

                attacks.append(
                    self.db.get_attack(atk["attack"])
                )

        return attacks

    def evolve(self):

        evo = self.species.evolution

        if evo is None:
            return

        if self.level >= evo["level"]:

            self.species = self.db.get_species(
                evo["species"]
            )

            self.load_sprites()

            self.max_hp = self.species.base_hp

            if self.hp > self.max_hp:
                self.hp = self.max_hp

    def food_required(self):
        if self.level > 3:
            return 10 ** 4
        return 10 ** self.level

    def feed(self, amount):

        self.food += amount

        while self.food >= self.food_required():

            self.food -= self.food_required()
            self.level += 1

            self.evolve()

    def take_damage(self, dmg):

        if self.state == Pokemon.DEAD:
            return

        self.hp -= dmg

        if self.hp <= 0:

            self.hp = 0
            self.state = Pokemon.DEAD

            if self.habitat:
                self.habitat.remove_pokemon(self)

    def update(self, dt):

        if self.state == Pokemon.HATCHING:

            self.hatch_timer -= dt

            if self.hatch_timer <= 0:
                self.state = Pokemon.IDLE