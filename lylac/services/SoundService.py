import pygame


class SoundService:
    _sound_cache: dict[str, pygame.mixer.Sound] = {}

    @staticmethod
    def loadSound(alias: str, path: str):
        SoundService._sound_cache[alias] = pygame.mixer.Sound(path);
        return SoundService._sound_cache[alias];

    @staticmethod
    def playSound(alias: str, volume: float = 1):
        if alias not in SoundService._sound_cache: raise Exception(f"{alias} is not a registered audio track");
        
        sound = SoundService._sound_cache[alias];
        sound.set_volume(volume);
        sound.play();
