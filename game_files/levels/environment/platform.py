from pygame import Surface, Rect, transform, mask
import pygame
from pygame.sprite import Sprite
from ...screens.screen_colors import ScreenColors


class Platform(Sprite):
    """
    platform size of width, height args
    Stops player from moving
    """

    def __init__(
        self,
        x_y: tuple,
        w_h: tuple = None,
        images: list = None,
        image_key: str = None,
        moving: bool = False,
    ):
        """
        w_h: tuple (width, height)
        x_y: tuple (x_position, y_position)
        """
        super().__init__()
        self.colors = ScreenColors()

        self.moving = moving
        self.connected_left, self.connected_right = False, False
        self.frozen = False

        if image_key:
            img_key = image_key
        else:
            img_key = "normal"

        if w_h and images:
            self.images = images
            self.__create_imaged_platform(x_y, image_key=img_key, scale=w_h)
        # use platform image at the default size
        elif images:
            self.images = images
            self.__create_imaged_platform(x_y, image_key=img_key)
        else:
            self.__build_black_platform(x_y, w_h)

    def __create_imaged_platform(self, pos: tuple, image_key: str, scale=None):
        """
        Create a platform out of given image
        """
        if scale:
            for img_str in self.images:
                self.images[img_str] = transform.scale(self.images[img_str], scale)
        self.image = self.images[image_key]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.x, self.y = float(self.rect.x), float(self.rect.y)
        self.width, self.height = self.rect.width, self.rect.height
        self.mask = mask.from_surface(self.image)

    def __build_black_platform(self, pos: tuple, dims: tuple):
        """
        x_y position
        wodth_height dimentions
        """
        self.width, self.height = pos
        self.image = Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = dims
        self.image.fill(self.colors.platform_color)

    def connect_left(self, platform: Sprite):
        """
        Connect a platform to this platforms left if not already connected
        """
        if not self.connected_left:
            self.connected_left = True
            self.connected_left_platform = platform
            platform.connect_right(self)

    def connect_right(self, platform: Sprite):
        """
        Connect a platform to this platforms right if not already connected
        """
        if not self.connected_right:
            self.connected_right = True
            self.connected_right_platform = platform
            platform.connect_left(self)

    def freeze(self):
        """
        Switch the platform image and stop it's movement
        """
        if not self.frozen:
            self.image = self.images["frozen"]
            self.frozen = True
            self.moving = False
            if self.connected_right:
                self.connected_right_platform.freeze()
            if self.connected_left:
                self.connected_left_platform.freeze()

    def unfreeze(self):
        """
        Switch platform image and start movement
        """
        self.image = self.images["normal"]
        # self.moving = True

    def set_position(self, x_pos=None, y_pos=None):
        """ Set the position of the wall """
        if x_pos:
            self.x = float(x_pos)
            self.rect.x = self.x
        if y_pos:
            self.y = float(y_pos)
            self.rect.y = y_pos

    def resize_wall(self, width: int, height: int):
        """ Resize the wall width, height """
        self.rect = Rect(0, 0, width, height)

    def update(self, movement_speed: float):
        """
        update the platforms position if it should be moving
        """
        if self.moving:
            self.movement_speed = float(movement_speed)
            self.x -= self.movement_speed
            self.rect.x = self.x


class Wave(Platform):
    """
    Child platform with class variables used to track their position in a queue
    """

    first: Platform = None
    last: Platform = None

    def __init__(self, x_y: tuple, images, w_h: tuple = None):
        super().__init__(
            x_y, w_h=w_h, images=images, image_key="wave_image", moving=True
        )
        # Each wave will point to the next wave in the queue
        self.next: Platform = None
