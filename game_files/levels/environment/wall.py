from pygame import Surface
from pygame import Rect
from pygame.sprite import Sprite


class Wall(Sprite):
    """
        Wall object size of width, height args
        Stops player from moving 
    """

    def __init__(self, w_h: tuple, x_y: tuple):
        """
            w_h: tuple (width, height)
            x_y: tuple (x_position, y_position)
        """
        self.width, self.height = w_h[0], w_h[1]
        super().__init__()

        self._build_wall(x_y[0], x_y[1])

    def _build_wall(self, x: int, y: int):
        self.image = Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image.fill((10, 10, 10))

    def set_position(self, x_pos=None, y_pos=None):
        """ Set the position of the wall """
        if x_pos:
            self.rect.x = x_pos
        if y_pos:
            self.rect.y = y_pos

    def resize_wall(self, width: int, height: int):
        """ Resize the wall width, height """
        self.rect = Rect(0, 0, width, height)
        self.fill((10, 10, 10))
