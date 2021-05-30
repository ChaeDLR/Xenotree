from pygame import transform


class WeaponBar:
    def __init__(self, coords: tuple, assets: dict):
        self.x = float(coords[0])
        self.y = float(coords[1])
        self.starting_y = coords[1]

        self.assets = assets
        self.moving_up = True

        self.__load_weapon_bar()
        self.set_positions(cycle=False)

    def __get_fireball(self, color: str) -> tuple:
        """
        red fireball ui element (img, rect)
        """
        fb_img = self.assets[f"{color}_fb_idle_imgs"][0]
        fb_img = transform.scale(fb_img, (17, 25))
        fb_rect = fb_img.get_rect()
        return (fb_img, fb_rect)

    def __load_weapon_bar(self):
        """
        Initial loading of the weapon ui element
        """
        self.red = self.__get_fireball("red")
        self.blue = self.__get_fireball("blue")
        self.purple = self.__get_fireball("purple")

        # default weapons bar order
        self.fire_bar = {"left": self.blue, "mid": self.red, "right": self.purple}

    def set_positions(self, cycle=True):
        """
        Set the positions of each fireball
        """
        pos_left = (140, 20)
        pos_mid = (160, 20)
        pos_right = (180, 20)

        # start cycling code
        if cycle:
            if self.fire_bar["mid"] is self.red:
                self.fire_bar["mid"] = self.blue
                self.fire_bar["left"] = self.purple
                self.fire_bar["right"] = self.red

            elif self.fire_bar["mid"] is self.blue:
                self.fire_bar["mid"] = self.purple
                self.fire_bar["left"] = self.red
                self.fire_bar["right"] = self.blue

            elif self.fire_bar["mid"] is self.purple:
                self.fire_bar["mid"] = self.red
                self.fire_bar["left"] = self.blue
                self.fire_bar["right"] = self.purple

        self.fire_bar["left"][1].center = pos_left
        self.fire_bar["mid"][1].center = pos_mid
        self.fire_bar["right"][1].center = pos_right

        self.fire_bar["left"][0].set_alpha(50)
        self.fire_bar["mid"][0].set_alpha(255)
        self.fire_bar["right"][0].set_alpha(50)

    def update(self, active_fireball: str = None):
        """
        'red', 'blue', 'purple'
        """
        if self.moving_up:
            self.y -= 0.2
            self.fire_bar["mid"][1].y = self.y
            if self.fire_bar["mid"][1].y <= 5:
                self.moving_up = False

        else:
            self.y += 0.2
            self.fire_bar["mid"][1].y = self.y
            if self.fire_bar["mid"][1].y >= self.starting_y:
                self.moving_up = True
