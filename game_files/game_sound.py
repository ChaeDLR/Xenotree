import pygame
import os

from .settings import Settings

# TODO: need music and effect assets


class GameSound:
    """manages sound settings"""

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        # self._load_sound_assets()
        self.music_volume, self.effects_volume = 0.1, 0.3
        self.__read_volume_data()

    def __read_volume_data(self):
        """
        Try to load existing volume data
        if it fails load the default settings
        """
        try:
            volume_data = Settings.load_setting("volume.json")
            self.set_effects_volume(volume_data["effects_volume"])
            self.set_music_volume(volume_data["music_volume"])
        except:
            self.set_music_volume(self.music_volume)
            self.set_effects_volume(self.effects_volume)

    def save_volumes(self):
        """
        save the current volumes as json data
        """
        Settings.save_setting(
            {
                "music_volume": self.music_volume,
                "effects_volume": self.effects_volume,
            },
            "volume.json",
        )

    def set_effects_volume(self, effects_volume: float):
        """
        effects_volume: (0.0 - 1.0)
        """
        self.effects_volume = effects_volume
        # self.player_movement_sound.set_volume(effects_volume)
        # self.player_impact_sound.set_volume(effects_volume)

    def set_music_volume(self, music_volume: float):
        """
        music_volume: (0.0 - 1.0)
        """
        self.music_volume = music_volume
        pygame.mixer.music.set_volume(music_volume)
        # pygame.mixer.music.stop()

    def increase_effects_volume(self):
        if self.effects_volume < 0.5:
            self.effects_volume += 0.1
            self.effects_volume = round(self.effects_volume, 2)
            self.set_effects_volume(self.effects_volume)

    def decrease_effects_volume(self):
        if self.effects_volume > 0.0:
            self.effects_volume -= 0.1
            self.effects_volume = round(self.effects_volume, 2)
            self.set_effects_volume(self.effects_volume)

    def increase_music_volume(self):
        if self.music_volume < 0.5:
            self.music_volume += 0.1
            self.music_volume = round(self.music_volume, 2)
            self.set_music_volume(self.music_volume)

    def decrease_music_volume(self):
        if self.music_volume > 0.0:
            self.music_volume -= 0.1
            self.music_volume = round(self.music_volume, 2)
            self.set_music_volume(self.music_volume)
