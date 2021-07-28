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
            platform.connect_right(self)

    def connect_right(self, platform: Sprite):
        """
        Connect a platform to this platforms right if not already connected
        """
        if not self.connected_right:
            self.connected_right = True
            self.connected_right_platform = platform
            platform.connect_left(self)

    def set_position(self, x_pos=None, y_pos=None):
        """ Set the position of the wall """
        if x_pos:
            self.x = float(x_pos)
            self.rect.x = int(self.x)
        if y_pos:
            self.y = float(y_pos)
            self.rect.y = int(self.y)

    def resize_wall(self, width: int, height: int):
        """ Resize the wall width, height """
        self.rect = Rect(self.rect.x, self.rect.y, width, height)

    def update(self, scroll_x: float = 0.0, scroll_y: float = 0.0):
        """
        update the platforms position if it should be moving
        """
        self.x += scroll_x
        self.y += scroll_y
        self.rect.x, self.rect.y = int(self.x), int(self.y)


class Wave(Platform):
    """
    Child platform with class variables used to track their position in a queue
    """

    first: Platform = None
    last: Platform = None

    def __init__(self, x_y: tuple, images):
        super().__init__(
            x_y=x_y,
            img_rect=(images["wave_image"], images["wave_image"].get_rect()),
            moving=True,
        )
        # Each wave will point to the next wave in the queue
        self.next: Platform = None

    def update(self, scroll_y: float):
        super().update(scroll_y=scroll_y)
        self.x -= 4.5
        self.rect.x = self.x
