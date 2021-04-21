import pygame.font
from pygame import Surface
from .screen_colors import ScreenColors


class Button(Surface):
    """ create a button """

    def __init__(self, surface: object, button_text: str):
        """ initialize button settings """
        self.width, self.height = 150, 50
        super(Button, self).__init__((self.width, self.height))
        colors = ScreenColors()
        self.surface = surface
        self.button_color = colors.button_color
        self.text_color = colors.text_color
        self.text = button_text
        # coords to set button to middle of screen
        self.button_mid_pos_x = (surface.width / 2) - (self.width / 2)
        self.button_mid_pos_y = (surface.height / 3) * 2

        # build the button rect and text. Set it's position
        self.resize((self.width, self.height))

        self.fill(self.button_color)

    def resize(self, w_h: tuple, font_size: int = 40):
        """
        Resize the buttone given the width, height tuple
        """
        self.rect = pygame.Rect(0, 0, w_h[0], w_h[1])
        self.rect.x, self.rect.y = self.button_mid_pos_x, self.button_mid_pos_y
        self._prep_text(font_size)

    def check_button(self, mouse_pos):
        """ check for button collision """
        if self.rect.collidepoint(mouse_pos):
            return True
        return False

    def set_position(self, x_pos=None, y_pos=None):
        """ Set the position of the button """
        if x_pos:
            self.rect.x = x_pos
        if y_pos:
            self.rect.y = y_pos

        self.msg_image_rect.center = self.rect.center

    def _prep_text(self, fontsize: int):
        """ prep the text to be rendered in the button """
        font = pygame.font.SysFont(None, fontsize, bold=True)
        self.msg_image = font.render(
            self.text, True, self.text_color, self.button_color
        )
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def blitme(self):
        self.surface.blit(self, self.rect)
        self.surface.blit(self.msg_image, self.msg_image_rect)
