from pygame import Surface, transform


class WaveGroup:
    """This class is meant to be used as a layer group in the Environment class"""

    def __init__(
        self,
        y: int,
        img: Surface,
        wave_speed: float,
        wave_count: int,
    ):
        """
        y: int -> where to place the waves loop
        img: Surface -> the preloaded wave image
        wave_speed: float -> how fast to move the waves
        wave_count: int -> how many waves to put in the queue
        y_limit: int -> set a stop value for waves moving up the screen
        """
        self.wave_speed: float = wave_speed
        self.first: Surface = None
        self.last: Surface = None

        self.__create_waves_group(wave_count, y, img=img)

    def __create_waves_group(self, count: int, y: float, img: Surface):
        # all the waves (image, rect) tuples
        self.images: list = []
        # group of all the wave objects
        self.group: list = []
        wave_rect = img.get_rect()
        wave_width = wave_rect.width

        for i in range(count, -1, -1):
            new_wave: Wave = Wave((wave_width * i, y), img, self.wave_speed)
            if i == 0:
                self.first = new_wave
                new_wave.next = previous_wave
            elif i == count:
                self.last = new_wave
            else:
                new_wave.next = previous_wave

            self.images.append((new_wave.image, new_wave.rect))
            self.group.append(new_wave)
            previous_wave = new_wave

    def resize_waves(self, width: int = None, height: int = None):
        """
        Resize all of the waves in the wave group
        """
        self.images.clear()
        for wave in self.group:
            wave.resize(
                width=width,
                height=height,
            )
            self.images.append((wave.image, wave.rect))

    def update(self, scroll_x: float, scroll_y: float):
        """
        WaveGroup has a constant x decrement so we dont need scroll x
        however all layergroup's update methods will be passed an scrool x and y value
        """
        for wave in self.group:
            wave.update(scroll_y=scroll_y)
        # cycle waves
        if self.first.rect.x < -self.first.rect.width:
            self.first.set_position(x_pos=(self.last.rect.x + self.last.rect.width))
            self.last.next = self.first
            self.last = self.first
            self.first = self.first.next


class Wave:
    """
    Child platform with class variables used to track their position in a queue
    """

    def __init__(self, x_y: tuple, image: Surface, wave_speed: float):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = x_y
        self.x, self.y = float(self.rect.x), float(self.rect.y)
        # Each wave will point to the next wave in the queue
        self.next = None
        self.wave_speed = wave_speed

    def resize(self, width: int = None, height: int = None):
        """
        update image and rect to a new size
        """
        new_width, new_height = self.rect.width, self.rect.height
        if width:
            new_width = width
        if height:
            new_height = height
        self.image = transform.scale(self.image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = int(self.x), int(self.y)

    def set_position(self, x_pos: int = None, y_pos: int = None):
        if x_pos:
            self.rect.x = x_pos
            self.x = float(self.rect.x)
        if y_pos:
            self.rect.y = y_pos
            self.y = float(self.rect.y)

    def update(self, scroll_y: float):
        self.x -= self.wave_speed
        self.rect.x = self.x
        if not scroll_y == 0.0:
            self.y += scroll_y
            self.rect.y = int(self.y)
