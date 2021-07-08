from pygame import Surface, Rect, transform, mask
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
        image=None,
        connect_left: bool = False,
        connect_right: bool = False,
        moving: bool = False
    ):
        """
        w_h: tuple (width, height)
        x_y: tuple (x_position, y_position)
        """
        super().__init__()
        self.colors = ScreenColors()
        # These bools will be used to check if the platform is connected to another platform
        # on either side
        self.connected_left = connect_left
        self.connected_right = connect_right

        self.moving = moving

        if w_h and image:
            self.__create_imaged_platform(x_y, image, scale=w_h)
        # use platform image at the default size
        elif image:
            self.__create_imaged_platform(x_y, image)
        else:
            self.__build_black_platform(x_y, w_h)

    def __create_imaged_platform(self, pos: tuple, image: Surface, scale=None):
        """
        Create a platform out of given image
        """
        self.image = image
        if scale:
            self.image = transform.scale(self.image, scale)
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

    def set_position(self, x_pos=None, y_pos=None):
        """ Set the position of the wall """
        if x_pos:
            self.rect.x = x_pos
        if y_pos:
            self.rect.y = y_pos

    def resize_wall(self, width: int, height: int):
        """ Resize the wall width, height """
        self.rect = Rect(0, 0, width, height)
    
    def update(self, movement_speed: float):
        """
        update the platforms position if it should be moving
        """
        if self.moving:
            self.x -= float(movement_speed)
            self.rect.x = self.x
