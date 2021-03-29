import pygame.font
from pygame import Surface
from .screen_colors import ScreenColors


class Button(Surface):
    """ create a button """

    def __init__(self, surface, button_text: str):
        """ initialize button settings """
        self.width, self.height = 150, 50
        super(Button, self).__init__((self.width, self.height))
        colors = ScreenColors()
        self.surface = surface
        self.button_color = colors.button_color
        self.text_color = colors.text_color
        # coords to set button to middle of screen
        self.button_mid_pos_x = (
            surface.width/2)-(self.width/2)
        self.button_mid_pos_y = (surface.height/3)*2

        # build the button rect and set it's position
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.x, self.rect.y = self.button_mid_pos_x, self.button_mid_pos_y

        self._prep_text(button_text)

        self.fill(self.button_color)

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

    def _prep_text(self, text: str):
        """ prep the text to be rendered in the button """
        font = pygame.font.SysFont(None, 40, bold=True)
        self.msg_image = font.render(
            text, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def blitme(self):
        self.surface.blit(self, self.rect)
        self.surface.blit(self.msg_image, self.msg_image_rect)
