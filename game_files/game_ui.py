import pygame.font
from .ui_components import *


class Game_Ui:
    """ Game ui """

    def __init__(self, settings, stats):
        """ initialize scoring attributes """
        self.settings = settings
        self.stats = stats

        self.health_bar = HealthBar((10, 10))

    def get_ui_components(self) -> list:
        """
        list[tuple(image, rect)] 
        """
        return [
            (self.health_bar.image, self.health_bar.rect)
        ]

    def update(self, player_health: int):
        """
        Calls needed to update ui elements
        """
        self.health_bar.update(player_health)
