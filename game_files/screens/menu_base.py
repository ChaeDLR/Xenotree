import pygame.font
import sys
from abc import ABC, abstractmethod
from pygame import Surface, Rect
from .screen_colors import ScreenColors


class MenuBase(Surface, ABC):
    """ Parent class for the game menus """

    def __init__(self, w_h: tuple, stats: object, settings: object):
        super().__init__((w_h[0], w_h[1]))
        self.stats = stats
        self.settings = settings
        # Set menu colors
        colors = ScreenColors()
        self.background_color = colors.bg_color
        self.text_color = colors.text_color
        # set menu font and rect
        self.font = pygame.font.SysFont(None, 56, bold=True)
        self.rect = Rect(0, 0, w_h[0], w_h[1])

        self.width, self.height = w_h[0], w_h[1]
    
    def start_game(self):
        """ Reset the game """
        self.stats.set_active_screen(game_active=True)
        self.stats.active_level = 1
        pygame.mouse.set_cursor(pygame.cursors.broken_x)
        #pygame.mouse.set_visible(False)
        # No game music added yet
        # TODO: Add game music
        # pygame.mixer.music.play()

    def check_base_events(self, menu_check_event):
        """ 
        check for exit event 
        or mouse down events on the menu screens
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.stats.game_active:
                mouse_pos = pygame.mouse.get_pos()
                menu_check_event(mouse_pos)
    
    @abstractmethod
    def update(self):
        """
        Each level needs an update method that with contain all of blits for it
        This method is called from the main game loop
        """
        pass
