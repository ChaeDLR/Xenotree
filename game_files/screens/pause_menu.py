import pygame
from .menu_base import MenuBase
from .button import Button


class PauseMenu(MenuBase):
    def __init__(self, w_h: tuple, stats: object, settings: object):
        super().__init__(w_h, stats, settings)

        self._load_buttons()
        self._load_text()

    def _load_buttons(self):
        self.resume_button = Button(self, "Resume")
        self.quit_button = Button(self, "Quit")
        self.resume_button.set_position(y_pos=(self.height / 2))

    def _load_text(self):
        self.text_image = self.font.render(
            "PAUSED", False, self.text_color, self.background_color
        )
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.midtop = self.rect.midtop
        self.text_image_rect.y += 60

    def _unpause_game(self):
        self.stats.game_active = True
        self.stats.game_paused = False

    def check_buttons(self, mouse_pos):
        if self.resume_button.check_button(mouse_pos):
            self._unpause_game()
        elif self.quit_button.check_button(mouse_pos):
            self.stats.set_active_screen(main_menu=True)

    def update(self):
        self.check_base_events(self.check_buttons)
        self.fill(self.background_color, self.rect)
        self.blit(self.text_image, self.text_image_rect)
        self.quit_button.blitme()
        self.resume_button.blitme()
