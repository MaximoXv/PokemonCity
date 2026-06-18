import pygame
from utils import resource_path


class Pokemon:

    HATCHING = "hatching"
    IDLE = "idle"
    DEAD = "dead"
    EVOLVING = "evolving"

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

        self.evolving = False
        self.evolution_timer = 0
        self.evolution_duration = 18.0
        self.next_form = None

        self.evo_state = "none"  

        self.evo_sound1_played = False
        self.evo_sound2_played = False
        self.evo_success_playing = False

        self.facing = "front"

        self.load_sprites()

    def load_sprites(self):

        sprite_name = self.name.lower()

        self.sprites = {
            "front": pygame.image.load(
                resource_path(f"assets/pokemon/{sprite_name}_front.png")
            ).convert_alpha(),

            "back": pygame.image.load(
                resource_path(f"assets/pokemon/{sprite_name}_back.png")
            ).convert_alpha(),
        }

    def get_sprite(self):

        return self.sprites.get(self.facing, self.sprites["front"])

    def evolve(self):

        if self.evolving:
            return

        next_name = None

        if self.name == "Torchic" and self.level >= 10:
            next_name = "Combusken"

        elif self.name == "Combusken" and self.level >= 30:
            next_name = "Blaziken"

        elif self.name == "Mudkip" and self.level >= 10:
            next_name = "Marshtomp"

        elif self.name == "Marshtomp" and self.level >= 30:
            next_name = "Swampert"

        elif self.name == "Treecko" and self.level >= 10:
            next_name = "Grovyle"

        elif self.name == "Grovyle" and self.level >= 30:
            next_name = "Sceptile"

        if next_name:

            self.evolving = True
            self.state = Pokemon.EVOLVING

            self.evolution_timer = self.evolution_duration
            self.next_form = next_name

            try:
                pygame.mixer.music.load("assets/pokemon/evolve_music.mp3")
                pygame.mixer.music.play(-1)

                self.evo_state = "music"
                self.evo_sound1_played = False
                self.evo_sound2_played = False
                self.evo_success_playing = False
            except:
                pass

    def is_locked(self):
        return self.state == Pokemon.EVOLVING

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

            self.evolve()

    def update(self, dt):

        print(self.state, self.name, self.next_form)

        if self.state == Pokemon.HATCHING:
            self.hatch_timer -= dt
            if self.hatch_timer <= 0:
                self.state = Pokemon.IDLE

        if self.state == Pokemon.EVOLVING:

            self.evolution_timer -= dt

            if self.evo_state == "music" and self.evolution_timer <= 2.0 and not self.evo_sound1_played:
            
                self.evo_sound1_played = True

                self.sound1 = pygame.mixer.Sound("assets/pokemon/evo_sound_1.mp3")
                self.sound1.play()

            if self.evo_sound1_played and not self.evo_sound2_played:
            
                if not pygame.mixer.get_busy():
                    self.evo_sound2_played = True

                    self.sound2 = pygame.mixer.Sound("assets/pokemon/evo_sound_2.mp3")
                    self.sound2.play()

                    self.name = self.next_form
                    self.load_sprites()

            if self.evolution_timer <= 0 and self.evo_state != "success":
            
                pygame.mixer.music.fadeout(800)

                self.evo_state = "success"

                self.success_music = pygame.mixer.Sound("assets/pokemon/evolve_success.mp3")
                self.success_music.play()

                self.success_timer = 4.0

            if self.evo_state == "success":
            
                self.success_timer -= dt

                if self.success_timer <= 0:
                
                    self.state = Pokemon.IDLE
                    self.evolving = False
                    self.next_form = None

                    pygame.mixer.music.stop()

    def draw(self, screen, rect):

        image = self.get_sprite()
    
        if self.state == Pokemon.EVOLVING and self.evo_state != "success":
        
            # no retornar vacío nunca
            screen_image = image
    
            # flash
            if int(self.evolution_timer * 10) % 2 == 0:
                screen_image = pygame.Surface(rect.size, pygame.SRCALPHA)
                screen.blit(screen_image, rect.topleft)
                return
    
            # zoom
            scale = 1.0 + (self.evolution_timer / self.evolution_duration) * 0.5
    
            size = (
                int(rect.width * scale),
                int(rect.height * scale)
            )
    
            screen_image = pygame.transform.smoothscale(image, size)
    
            pos = (
                rect.centerx - size[0] // 2,
                rect.centery - size[1] // 2
            )
    
            screen.blit(screen_image, pos)
            return
    
        # normal
        image = pygame.transform.smoothscale(image, rect.size)
        screen.blit(image, rect.topleft)