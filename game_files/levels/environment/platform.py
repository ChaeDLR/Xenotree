from pygame import Rect
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

    def resize_wall(self, width: int, height: int):
        """ Resize the wall width, height """
        self.rect = Rect(self.rect.x, self.rect.y, width, height)

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
