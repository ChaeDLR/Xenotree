import pygame.font
from pygame import Surface, Rect
from .screen_colors import ScreenColors


class MenuBase(Surface):
    """ Parent class for the game menus """

    def __init__(self, width: int, height: int):
        super().__init__((width, height))
        # Set menu colors
        colors = ScreenColors()
        self.background_color = colors.bg_color
        self.text_color = colors.text_color
        # set menu font and rect
        self.font = pygame.font.SysFont(None, 56, bold=True)
        self.rect = Rect(0, 0, width, height)

        self.width, self.height = width, height
