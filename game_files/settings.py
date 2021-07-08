import pygame
class Settings:
    """ organize our game settings """

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

        self.key_bindings: dict = {
            "move_left": pygame.K_a,
            "move_right": pygame.K_d,
            "jump": pygame.K_SPACE,
            "dash": pygame.K_LSHIFT,
            "cycle_fireball": pygame.K_r
        }

    def set_resolution(self, x_y: tuple):
        """ change screen dimensions """

        self.screen_width = x_y[0]
        self.screen_height = x_y[1]
