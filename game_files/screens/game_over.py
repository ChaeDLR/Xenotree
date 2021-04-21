import pygame.font
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

        self._load_buttons()
        self._load_text()

    def _load_buttons(self):
        self.main_menu_button = Button(self, "Main Menu")
        self.main_menu_button.resize((150, 50), 32)
        self.quit_button = Button(self, "Quit")

        self.main_menu_button.set_position(y_pos=self.rect.height / 2)

    def _load_text(self):
        font = pygame.font.SysFont(None, 100, bold=True)
        self.game_over_img = font.render(
            "Game Over", True, self.text_color, self.background_color
        )
        self.game_over_img_rect = self.game_over_img.get_rect()
        self.game_over_img_rect.midtop = self.rect.midtop
        self.game_over_img_rect.y += 40

    def check_buttons(self, mouse_pos):
        if self.main_menu_button.check_button(mouse_pos):
            self.stats.set_active_screen(game_active=True)
        elif self.quit_button.check_button(mouse_pos):
            self.stats.set_active_screen(main_menu=True)

    def update(self):
        self.check_base_events(self.check_buttons)
        self.fill(self.background_color, self.rect)
        self.blit(self.game_over_img, self.game_over_img_rect)
        self.main_menu_button.blitme()
        self.quit_button.blitme()
