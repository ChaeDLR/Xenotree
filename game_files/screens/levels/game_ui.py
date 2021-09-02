from .ui_components import *


class GameUi:
    """Game ui"""

    def __init__(self, assets: dict):
        """initialize  ui components"""
        self.health_bar = HealthBar((10, 10))
        self.active_weapon_bar = WeaponBar((120, 10), assets)
        self.cooldown_bar = CooldownBar(
            (self.health_bar.rect.x, self.health_bar.rect.bottom + 5)
        )

        self.colors: dict = {
            "red": assets["red_fb_idle_imgs"][0].get_at((4, 2)),
            "blue": assets["blue_fb_idle_imgs"][0].get_at((4, 2)),
            "purple": assets["purple_fb_idle_imgs"][0].get_at((4, 2)),
        }

        # (img, rect)
        self.components = [
            (self.health_bar.image, self.health_bar.rect),
            (self.cooldown_bar.image, self.cooldown_bar.rect),
            self.active_weapon_bar.red,
            self.active_weapon_bar.blue,
            self.active_weapon_bar.purple,
        ]

    def update(self, player_health: int, cooldown: int):
        """
        Calls needed to update ui elements
        """
        self.health_bar.update(player_health)
        self.active_weapon_bar.update()
        self.cooldown_bar.update(
            cooldown, self.colors[self.active_weapon_bar.element_type]
        )
