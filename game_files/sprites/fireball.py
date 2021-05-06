import os
import pygame
from .projectile_base import Projectile
from ..utils.spritesheet import SpriteSheet

class Fireball(Projectile):
    def __init__(self, start_x_y: tuple, dir_x_y: tuple):
        """
        Create fireball transformed based on direction
        """
        super().__init__()
        self.set_start(start_x_y, dir_x_y)
        self.load_img()

    def change_color(
        self, red: bool=False, blue: bool=False, purple: bool=False
        ) -> None:
        """
        Change what color the fireball should be
        """
        if red:
            self.color = "red"
        elif blue:
            self.color = "blue"
        elif purple:
            self.color = "purple"

    def __fireball_coords(self) -> dict:
        coords = {"idle_purp": [
            (2, 1, 4, 7),
            (26, 3, 3, 5)
        ],
        "idle_blue": [
            (2, 11, 4, 7),
            (26, 13, 3, 5)
        ],
        "idle_red": [
            (2, 21, 4, 7),
            (26, 23, 3, 5)
        ],
        "fire_purp": [
            (8, 4, 7, 4),
            (18, 5, 5, 3)
        ],
        "fire_blue": [
            (8, 14, 7, 4),
            (18, 15, 5, 3)
        ],
        "fire_red": [
            (8, 24, 7, 4),
            (18, 25, 5, 3)
        ]}
        return coords

    def load_img(self):
        """
        Load fireball images from spritesheet
        """
        path = os.path.dirname(__file__)
        fireballs_path = os.path.join(
            path, "sprite_assets/player_assets/fireballs.png"
        )
        ss_tool = SpriteSheet(fireballs_path)
        fireball_ss_coords: dict = self.__fireball_coords()
        p_colorkey = (0, 0, 0)

        self.purp_fb_idle_imgs = ss_tool.images_at(
            fireball_ss_coords["idle_purp"], p_colorkey
            )

        self.blue_fb_idle_imgs = ss_tool.images_at(
            fireball_ss_coords["idle_blue"], p_colorkey
        )

        self.red_fb_idle_imgs = ss_tool.images_at(
            fireball_ss_coords["idle_red"], p_colorkey
        )

        self.purp_fb_fire_imgs = ss_tool.images_at(
            fireball_ss_coords["fire_purp"], p_colorkey
        )

        self.blue_fb_fire_imgs = ss_tool.images_at(
            fireball_ss_coords["fire_blue"], p_colorkey
        )

        self.red_fb_fire_imgs = ss_tool.images_at(
            fireball_ss_coords["fire_red"]
        )
