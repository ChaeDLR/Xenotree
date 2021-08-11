import pygame.font
import sys
from ..screen_base import ScreenBase
from .button import Button


class GameOver(ScreenBase):
    def __init__(self):
        super().__init__()

        self.buttons: list = self._load_buttons()
        self.game_over_img, self.game_over_img_rect = self.create_text(
            (self.rect.centerx, 40), "GAME OVER", textsize=100
        )

    def _load_buttons(self) -> list:
        """create buttons needed for the menu screen and store objects in a list"""
        self.main_menu_button = Button(self.image, "Main Menu", font_size=32)
        self.main_menu_button.resize((150, 50))
        self.quit_button = Button(self.image, "Quit")
        self.main_menu_button.set_position(y_pos=self.rect.height / 2)
        return [self.main_menu_button, self.quit_button]

    def check_button_down(self, mouse_pos):
        self.main_menu_button.check_button(mouse_pos)
        self.quit_button.check_button(mouse_pos)

    def check_button_up(self, mouse_pos):
        if self.main_menu_button.check_button(mouse_pos, True):
            ScreenBase.change_screen = True
            ScreenBase.current_screen_key = "main_menu"
        elif self.quit_button.check_button(mouse_pos, True):
            sys.exit()
        else:
            for button in self.buttons:
                button.reset_alpha()

    def check_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.check_button_down(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.check_button_up(event.pos)

    def update(self):
        self.image.fill(self.background_color, self.rect)
        self.image.blit(self.game_over_img, self.game_over_img_rect)
        self.main_menu_button.blitme()
        self.quit_button.blitme()
