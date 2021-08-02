from pygame import transform
from pygame.sprite import Sprite
from ...screens.screen_colors import ScreenColors
from ...game_assets import AssetManager

class Platforms:
    """Uses the _Platform class to generate platforms"""
    # use keys
    # "platform_images" for tiles
    # "wave_image" for waves
    # holds the platform images 
    # but needs to be assigned after the display is init
    platform_assets: dict = None

    @classmethod
    def tile_block(cls, rows_col: tuple, x_y: tuple) -> list:
        """
        Create a tile block of dirt/grass using _Platform
        return the new objects in a list
        rows_col: tuple -> (width, height)
        """
        if not cls.platform_assets:
            Platforms.platform_assets = AssetManager.platform_assets()

        platform_images = cls.platform_assets["platform_images"]
        tile_height = platform_images["tile-1"].get_height()

        tile_group: list = []
        for i in range(1, rows_col[0] + 1):  # row
            previous_platform = None
            for j in range(1, rows_col[1] + 1):  # column

                if j == 1:  # first tile in row
                    if i == 1:  # first row of the block
                        image = platform_images["tile-1"]
                    elif i == rows_col[0]:  # last row of the block
                        image = platform_images["tile-1"]
                        image = transform.rotate(image, 90)
                    else:
                        image = platform_images["tile-2"]
                        image = transform.rotate(image, 90)
                    floor_tile = _Platform(
                        (x_y[0], x_y[1] + (tile_height * (i - 1))),
                        img=image,
                    )

                elif j == rows_col[1]:  # last tile
                    if i == 1:  # first row of the block
                        image = platform_images["tile-3"]  # corner tile top-left
                    elif i == rows_col[0]:  # last row of the block
                        image = platform_images["tile-3"]
                        image = transform.rotate(image, -90)
                    else:  # all the rows inbetween
                        image = platform_images["tile-2"]
                        image = transform.rotate(image, -90)
                    floor_tile = _Platform(
                        previous_platform.rect.topright,
                        img=image,
                    )

                else:  # middle tiles
                    if i == 1:  # first row of the block
                        image = platform_images["tile-2"]
                    elif i == rows_col[0]:  # last row of the block
                        image = platform_images["tile-2"]
                        image = transform.rotate(image, 180)
                    else:
                        image = platform_images["tile-12"]
                    floor_tile = _Platform(
                        previous_platform.rect.topright,
                        img=image,
                    )
                    floor_tile.connect_left(previous_platform)

                tile_group.append(floor_tile)
                previous_platform = floor_tile
        return tile_group

class _Platform(Sprite):
    """
    platform size of width, height args
    Stops player from moving
    """

    def __init__(
        self,
        x_y: tuple,
        img,
        moving: bool = False,
    ):
        """
        img_rect: tuple (image, rect)
        """
        super().__init__()
        self.colors = ScreenColors()
        self.image = img
        self.rect = self.image.get_rect()
        self.x, self.y = float(x_y[0]), float(x_y[1])
        self.set_position(x_y[0], x_y[1])
        self.moving = moving
        self.connected_left, self.connected_right = False, False
        self.frozen = False

    def connect_left(self, platform: Sprite):
        """
        Connect a platform to this platforms left if not already connected
        """
        if not self.connected_left:
            self.connected_left = True
            self.connected_left_platform = platform
            self.rect.midleft = platform.rect.midright
            self.x, self.y = float(self.rect.x), float(self.rect.y)
            platform.connect_right(self)

    def connect_right(self, platform: Sprite):
        """
        Connect a platform to this platforms right if not already connected
        """
        if not self.connected_right:
            self.connected_right = True
            self.connected_right_platform = platform
            self.rect.midright = platform.rect.midleft
            self.x, self.y = float(self.rect.x), float(self.rect.y)
            platform.connect_left(self)

    def set_position(self, x_pos=None, y_pos=None):
        """ Set the position of the wall """
        if x_pos:
            self.x = float(x_pos)
            self.rect.x = int(self.x)
        if y_pos:
            self.y = float(y_pos)
            self.rect.y = int(self.y)

    def update(self, scroll_x: float = 0.0, scroll_y: float = 0.0):
        """
        update the platforms position if it should be moving
        """
        if self.connected_left:  # Current fix for the pixel gaps in platform blocks
            self.rect.midleft = self.connected_left_platform.rect.midright
            self.x, self.y = float(self.rect.x), float(self.rect.y)
        else:
            if not scroll_x == 0.0:
                self.x += scroll_x
                self.rect.x = int(self.x)
            if not scroll_y == 0.0:
                self.y += scroll_y
                self.rect.y = int(self.y)
