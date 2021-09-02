from pygame import Surface, SRCALPHA


class _Bar:
    """Base class for a dynamic bar ui element"""

    def __init__(self, coords: tuple, size: tuple):
        self.image = Surface(size, flags=SRCALPHA)
        self.base_color: tuple = (10, 10, 10, 200)
        self.image.fill((10, 10, 10, 200))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords


class HealthBar(_Bar):
    """
    Player health bar surface object
    """

    def __init__(self, coords: tuple):
        super().__init__(coords, size=(100, 25))

    def update(self, health_percentage: int):
        """
        Take the players current health percentage
        to the nearest whole number
        """
        healthbar_img = Surface(
            (health_percentage - 20, self.rect.height - 10)
        ).convert()
        healthbar_img.fill((192, 16, 16))

        self.image.fill(self.base_color)
        self.image.blit(
            healthbar_img,
            (
                self.rect.x,
                self.rect.y - 5,
            ),
        )


class CooldownBar(_Bar):
    """
    Player special attack cooldown bar
    """

    def __init__(self, coords: tuple):
        super().__init__(coords, size=(100, 10))
        self.cooldown_level: int = 100

    def update(self, cooldownlevel: float, color: tuple):
        """
        cooldownlevel: float -> Cooldown reset percentage
        """
        self.image.fill((10, 10, 10, 200))

        if 100 >= cooldownlevel >= 0:
            cd_bar_img = Surface((cooldownlevel, 10)).convert()
        elif cooldownlevel > 100:
            cd_bar_img = Surface((self.cooldown_level, 10)).convert()

        cd_bar_img.fill(color)
        cd_bar_rect = cd_bar_img.get_rect()
        self.image.blit(cd_bar_img, cd_bar_rect)
