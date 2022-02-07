import pygame
import os


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
    fireball_assets: dict = None

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
    player_assets: dict = None

    background_assets: dict = None

    platform_assets: dict = None

    env_assets: dict = None

    enemy_projectile_assets: dict = None

    fireball_assets: dict = None

    turret_assets: dict = None

    projectile_assets: dict = None

    def __get_image_at(
        rectangle: tuple,
        filepath: str,
        colorkey: tuple = None,
        scale: tuple = None,
    ):
        """Load specific image from a specific rectangle"""
        # Loads image from x, y, x+offset, y+offset
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(pygame.image.load(filepath), (0, 0), rect)
        if colorkey:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        if scale:
            return pygame.transform.scale(image, scale)
        return image

    @classmethod
    def __get_images_at(
        cls,
        rects,
        filepath,
        colorkey=None,
        scale=None,
    ) -> list:
        """Load a whole numch of images from a single file and return them as a list"""
        if not scale:
            return [cls.__get_image_at(rect, filepath, colorkey) for rect in rects]
        return [
            pygame.transform.scale(cls.__get_image_at(rect, filepath, colorkey), scale)
            for rect in rects
        ]

    @classmethod
    def get_background_assets(cls, w_h: tuple) -> dict:
        """
        Load all background images
        w_h: tuple -> (screen_wdith, screen_height)
        """
        if cls.background_assets:
            return cls.background_assets

        background_image_path = os.path.join(
            cls.current_path, "screens/levels/environment/env_assets/background/Layers"
        )

        # layers staring dims (576, 324)
        # background layers
        bg_layer_size = int(w_h[0] * 1.2), int(w_h[1] * 1.2)
        bg_layers: dict = {}
        for i in range(1, 4):
            bg_layers[i] = pygame.transform.scale(
                pygame.image.load(
                    os.path.join(background_image_path, f"{i}.png")
                ).convert(),
                bg_layer_size,
            )

        # foreground layers
        fg_layer_size = int(w_h[0]), int(w_h[1] * 0.5)
        fg_layers: dict = {}
        for i in range(5, 6):
            fg_layers[i - 3] = pygame.transform.scale(
                pygame.image.load(
                    os.path.join(background_image_path, f"{i}.png")
                ).convert(),
                fg_layer_size,
            )

        cls.background_assets = {
            "background_layers": {**bg_layers},
            "foreground_layers": {**fg_layers},
        }
        return cls.background_assets

    @classmethod
    def get_platform_assets(cls) -> dict:
        """
        Load platform images
        """
        if cls.platform_assets:
            return cls.platform_assets
        platform_image_path = os.path.join(
            cls.current_path, "screens/levels/environment/env_assets/tiles"
        )

        tiles: dict = {}
        for i in range(1, 61):
            tiles[f"tile-{i}"] = pygame.image.load(
                os.path.join(platform_image_path, f"Tile_{i}.png")
            ).convert()

        cls.platform_assets = {"platform_images": {**tiles}}
        return cls.platform_assets

    @classmethod
    def get_env_assets(cls) -> dict:
        """
        Get images for the level environment
        """
        if cls.env_assets:
            return cls.env_assets
        wave_image = pygame.image.load(
            os.path.join(
                cls.current_path, "screens/levels/environment/env_assets/water.png"
            )
        ).convert()  # default size (128, 128)

        wave_image.set_colorkey(wave_image.get_at((0, 0)))

        cls.env_assets = {"wave_image": wave_image}
        return cls.env_assets

    @classmethod
    def get_enemy_projectile_assets(cls) -> dict:
        """
        load enemy projectile images
        """
        if cls.enemy_projectile_assets:
            return cls.enemy_projectile_assets
        # load lasers
        laser_img_path = os.path.join(
            cls.current_path, "screens/levels/sprites/sprite_assets/laser.png"
        )
        laser_img = pygame.image.load(laser_img_path)

        cls.enemy_projectile_assets = {"laser_img": laser_img}
        return cls.enemy_projectile_assets

    @classmethod
    def get_fireball_assets(cls) -> dict:
        """
        Load the level one assets that are created and destroyed
        durring gameplay and return them in a dict
        """
        if cls.fireball_assets:
            return cls.fireball_assets
        # load fireballs
        path: str = os.path.join(
            cls.current_path,
            "screens/levels/sprites/sprite_assets/player_assets/fireballs.png",
        )
        fb_size: tuple = (16, 13)

        purp_fb_idle_imgs = cls.__get_images_at(
            cls.fireball_coords["idle_purp"], path, cls.p_colorkey, fb_size
        )

        blue_fb_idle_imgs = cls.__get_images_at(
            cls.fireball_coords["idle_blue"],
            path,
            colorkey=cls.p_colorkey,
            scale=fb_size,
        )

        red_fb_idle_imgs = cls.__get_images_at(
            cls.fireball_coords["idle_red"],
            path,
            colorkey=cls.p_colorkey,
            scale=fb_size,
        )

        purp_fb_fire_imgs = cls.__get_images_at(
            cls.fireball_coords["fire_purp"],
            path,
            colorkey=cls.p_colorkey,
            scale=fb_size,
        )

        blue_fb_fire_imgs = cls.__get_images_at(
            cls.fireball_coords["fire_blue"],
            path,
            colorkey=cls.p_colorkey,
            scale=fb_size,
        )

        red_fb_fire_imgs = cls.__get_images_at(
            cls.fireball_coords["fire_red"],
            path,
            colorkey=cls.p_colorkey,
            scale=fb_size,
        )

        # special attack fireballs
        super_fb_size = (24, 20)
        red_sfb_fire_imgs = cls.__get_images_at(
            cls.fireball_coords["fire_red"],
            path,
            colorkey=cls.p_colorkey,
            scale=super_fb_size,
        )
        blue_sfb_fire_imgs = cls.__get_images_at(
            cls.fireball_coords["fire_blue"],
            path,
            colorkey=cls.p_colorkey,
            scale=super_fb_size,
        )
        purp_sfb_fire_imgs = cls.__get_images_at(
            cls.fireball_coords["fire_purp"],
            path,
            colorkey=cls.p_colorkey,
            scale=super_fb_size,
        )

        fireball_imgs_dict: dict = {
            "purple_fb_idle_imgs": purp_fb_idle_imgs,
            "blue_fb_idle_imgs": blue_fb_idle_imgs,
            "red_fb_idle_imgs": red_fb_idle_imgs,
            "purple_fb_fire_imgs": purp_fb_fire_imgs,
            "blue_fb_fire_imgs": blue_fb_fire_imgs,
            "red_fb_fire_imgs": red_fb_fire_imgs,
        }

        # Add the super fireballs after the rescaling
        fireball_imgs_dict["red_sfb_fire_imgs"] = red_sfb_fire_imgs
        fireball_imgs_dict["blue_sfb_fire_imgs"] = blue_sfb_fire_imgs
        fireball_imgs_dict["purple_sfb_fire_imgs"] = purp_sfb_fire_imgs

        cls.fireball_assets = fireball_imgs_dict
        return cls.fireball_assets

    @classmethod
    def get_player_images(cls) -> dict:
        """Load player images and masks from assets folder"""
        if cls.player_assets:
            return cls.player_assets
        path = os.path.join(
            cls.current_path,
            "screens/levels/sprites/sprite_assets/player_assets/MageSpriteSheet.png",
        )

        def get_animations(coords_list: list, key: str) -> dict:
            right_images = []
            for coord in coords_list:
                image = cls.__get_image_at(coord, path, cls.p_colorkey)
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

        cls.player_assets = {
            **get_animations(cls.player_coords["idle"], "idle"),
            **get_animations(cls.player_coords["walk"], "walk"),
            **get_animations(cls.player_coords["jump"], "jump"),
            **get_animations(cls.player_coords["hit"], "hit"),
            **get_animations(cls.player_coords["death"], "death"),
        }
        return cls.player_assets

    @classmethod
    def get_turret_assets(cls) -> dict:
        """
        Get turret images for animation and projectile
        """
        if cls.turret_assets:
            return cls.turret_assets
        turret_imgs_path = os.path.join(
            cls.current_path, "screens/levels/sprites/sprite_assets/turret"
        )
        images_list: list = os.listdir(turret_imgs_path)
        # Sort the images by the number value in the file name string
        images_list.sort(key=lambda img_string: img_string[7])

        loaded_images: list = []
        for img in images_list:
            img_path = os.path.join(turret_imgs_path, img)
            loaded_images.append(pygame.image.load(img_path).convert())

        cls.turret_assets = {"turret_images": loaded_images}
        return cls.turret_assets

    @classmethod
    def get_projectile_assets(cls) -> dict:
        """
        Get all of the level one assets in one dict
        """
        if cls.projectile_assets:
            return cls.projectile_assets
        fireballs = cls.get_fireball_assets()
        enemy_projectiles = cls.get_enemy_projectile_assets()
        cls.projectile_assets = {**fireballs, **enemy_projectiles}
        return cls.projectile_assets

    @classmethod
    def cut_image(
        cls,
        path: str,
        grid: tuple[int, int],
        scale: tuple[int, int],
        margins: tuple = (0, 0, 0, 0),
    ) -> list[pygame.Surface]:
        """
        cut the image by the given dimensions
        grid: tuple[col, rows]
        margins: tuple[top, bottom, left, right]
        """
        image: pygame.Surface = pygame.image.load(path).convert_alpha()
        rect: pygame.Rect = image.get_rect()
        img_width: int = int((rect.width - (margins[2] + margins[3])) / grid[0])
        img_height: int = int((rect.height - (margins[0] + margins[1])) / grid[1])

        cut_buttons = []
        for column in [int(img_width * i) + margins[3] for i in range(grid[0])]:
            for row in [int(img_height * i) + margins[0] for i in range(grid[1])]:

                new_button: pygame.Surface = pygame.Surface((img_width, img_height))
                new_button.blit(
                    image, (0, 0), area=[column, row, img_width, img_height]
                )
                new_button = pygame.transform.scale(new_button, scale)
                new_button.set_colorkey(new_button.get_at((0, 0)))

                cut_buttons.append(new_button)
        return cut_buttons
