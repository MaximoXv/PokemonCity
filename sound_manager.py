import pygame

from utils import resource_path


class SoundManager:

    def __init__(self):

        self.sounds = {
            "click": pygame.mixer.Sound(resource_path("assets/sfx/click.wav")),
            "collect_food": pygame.mixer.Sound(resource_path("assets/sfx/collect_food.mp3")),
            "collect_gold": pygame.mixer.Sound(resource_path("assets/sfx/collect_gold.mp3")),
            "buy": pygame.mixer.Sound(resource_path("assets/sfx/buy.mp3")),
            "error": pygame.mixer.Sound(resource_path("assets/sfx/error.mp3")),
        }

        for sound in self.sounds.values():
            sound.set_volume(1.0)

    def play(self, name):

        sound = self.sounds.get(name)

        if sound:
            sound.play()