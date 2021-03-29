# No ui has been made yet
import pygame.font


class Game_Ui:
    """ Displays game ui to surface """

    def __init__(self, surface, settings, stats):
        """ initialize scoring attributes """
        self.screen = surface
        self.screen_rect = self.screen.get_rect()
        self.settings = settings
        self.stats = stats
        self.rect = self.screen_rect

        # text settings
        self.text_color = (200, 200, 200)
        self.text_font = pygame.font.SysFont(None, 34)
