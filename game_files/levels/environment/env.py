from pygame import Surface

class Environment:
    """Holds and updates backgorund and foreground"""
    width: int = 0
    height: int = 0

    def __init__(self, background: dict, foreground: dict, w_h: tuple):
        Environment.width = w_h[0]
        Environment.height = w_h[1]

        self.fg_layers: dict = {}
        for num, key in enumerate(foreground):
            self.fg_layers[key] = _LayerGroup(
                foreground[key], (1.0+(num+1*2.0))
                )

        self.bg_layers: dict = {}
        for num, key in enumerate(background):
            self.bg_layers[key] = _LayerGroup(
                background[key], (1.0-(num+1*0.18))
            )

    def scroll(self, x_scroll: float, y_scroll: float):
        for layer in self.bg_layers:
            if not layer == 1:# dont scroll the base background
                self.bg_layers[layer].update(-x_scroll, y_scroll)
        for layer in self.fg_layers:
            self.fg_layers[layer].update(x_scroll, y_scroll)

class _LayerGroup:
    """group of images that make up a layer of the parallax background"""
    def __init__(self, image: Surface, speed_mod: float) -> None:
        self.speed_modifier = speed_mod
        self.left = _Layer(image)
        self.middle = _Layer(image)
        self.right = _Layer(image)

        self.images: list = [
            (self.left.image, self.left.rect),
            (self.middle.image, self.middle.rect),
            (self.right.image, self.right.rect)
        ]

    def __cycle_positions(self, dir_flag: bool):
        """
        swap the layers positions
        True = move right layer to the left
        False = move left layer to the right
        """
        old_middle = self.middle
        old_left = self.left
        old_right = self.right

        if dir_flag:
            self.left = old_right
            self.middle = old_left
            self.right = old_middle
        else:
            self.left = old_middle
            self.middle = old_right
            self.right = old_left

    def update(self, x: float, y: float):
        self.middle.x += float(x*self.speed_modifier)
        self.middle.rect.x = int(self.middle.x)
        # middle image goes off of the screen to the right
        if self.middle.rect.x > Environment.width:
            self.__cycle_positions(True)
        # middle image goes off of the screen ro themleft
        elif self.middle.rect.right < 0:
            self.__cycle_positions(False)

        self.left.rect.midright = self.middle.rect.midleft
        self.right.rect.midleft = self.middle.rect.midright

class _Layer:

    def __init__(self, image: Surface) -> None:
        self.image = image
        self.rect = self.image.get_rect()
        self.x: float = float(self.rect.x)
        self.y: float = float(self.rect.y)

    def update(self, x: float, y: float):
        self.x += float(x*self.speed_modifier)
        self.rect.x = int(self.x)
