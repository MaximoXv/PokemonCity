import pygame
from utils import resource_path


class Pokemon:

    HATCHING = "hatching"
    IDLE = "idle"
    DEAD = "dead"
    EVOLVING = "evolving"

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

        # Evolución
        self.evolving = False

        self.evolution_timer = 0
        self.evolution_duration = 18.0

        self.next_species = None

        self.evo_state = "none"

        self.evo_sound1_played = False
        self.evo_sound2_played = False
        self.evo_success_playing = False

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

        image = self.get_sprite(mode)

        if (
            self.state == Pokemon.EVOLVING
            and self.evo_state != "success"
        ):

            screen_image = image

            if int(self.evolution_timer * 10) % 2 == 0:

                screen_image = pygame.Surface(
                    rect.size,
                    pygame.SRCALPHA
                )

                screen.blit(
                    screen_image,
                    rect.topleft
                )

                return

            scale = (
                1.0 +
                (
                    self.evolution_timer
                    / self.evolution_duration
                ) * 0.5
            )

            size = (
                int(rect.width * scale),
                int(rect.height * scale)
            )

            screen_image = pygame.transform.smoothscale(
                image,
                size
            )

            pos = (
                rect.centerx - size[0] // 2,
                rect.centery - size[1] // 2
            )

            screen.blit(
                screen_image,
                pos
            )

            return

        image = pygame.transform.smoothscale(
            image,
            rect.size
        )

        screen.blit(
            image,
            rect.topleft
        )

    def get_name(self):
        return self.species.name

    def get_type(self):
        return self.species.type

    def get_attacks(self):

        attacks = []

        for atk in self.species.attacks:

            if self.level >= atk["level"]:

                attacks.append(
                    self.db.get_attack(
                        atk["attack"]
                    )
                )

        return attacks

    def evolve(self):

        if self.evolving:
            return

        evo = self.species.evolution

        if evo is None:
            return

        if self.level < evo["level"]:
            return

        self.evolving = True
        self.state = Pokemon.EVOLVING

        self.evolution_timer = self.evolution_duration

        self.next_species = self.db.get_species(
            evo["species"]
        )

        try:

            pygame.mixer.music.load(
                resource_path(
                    "assets/pokemon/evolve_music.mp3"
                )
            )

            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play(-1)

            self.evo_state = "music"

            self.evo_sound1_played = False
            self.evo_sound2_played = False
            self.evo_success_playing = False

        except:
            pass

    def finish_evolution(self):

        self.species = self.next_species

        self.load_sprites()

        self.max_hp = self.species.base_hp

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def is_locked(self):

        return self.state == Pokemon.EVOLVING

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

        if self.state == Pokemon.EVOLVING:

            self.evolution_timer -= dt

            if (
                self.evo_state == "music"
                and self.evolution_timer <= 2.0
                and not self.evo_sound1_played
            ):

                self.evo_sound1_played = True

                self.sound1 = pygame.mixer.Sound(
                    resource_path(
                        "assets/pokemon/evo_sound_1.mp3"
                    )
                )

                self.sound1.play()

            if (
                self.evo_sound1_played
                and not self.evo_sound2_played
            ):

                if not pygame.mixer.get_busy():

                    self.evo_sound2_played = True

                    self.sound2 = pygame.mixer.Sound(
                        resource_path(
                            "assets/pokemon/evo_sound_2.mp3"
                        )
                    )

                    self.sound2.play()

                    self.finish_evolution()

            if (
                self.evolution_timer <= 0
                and self.evo_state != "success"
            ):

                pygame.mixer.music.fadeout(800)

                self.evo_state = "success"

                self.success_music = pygame.mixer.Sound(
                    resource_path(
                        "assets/pokemon/evolve_success.mp3"
                    )
                )

                self.success_music.play()

                self.success_timer = 4.0

            if self.evo_state == "success":

                self.success_timer -= dt

                if self.success_timer <= 0:

                    self.state = Pokemon.IDLE

                    self.evolving = False

                    self.next_species = None

                    pygame.mixer.music.stop()