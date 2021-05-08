import pygame
import os
from .utils.spritesheet import SpriteSheet

class AssetManager:
    """
    This class will load and store assets the game needs
    """
    fireball_coords = {"idle_purp": [
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

    @classmethod
    def level_one_assets(cls) -> dict:
        """
        Load the level one assets that are created and destroyed 
        durring gameplay and return them in a dict
        """
        # load lasers
        current_path = os.path.dirname(__file__)
        laser_img_path = os.path.join(
            current_path, "sprites/sprite_assets/laser.png"
            )
        laser_img = pygame.image.load(laser_img_path)

        # load fireballs
        fireballs_path = os.path.join(
            current_path, "sprites/sprite_assets/player_assets/fireballs.png"
        )
        ss_tool = SpriteSheet(fireballs_path)
        fireball_ss_coords: dict = cls.fireball_coords
        p_colorkey = (0, 0, 0)

        purp_fb_idle_imgs = ss_tool.images_at(
            fireball_ss_coords["idle_purp"], p_colorkey
            )

        blue_fb_idle_imgs = ss_tool.images_at(
            fireball_ss_coords["idle_blue"], p_colorkey
        )

        red_fb_idle_imgs = ss_tool.images_at(
            fireball_ss_coords["idle_red"], p_colorkey
        )

        purp_fb_fire_imgs = ss_tool.images_at(
            fireball_ss_coords["fire_purp"], p_colorkey
        )

        blue_fb_fire_imgs = ss_tool.images_at(
            fireball_ss_coords["fire_blue"], p_colorkey
        )

        red_fb_fire_imgs = ss_tool.images_at(
            fireball_ss_coords["fire_red"], p_colorkey
        )

        return {
            "laser_img": laser_img,
            "purple_fb_idle_imgs": purp_fb_idle_imgs,
            "blue_fb_idle_imgs": blue_fb_idle_imgs,
            "red_fb_idle_imgs": red_fb_idle_imgs,
            "purple_fb_fire_imgs": purp_fb_fire_imgs,
            "blue_fb_fire_imgs": blue_fb_fire_imgs,
            "red_fb_fire_imgs": red_fb_fire_imgs
        }
        