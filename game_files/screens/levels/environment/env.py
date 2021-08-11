from pygame import Surface
from .waves import WaveGroup


class Environment:
    """Holds and updates backgorund and foreground"""

    width: int = 0
    height: int = 0

    def __init__(
        self, background: dict, foreground: dict, w_h: tuple, wave_img: Surface
    ):
        Environment.width = w_h[0]
        Environment.height = w_h[1]
        # create the wave groups
        wave_groups: tuple = self.__load_waves(wave_img)
        # 0 index in list=first_drawn = frontloaded
        # final index in list=last_drawn = backloaded
        # background layer group list
        self.bg_layers: list = self.__load_bg_layers(
            background, backload=wave_groups[0]
        )
        # foreground layer group list
        self.fg_layers: list = self.__load_fg_layers(
            foreground, frontload=wave_groups[1]
        )

    def __load_bg_layers(
        self, background: dict, frontload: any = None, backload: any = None
    ) -> list:
        """
        loads images from a dict, creates _LayerGroup object from it, set position, add to list.
        background: dict -> dict containing surface objects with images already loaded
        Frontload and backload can be any object with an update method that will have it's own layer group
        frontload: any -> place object in the front of the list(will be drawn first)
        backload: any -> place object in the back of the list(will be drawn last)
        returns -> list[*_LayerGroup]
        """
        layer_groups: list = []
        if frontload:
            layer_groups.append(frontload)
        # key starts at 1 because thats how the file is labeled
        for num, key in enumerate(background):
            gap = None
            if key == 3:  # place a gap between the front tree layers
                gap = int(Environment.width / 4)
            # find the y_bounds we should be using
            bg_wiggle_room: int = background[key].get_height() - Environment.height
            new_layer: _LayerGroup = _LayerGroup(
                background[key],
                speed_mod=-1.0 + ((len(background) - num) * 0.30),
                gap=gap,
                y_bound=(-bg_wiggle_room, Environment.height + bg_wiggle_room),
            )
            for layer in new_layer.group:
                layer.rect.centery = int(Environment.height / 2)
                layer.y = float(layer.rect.y)
            layer_groups.append(new_layer)
        if backload:
            layer_groups.append(backload)
        return layer_groups

    def __load_fg_layers(
        self, foreground: dict, frontload: any = None, backload: any = None
    ) -> list:
        """
        loads images from a dict, creates _LayerGroup object from it, set position, add to list.
        background: dict -> dict containing surface objects with images already loaded
        Front and backload can be any object with an update method that will have it's own layer group
        frontload: any -> place object in the front of the list(will be drawn first)
        backload: any -> place object in the back of the list(will be drawn last)
        returns -> list[*_LayerGroup]
        """
        layer_groups: list = []
        if frontload:
            layer_groups.append(frontload)
        for num, key in enumerate(foreground):
            fg_starting_y = int((Environment.height / 24) * 14)
            layer_groups.append(
                _LayerGroup(
                    foreground[key],
                    speed_mod=(1.0 + (num + 1 * 2.0)),
                    y_pos=fg_starting_y,
                    gap=int(foreground[key].get_width() / 2),
                    y_bound=(
                        fg_starting_y - 10,
                        int(fg_starting_y + foreground[key].get_height() * 1.2),
                    ),
                )
            )
        if backload:
            layer_groups.append(backload)
        return layer_groups

    def __load_waves(self, image: Surface) -> tuple:
        """
        Create the background and foreground wave groups
        returns -> tuple (bg wave group, fg wave group)
        """
        num_of_waves: int = int(self.width / image.get_width()) + 2
        bg_waves = WaveGroup(
            y=self.height - 92, img=image, wave_speed=6.0, wave_count=num_of_waves
        )
        fg_waves = WaveGroup(
            y=self.height - 78,
            img=image,
            wave_speed=8.5,
            wave_count=num_of_waves,
        )
        fg_waves.resize_waves(128, 175)
        return (bg_waves, fg_waves)

    def get_bottom(self) -> int:
        """
        Get the y value of the bottom of the env that scrolls across the y
        This will be used to determine if the player has fallen off the stage
        """
        return self.fg_layers[0].first.rect.y

    def scroll(self, x_scroll: float, y_scroll: float):
        for num, bg_lg in enumerate(self.bg_layers):
            if not num == 0:  # dont bother scrolling the base background
                bg_lg.update(-x_scroll, y_scroll)
        for fg_lg in self.fg_layers:
            fg_lg.update(x_scroll, y_scroll)


