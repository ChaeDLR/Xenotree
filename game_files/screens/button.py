import pygame
from pygame import Surface
from .screen_colors import ScreenColors


class Button(Surface):
    def __init__(
        self,
        surface: object,
        button_text: str,
        size: tuple = None,
        font_size: int = 40,
        name: str = None,
    ):
        """ initialize button settings """
        if size != None:
            self.width, self.height = size
        else:
            self.width, self.height = 150, 50

        super(Button, self).__init__((self.width, self.height))
        colors = ScreenColors()
        self.surface = surface
        self.button_color = colors.button_color
        self.text_color = colors.text_color
        # coords to set button to middle of screen
        self.button_mid_pos_x = (surface.width / 2) - (self.width / 2)
        self.button_mid_pos_y = (surface.height / 3) * 2

        if font_size:
            self.resize((self.width, self.height))
        else:
            # build the button rect and text. Set it's position
            self.resize((self.width, self.height))
        self.set_text(button_text, font_size)
        if name:
            self.name = name

        self.fill(self.button_color)

    def resize(self, w_h: tuple):
        """
        Resize the buttone given the width, height tuple
        """
        self.rect = pygame.Rect(0, 0, w_h[0], w_h[1])
        self.fill(self.button_color)
        self.rect.x, self.rect.y = self.button_mid_pos_x, self.button_mid_pos_y

    def check_button(self, mouse_pos, mouse_up: bool = False) -> bool:
        """ check for button collision """
        if self.rect.collidepoint(mouse_pos):
            if mouse_up:
                self.reset_alpha()
                return True
            self.set_alpha(25, pygame.RLEACCEL)
            self.msg_image.set_alpha(25, pygame.RLEACCEL)

    def reset_alpha(self):
        self.set_alpha(255, pygame.RLEACCEL)
        self.msg_image.set_alpha(255, pygame.RLEACCEL)
        self.fill(self.button_color)

    def set_position(self, x_pos=None, y_pos=None):
        """ Set the position of the button """
        if x_pos:
            self.rect.x = x_pos
        if y_pos:
            self.rect.y = y_pos

        self.msg_image_rect.center = self.rect.center

    def clear_text(self):
        self.msg_image.fill(self.button_color)

    def set_text(self, txt: str, fontsize: int = 40):
        txt_font = pygame.font.SysFont(None, fontsize, bold=True)
        self.msg_image = txt_font.render(txt, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def blitme(self):
        self.surface.blit(self, self.rect)
        self.surface.blit(self.msg_image, self.msg_image_rect)
