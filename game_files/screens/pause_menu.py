import pygame
from .menu_base import MenuBase
from .button import Button


class PauseMenu(MenuBase):
    def __init__(self, w_h: tuple, stats: object, settings: object):
        super().__init__(w_h, stats, settings)

        self.__load_buttons()
        self.text_image, self.text_image_rect = self.create_text(
            (self.rect.centerx, 60),
            "PAUSED",
            boldtext=False
        )

    def __load_buttons(self):
        self.resume_button = Button(self, "Resume")
        self.quit_button = Button(self, "Quit")
        self.resume_button.set_position(y_pos=(self.height / 2))

    def __unpause_game(self):
        self.stats.game_active = True
        self.stats.game_paused = False

    def check_button_down(self, mouse_pos):
        self.resume_button.check_button(mouse_pos)
        self.quit_button.check_button(mouse_pos)

    def check_button_up(self, mouse_pos):
        if self.resume_button.check_button(mouse_pos, True):
            self.__unpause_game()
        elif self.quit_button.check_button(mouse_pos, True):
            self.stats.set_active_screen(main_menu=True)

    def update(self):
        self.check_base_events(self.check_button_down, self.check_button_up)
        self.fill(self.background_color, self.rect)
        self.blit(self.text_image, self.text_image_rect)
        self.quit_button.blitme()
        self.resume_button.blitme()
