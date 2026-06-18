import pygame

class AudioManager:
    def __init__(self):
        self.sounds = {}
        self.music_volume = 0.5
        self.sfx_volume = 0.7

    def load_sound(self, name, path):
        sound = pygame.mixer.Sound(path)
        sound.set_volume(self.sfx_volume)
        self.sounds[name] = sound

    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()

    def stop_sound(self, name):
        if name in self.sounds:
            self.sounds[name].stop()

    def play_music(self, path, loops=-1):
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(loops)

    def stop_music(self):
        pygame.mixer.music.stop()

    def set_sfx_volume(self, volume):
        self.sfx_volume = volume
        for sound in self.sounds.values():
            sound.set_volume(volume)

    def set_music_volume(self, volume):
        self.music_volume = volume
        pygame.mixer.music.set_volume(volume)