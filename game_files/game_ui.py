import pygame.font
from .ui_components import *


class Game_Ui:
    """ Game ui """

    def __init__(self, settings: object, stats: object, assets: dict):
        """ initialize scoring attributes """
        self.settings = settings
        self.stats = stats

        self.health_bar = HealthBar((10, 10))
        self.active_weapon_bar = ActiveWeapon((120, 10), assets)

    def get_ui_components(self) -> list:
        """
        list[tuple(image, rect)] 
        """
        return [
            (self.health_bar, self.health_bar.rect),
            (self.active_weapon_bar.image, self.active_weapon_bar.rect)
        ]

    def update(self, player_health: int, fireball_type: str=None):
        """
        Calls needed to update ui elements
        """
        self.health_bar.update(player_health)
        # if the player changes the fireball type
        #if fireball_type:
        self.active_weapon_bar.update(fireball_type)
