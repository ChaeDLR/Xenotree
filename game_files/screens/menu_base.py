import pygame.font
import sys
from abc import ABC, abstractmethod
from pygame import Surface, Rect
from .screen_colors import ScreenColors


class MenuBase(Surface, ABC):
    """ Parent class for the game menus """

    def __init__(
        self, w_h: tuple, stats: object, settings: object, special_flags: int = 0
    ):
        """
        w_h: tuple -> (width, height)
        stats: object -> GameStats
        settings: object -> Settings
        buttons: list -> [*Button]
        """
        super().__init__((w_h[0], w_h[1]), flags=special_flags)

        self.screen_rows = w_h[1] / 6
        self.screen_columns = w_h[0] / 6

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
        # pygame.mouse.set_visible(False)
        # No game music added yet
        # TODO: Add game music
        # pygame.mixer.music.play()

    def check_base_events(self, menu_check_md_event, menu_check_mu_event):
        """
        check for exit event
        or Mouse Down/Mouse Up events on the menu screens
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif not self.stats.game_active:

                if event.type == pygame.MOUSEBUTTONDOWN:
                    menu_check_md_event(pygame.mouse.get_pos())
                elif event.type == pygame.MOUSEBUTTONUP:
                    menu_check_mu_event(pygame.mouse.get_pos())
                elif event.type == pygame.KEYDOWN:
                    return event

    def create_text(
        self, x_y: tuple, text: str, textsize: int = 56, boldtext: bool = True, 
    ) -> tuple:
        """
        Tuple -> (text_img, text_rect)
        """
        text_font = pygame.font.SysFont(None, textsize, bold=boldtext)
        text_img = text_font.render(text, True, self.text_color, self.background_color)
        text_img.set_colorkey(self.background_color)
        text_rect = text_img.get_rect()
        text_rect.center = x_y
        return (text_img, text_rect)

    @abstractmethod
    def update(self):
        """
        Each level needs an update method that with contain all of its blits
        This method is called from the main game loop
        """
        pass
