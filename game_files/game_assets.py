import pygame
import os
from .utils.spritesheet import SpriteSheet


class AssetManager:
    """
    This class will load and store assets the game needs
    """

    current_path = os.path.dirname(__file__)
    p_colorkey = (0, 0, 0)

    fireball_coords: dict = {
        "idle_purp": [(2, 1, 4, 7), (26, 3, 3, 5)],
        "idle_blue": [(2, 11, 4, 7), (26, 13, 3, 5)],
        "idle_red": [(2, 21, 4, 7), (26, 23, 3, 5)],
        "fire_purp": [(8, 4, 7, 4), (18, 5, 5, 3)],
        "fire_blue": [(8, 14, 7, 4), (18, 15, 5, 3)],
        "fire_red": [(8, 24, 7, 4), (18, 25, 5, 3)],
    }

    player_coords: dict = {
        "idle": [
            # (8, 1, 21, 30), Animation looks a lot smoother without this image
            (40, 0, 21, 30),
            (72, 0, 24, 30),
            (100, 1, 25, 30),
            (133, 2, 24, 30),
        ],
        "walk": [(2, 32, 28, 30), (35, 33, 28, 30), (67, 34, 28, 30), (98, 34, 28, 30)],
        "jump": [(2, 65, 28, 27), (33, 66, 30, 27), (65, 66, 30, 26), (98, 66, 28, 27)],
        "hit": [(8, 97, 22, 32), (39, 96, 24, 32)],
        "death": [
            (3, 129, 30, 27),
            (36, 131, 29, 25),
            (66, 137, 31, 22),
            (97, 140, 31, 20),
            (130, 141, 30, 19),
        ],
    }

    @classmethod
    def __get_image(
        self,
        path: str,
        resize: tuple = None,
        colorKey: tuple = (0, 0, 0),
        colorkey_at: tuple = None,
    ) -> pygame.Surface:
        """
        Return an image and a rect from a given path
        resize: tuple -> (width, height)
        colorkey: tuple -> (0, 0, 0)
        colokey_at: tuple -> (x, y)
        """
        image = pygame.image.load(path).convert()
        if resize:
            image = pygame.transform.scale(image, resize)

        img_colorkey = colorKey
        if colorkey_at:
            img_colorkey = image.get_at(colorkey_at)
        image.set_colorkey(img_colorkey, pygame.RLEACCEL)
        return image

    @classmethod
    def background_assets(cls, w_h: tuple) -> dict:
        """
        Load all background images
        w_h: tuple -> (screen_wdith, screen_height)
        """
        background_image_path = os.path.join(
            cls.current_path, "levels/environment/env_assets/background"
        )
        # move background loading from level base to here
        # load background layers
        background_image = cls.__get_image(
            os.path.join(background_image_path, "Background.png"), resize=w_h
        )

        # background layers
        bg_layer_size = int(w_h[0] * 1.2), int(w_h[1] * 1.2)
        bg_layers: dict = {}
        for i in range(1, 4):
            bg_layers[i] = cls.__get_image(
                os.path.join(background_image_path, f"Layers/{i}.png"),
                resize=bg_layer_size,
            )
        # foreground layers
        fg_layer_size = int(w_h[0]), int(w_h[1] * 0.5)
        fg_layers: dict = {}
        for i in range(5, 6):
            fg_layers[i - 3] = cls.__get_image(
                os.path.join(background_image_path, f"Layers/{i}.png"),
                resize=fg_layer_size,
            )

        return {
            "background": background_image,
            "background_layers": {**bg_layers},
            "foreground_layers": {**fg_layers},
        }

    @classmethod
    def platform_assets(cls) -> dict:
        """
        Load platform images
        """
        platform_image_path = os.path.join(
            cls.current_path, "levels/environment/env_assets/tiles"
        )

        tiles: dict = {}
        for i in range(1, 61):
            tiles[f"tile-{i}"] = cls.__get_image(
                os.path.join(platform_image_path, f"Tile_{i}.png")
            )

        # 128, 128
        water_image = pygame.image.load(
            os.path.join(cls.current_path, "levels/environment/env_assets/water.png")
        ).convert()
        water_image_rect = water_image.get_rect()
        # water back ground image and rect
        wbg_rect = pygame.Rect((0, 0, water_image_rect.width, water_image_rect.height))
        wbg_image = pygame.Surface(wbg_rect.size).convert()
        wbg_image.blit(water_image, (0, 0), wbg_rect)
        colorkey = wbg_image.get_at((1, 1))
        wbg_image.set_colorkey(colorkey, pygame.RLEACCEL)

        return {
            "platform_images": {**tiles},
            "wave_image": wbg_image,
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
            "red_fb_fire_imgs": red_fb_fire_imgs,
        }

        # scale up the fireball images
        for key in fireball_imgs_dict:
            fireball_imgs_dict[key] = [
                pygame.transform.scale(x, (16, 13)) for x in fireball_imgs_dict[key]
            ]

        return fireball_imgs_dict

    @classmethod
    def load_player_images(cls) -> dict:
        """ Load player images and masks from assets folder """
        player_ss_path = os.path.join(
            cls.current_path, "sprites/sprite_assets/player_assets/MageSpriteSheet.png"
        )
        ss_tool = SpriteSheet(player_ss_path)

        def get_animations(coords_list: list, key: str) -> dict:
            right_images = []
            for coord in coords_list:
                image = ss_tool.image_at(coord, cls.p_colorkey)
                image = pygame.transform.scale(
                    image, (int(image.get_width() * 1.8), int(image.get_height() * 1.8))
                )
                mask = pygame.mask.from_surface(image)
                right_images.append((image, mask))

            temp_image_masks = right_images[:]
            left_images = []
            for i in range(0, len(right_images)):
                left_images.append(
                    (
                        pygame.transform.flip(temp_image_masks[i][0], True, False),
                        pygame.mask.from_surface(temp_image_masks[i][0]),
                    )
                )

            return {f"{key}_right": right_images, f"{key}_left": left_images}

        return {
            **get_animations(cls.player_coords["idle"], "idle"),
            **get_animations(cls.player_coords["walk"], "walk"),
            **get_animations(cls.player_coords["jump"], "jump"),
            **get_animations(cls.player_coords["hit"], "hit"),
            **get_animations(cls.player_coords["death"], "death"),
        }

    @classmethod
    def turret_assets(cls) -> dict:
        """
        Get turret images for animation and projectile
        """
        turret_imgs_path = os.path.join(
            cls.current_path, "sprites/sprite_assets/turret"
        )
        images_list: list = os.listdir(turret_imgs_path)
        # Sort the images by the number value in the file name string
        images_list.sort(key=lambda img_string: img_string[7])

        loaded_images: list = []
        for img in images_list:
            img_path = os.path.join(turret_imgs_path, img)
            loaded_images.append(pygame.image.load(img_path).convert())

        return {"turret_images": loaded_images}

    @classmethod
    def projectile_assets(cls) -> dict:
        """
        Get all of the level one assets in one dict
        """
        fireballs = cls.fireball_assets()
        enemy_projectiles = cls.enemy_projectile_assets()
        return {**fireballs, **enemy_projectiles}
