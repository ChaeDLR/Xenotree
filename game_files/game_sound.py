import pygame
import os
import json

# TODO: need music and effect assets


class GameSound:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        # self._load_sound_assets()
        self.music_volume, self.effects_volume = 0.1, 0.3
        # self._read_volume_data()

    def _read_volume_data(self):
        """
        Check if the user has previously saved volume data to load
        """
        directory = f"{os.getcwd()}/Settings_data"
        if os.path.isdir(directory):
            with open(f"{directory}/volume.json", "r") as volume_json_file:
                volume_data = json.load(volume_json_file)
            volume_json_file.close()
            self.set_effects_volume(volume_data["effects_volume"])
            self.set_music_volume(volume_data["music_volume"])
        else:
            self.set_music_volume(self.music_volume)
            self.set_effects_volume(self.effects_volume)

    def save_volumes(self):
        """
        save the current volumes as json data
        """
        directory = f"{os.getcwd()}/Settings_data"
        if not os.path.isdir(directory):
            os.mkdir(directory)

        volumes_json_data = {
            "music_volume": self.music_volume,
            "effects_volume": self.effects_volume,
        }
        with open(f"{directory}/volume.json", "w") as volume_json_file:
            json.dump(volumes_json_data, volume_json_file, indent=4)
        volume_json_file.close()

    def _load_sound_assets(self):
        """ Load sound from assets folder """
        path = os.path.dirname(__file__)
        self.player_movement_sound = pygame.mixer.Sound(
            os.path.join(path, "assets/player_movement_sound.wav")
        )
        self.player_impact_sound = pygame.mixer.Sound(
            os.path.join(path, "assets/player_impact.wav")
        )
        pygame.mixer.music.load(os.path.join(path, "assets/background_music.mp3"))

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
