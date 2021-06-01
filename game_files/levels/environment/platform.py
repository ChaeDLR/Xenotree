from pygame import Surface
from pygame import Rect
from pygame.sprite import Sprite
from ...screens.screen_colors import ScreenColors


class Platform(Sprite):
    """
    Wall object size of width, height args
    Stops player from moving
    """

    def __init__(self, w_h: tuple, x_y: tuple, image=None):
        """
        w_h: tuple (width, height)
        x_y: tuple (x_position, y_position)
        """
        self.width, self.height = w_h[0], w_h[1]
        super().__init__()
        self.colors = ScreenColors()

        if image:
            self.__create_imaged_platform(x_y[0], x_y[1], image)
        else:
            self.__build_black_platform(x_y[0], x_y[1])

    def __create_imaged_platform(self, x: int, y: int, image):
        """
        Create a platform out of given image
        """
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def __build_black_platform(self, x: int, y: int):
        self.image = Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image.fill(self.colors.platform_color)

    def set_position(self, x_pos=None, y_pos=None):
        """ Set the position of the wall """
        if x_pos:
            self.rect.x = x_pos
        if y_pos:
            self.rect.y = y_pos

    def resize_wall(self, width: int, height: int):
        """ Resize the wall width, height """
        self.rect = Rect(0, 0, width, height)