class _LayerGroup:
    """group of images that make up a layer of the parallax background"""

    def __init__(
        self,
        image: Surface,
        speed_mod: float,
        y_pos: int = None,
        gap: int = None,
        y_bound: tuple = None,
    ) -> None:
        """
        image -> Surface
        speed_mod -> multiplied by x
        layer_count -> number of layers to be created
        y_pos -> set y starting position (topleft)
        gap -> gap between layers
        y_bound: tuple -> (min, max) the range in which the layer is allow to move
        """
        self.speed_modifier = speed_mod
        self.left = _Layer(image)
        self.middle = _Layer(image)
        self.right = _Layer(image)
        self.gap: int = gap
        self.y_bound: tuple = y_bound
        # create an iterable containing the layers
        self.group: list = [
            self.left,
            self.middle,
            self.right,
        ]
        if y_pos:
            for layer in self.group:
                layer.rect.y = y_pos
                layer.y = float(layer.rect.y)

        self.images: list = [(lyr.image, lyr.rect) for lyr in self.group]

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

    def __update_layers_coords(self):
        """
        update the x and y floats for each layer in the class
        """
        self.left.x, self.left.y = float(self.left.rect.x), float(self.left.rect.y)
        self.middle.x, self.middle.y = float(self.middle.rect.x), float(
            self.middle.rect.y
        )
        self.right.x, self.right.y = float(self.right.rect.x), float(self.right.rect.y)

    def update(self, x: float, y: float):
        # control x-axis movement
        self.middle.x += float(x * self.speed_modifier)
        self.middle.rect.x = int(self.middle.x)

        # control y-axis movement
        if not y == 0.0 and self.y_bound:
            # if when we add y the background is still on the sceen
            if (
                self.y_bound[0] < (self.middle.y + y)
                and (self.middle.rect.bottom + y) < self.y_bound[1]
            ):
                self.middle.y += float(y)
                self.middle.rect.y = int(self.middle.y)

        # check if we need to change a layer's position
        if self.gap:
            half_gap: int = int(self.gap / 2)
            if self.middle.rect.x - half_gap > Environment.width:
                self.__cycle_positions(True)
            elif self.middle.rect.right + half_gap < 0:
                self.__cycle_positions(False)
            # realign the left and right layers with mid after being cycled
            # including the gap value
            self.left.rect.midright = (
                self.middle.rect.midleft[0] - self.gap,
                self.middle.rect.midleft[1],
            )
            self.right.rect.midleft = (
                self.middle.rect.midright[0] + self.gap,
                self.middle.rect.midright[1],
            )
        else:
            # middle image goes off of the screen to the right
            if self.middle.rect.x > Environment.width:
                self.__cycle_positions(True)
            # middle image goes off of the screen to the left
            elif self.middle.rect.right < 0:
                self.__cycle_positions(False)
            # realign left and right layers with mid
            self.left.rect.midright = self.middle.rect.midleft
            self.right.rect.midleft = self.middle.rect.midright
        self.__update_layers_coords()


class _Layer:
    def __init__(self, image: Surface) -> None:
        # next = layer to the right
        self.next = None
        self.image = image
        self.rect = self.image.get_rect()
        self.x: float = float(self.rect.x)
        self.y: float = float(self.rect.y)
