import pygame.font
from pygame import Surface
from .button import Button
from .screen_colors import ScreenColors


class Game_Over(Surface):
    def __init__(self, width: int, height: int):
        super(Game_Over, self).__init__((width, height))
        colors = ScreenColors()
        self.background_color = colors.bg_color
        self.text_color = colors.text_color
        self.rect = pygame.Rect(0, 0, width, height)

        self.width, self.height = width, height

        self._load_buttons()
        self._load_text()

    def _load_buttons(self):
        self.play_button = Button(self, "Play")
        self.quit_button = Button(self, "Quit")

        self.play_button.set_position(y_pos=self.rect.height / 2)

    def _load_text(self):
        font = pygame.font.SysFont(None, 50, bold=True)
        self.game_over_img = font.render(
            "Game Over", True, self.text_color, self.background_color
        )
        self.game_over_img_rect = self.game_over_img.get_rect()
        self.game_over_img_rect.midtop = self.rect.midtop
        self.game_over_img_rect.y += 40

    def check_buttons(self, mouse_pos):
        if self.play_button.check_button(mouse_pos):
            return 1
        elif self.quit_button.check_button(mouse_pos):
            return 2
        return -1

    def update(self):

        self.fill(self.background_color, self.rect)
        self.blit(self.game_over_img, self.game_over_img_rect)
        self.play_button.blitme()
        self.quit_button.blitme()
