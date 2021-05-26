import pygame
import os
from .utils.spritesheet import SpriteSheet

class AssetManager:
    """
    This class will load and store assets the game needs
    """

    current_path = os.path.dirname(__file__)
    p_colorkey = (0, 0, 0)

    fireball_coords = {
        "idle_purp": [
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
        ]
    }

    player_coords: dict = {
        "idle": [
            # (8, 1, 21, 30), Animation looks a lot smoother without this image
            (40, 0, 21, 30),
            (72, 0, 24, 30),
            (100, 1, 25, 30),
            (133, 2, 24, 30)
        ],
        "walk": [
            (2, 32, 28, 30),
            (35, 33, 28, 30),
            (67, 34, 28, 30),
            (98, 34, 28, 30)
        ],
        "jump": [
            (2, 65, 28, 27),
            (33, 66, 30, 27),
            (65, 66, 30, 26),
            (98, 66, 28, 27)
        ],
    }

    @classmethod
    def enemy_projectile_assets(cls) -> dict:
        """
        load enemy projectile images
        """
        # load lasers
        laser_img_path = os.path.join(
            cls.current_path, "sprites/sprite_assets/laser.png"
            )
        laser_img = pygame.image.load(laser_img_path)

        return {"laser_img": laser_img}

    @classmethod
    def fireball_assets(cls) -> dict:
        """
        Load the level one assets that are created and destroyed 
        durring gameplay and return them in a dict
        """
        # load fireballs
        fireballs_path = os.path.join(
            cls.current_path, "sprites/sprite_assets/player_assets/fireballs.png"
        )

        ss_tool = SpriteSheet(fireballs_path)

        purp_fb_idle_imgs = ss_tool.images_at(
            cls.fireball_coords["idle_purp"], cls.p_colorkey
            )

        blue_fb_idle_imgs = ss_tool.images_at(
            cls.fireball_coords["idle_blue"], cls.p_colorkey
        )

        red_fb_idle_imgs = ss_tool.images_at(
            cls.fireball_coords["idle_red"], cls.p_colorkey
        )

        purp_fb_fire_imgs = ss_tool.images_at(
            cls.fireball_coords["fire_purp"], cls.p_colorkey
        )

        blue_fb_fire_imgs = ss_tool.images_at(
            cls.fireball_coords["fire_blue"], cls.p_colorkey
        )

        red_fb_fire_imgs = ss_tool.images_at(
            cls.fireball_coords["fire_red"], cls.p_colorkey
        )

        fireball_imgs_dict: dict = {
            "purple_fb_idle_imgs": purp_fb_idle_imgs,
            "blue_fb_idle_imgs": blue_fb_idle_imgs,
            "red_fb_idle_imgs": red_fb_idle_imgs,
            "purple_fb_fire_imgs": purp_fb_fire_imgs,
            "blue_fb_fire_imgs": blue_fb_fire_imgs,
            "red_fb_fire_imgs": red_fb_fire_imgs
        }

        # scale up the fireball images
        for key in fireball_imgs_dict:
            fireball_imgs_dict[key] = [pygame.transform.scale(x, (16, 13)) for x in fireball_imgs_dict[key]]
        
        return fireball_imgs_dict

    @classmethod
    def load_player_images(cls) -> None:
        """ Load player image from assets folder """
        player_ss_path = os.path.join(
            cls.current_path, "sprites/sprite_assets/player_assets/MageSpriteSheet.png"
        )
        ss_tool = SpriteSheet(player_ss_path)

        def get_animations(coords_list: list, key: str) -> dict:
            right_images = []
            for coord in coords_list:
                image = ss_tool.image_at(coord, cls.p_colorkey)
                image = pygame.transform.scale(image, (41, 54))
                right_images.append(image)

            left_images = right_images[:]
            for i in range(0, len(right_images)):
                left_images[i] = pygame.transform.flip(
                    left_images[i], True, False
                )
            return {
            f"{key}_right": right_images,
            f"{key}_left": left_images
            }
        
        return {
            **get_animations(cls.player_coords["idle"], "idle"),
            **get_animations(cls.player_coords["walk"], "walk"),
            **get_animations(cls.player_coords["jump"], "jump")
        }

    @classmethod
    def level_one_assets(cls) -> dict:
        """
        Get all of the level one assets in one dict
        """
        fireballs = cls.fireball_assets()
        enemy_projectiles = cls.enemy_projectile_assets()
        return {**fireballs, **enemy_projectiles}

    

        