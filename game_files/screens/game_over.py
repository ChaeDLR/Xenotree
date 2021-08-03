import pygame.font
import sys
from .menu_base import MenuBase
from .button import Button
from .screen_colors import ScreenColors


class Game_Over(MenuBase):
    def __init__(self, w_h: tuple, stats, settings):
        super().__init__(w_h, stats, settings)
        colors = ScreenColors()
        self.background_color = colors.bg_color
        self.text_color = colors.text_color
        self.rect = pygame.Rect(0, 0, w_h[0], w_h[1])

        self.width, self.height = w_h[0], w_h[1]

        self.buttons: list = self._load_buttons()
        self.game_over_img, self.game_over_img_rect = self.create_text(
            (self.rect.centerx, 40), "GAME OVER", textsize=100
        )

    def _load_buttons(self) -> list:
        """create buttons needed for the menu screen and store objects in a list"""
        self.main_menu_button = Button(self, "Main Menu", font_size=32)
        self.main_menu_button.resize((150, 50))
        self.quit_button = Button(self, "Quit")
        self.main_menu_button.set_position(y_pos=self.rect.height / 2)
        return [self.main_menu_button, self.quit_button]

    def check_button_down(self, mouse_pos):
        self.main_menu_button.check_button(mouse_pos)
        self.quit_button.check_button(mouse_pos)

    def check_button_up(self, mouse_pos):
        if self.main_menu_button.check_button(mouse_pos, True):
            self.stats.set_active_screen(main_menu=True)
        elif self.quit_button.check_button(mouse_pos, True):
            sys.exit()
        else:
            for button in self.buttons:
                button.reset_alpha()

    def update(self):
        self.check_base_events(self.check_button_down, self.check_button_up)
        self.fill(self.background_color, self.rect)
        self.blit(self.game_over_img, self.game_over_img_rect)
        self.main_menu_button.blitme()
        self.quit_button.blitme()
