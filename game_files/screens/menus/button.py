import pygame

from ..screen_colors import ScreenColors
from ...asset_manager import AssetManager


class Button(pygame.Surface):
    def __init__(
        self,
        surface: object,
        button_text: str,
        size: tuple = (150, 50),
        font_size: int = 40,
        name: str = None,
    ):
        """initialize button settings"""
        super().__init__(size)
        self.width, self.height = size
        self.surface = surface
        self.text = button_text
        self.font_size = font_size
        self.button_color = ScreenColors.button_color()
        self.text_color = ScreenColors.text_color()
        self.name = name if name else button_text
        # coords to set button to middle of screen
        self.button_mid_pos_x = (surface.get_width() / 2) - (self.width / 2)
        self.button_mid_pos_y = (surface.get_height() / 3) * 2

        self.resize((self.width, self.height))
        self.set_text(button_text, font_size)
        self.fill(self.button_color)

    def resize(self, w_h: tuple):
        """
        Resize the buttone given the width, height tuple
        """
        self.rect = pygame.Rect(0, 0, w_h[0], w_h[1])
        self.rect.x, self.rect.y = self.button_mid_pos_x, self.button_mid_pos_y

    def check_button(self, mouse_pos, mouse_up: bool = False) -> bool:
        """check for button collision"""
        if self.rect.collidepoint(mouse_pos):
            if mouse_up:
                self.reset_alpha()
                return True
            self.set_alpha(25)
            self.msg_image.set_alpha(25)

    def reset_alpha(self):
        self.set_alpha(255)
        self.msg_image.set_alpha(255)

    def set_position(self, x_pos=None, y_pos=None):
        """Set the position of the button"""
        if x_pos:
            self.rect.x = x_pos
        if y_pos:
            self.rect.y = y_pos
        self.msg_image_rect.center = self.rect.center

    def clear_text(self):
        self.msg_image.fill(self.button_color)

    def set_text(self, txt: str, fontsize: int = None):
        self.text = txt
        if fontsize:
            self.font_size = fontsize
            self.text_font = pygame.font.SysFont(None, self.font_size, bold=True)
        self.msg_image = self.text_font.render(self.text, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def restore_text(self):
        """
        Display stored text value to the button surface
        """
        self.msg_image = self.text_font.render(self.text, True, self.text_color)

    def blitme(self):
        self.surface.blit(self, self.rect)
        self.surface.blit(self.msg_image, self.msg_image_rect)


class ImageButton:
    def __init__(self, image: pygame.Surface, **kwargs) -> None:
        self.image, self.rect = AssetManager.baptize_image(image)
        self.mask = pygame.mask.from_surface(self.image)

        for key in kwargs:
            try:
                self.__setattr__(key, kwargs[key])
            except ValueError:
                print(f"Failed to set attr {key}: {kwargs[key]}")

    def set_position(self, x_pos=None, y_pos=None):
        """Set the position of the button"""
        if x_pos:
            self.rect.x = x_pos
        if y_pos:
            self.rect.y = y_pos

    def reset_alpha(self) -> None:
        self.image.set_alpha(255)

    def check_button(self, mouse_pos, mouse_up: bool = False) -> bool:
        """check for button collision"""
        if self.rect.collidepoint(mouse_pos):
            if mouse_up:
                self.reset_alpha()
                return True
            self.image.set_alpha(25)
