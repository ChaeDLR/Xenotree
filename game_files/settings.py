import pygame
import os
import json


class Settings:
    """ organize our game settings """

    settings_path = f"{os.getcwd()}/Settings_data"

    def __init__(self):
        """ initialize our game settings """
        self.screen_width = 800
        self.screen_height = 600

        self.screen_mid_x = self.screen_width / 2
        self.screen_mid_y = self.screen_height / 2

        self.direction_list = [1, -1]

        self.bg_color = (113, 143, 30)

        self.screen_rows = self.screen_height / 12

        self.player_life_limit = 3

        if not os.path.isdir(self.settings_path):
            os.mkdir(self.settings_path)

        self.__load_keybind_settings()

    def __load_keybind_settings(self):
        try:
            self.key_bindings: dict = self.load_setting("keybinds.json")
        except:
            self.key_bindings: dict = {
                "move_left": pygame.K_a,
                "move_right": pygame.K_d,
                "jump": pygame.K_SPACE,
                "dash": pygame.K_LSHIFT,
                "cycle_fireball": pygame.K_r,
            }

    @classmethod
    def load_setting(self, file: str) -> dict:
        try:
            with open(f"{self.settings_path}/{file}", "r") as data_file:
                setting_data = json.load(data_file)
            data_file.close()
            return setting_data
        except:
            raise

    @classmethod
    def save_setting(self, settings_data: dict, file: str):
        """
        Save the current keybinds to json
        """
        with open(f"{self.settings_path}/{file}", "w") as data_file:
            json.dump(settings_data, data_file, indent=4)
        data_file.close()

    def set_resolution(self, x_y: tuple):
        """ change screen dimensions """

        self.screen_width = x_y[0]
        self.screen_height = x_y[1]
