import random
import pygame

from utils import resource_path


class MusicManager:

    def __init__(self):

        self.enabled = True

        self.tracks = [
            "assets/pokemon/background_music_1.mp3",
            "assets/pokemon/background_music_2.mp3"
        ]

        self.current_track = None

    def play_random(self):

        choices = self.tracks.copy()

        if self.current_track in choices:
            choices.remove(self.current_track)

        self.current_track = random.choice(choices)

        pygame.mixer.music.load(resource_path(self.current_track))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def update(self):

        if not self.enabled:
            return

        if not pygame.mixer.music.get_busy():
            self.play_random()