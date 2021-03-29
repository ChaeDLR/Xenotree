from .menu_base import MenuBase
from .button import Button


class MainMenu(MenuBase):
    """
    Initial screen that allows user options to
    Play the game, Enter settings menu, or Quit the game
    """

    def __init__(self, width: int, height: int):
        super().__init__(width, height)

        self._load_title()
        self._load_buttons()

    def _load_buttons(self):
        button_row = self.height / 6
        self.play_button = Button(self, "Play")
        self.quit_button = Button(self, "Quit")
        self.settings_button = Button(self, "Settings")

        self.play_button.set_position(y_pos=button_row * 2)
        self.settings_button.set_position(y_pos=button_row * 3)
        self.quit_button.set_position(y_pos=button_row * 4)

    def _load_title(self):
        """ load game title """
        self.main_menu_img = self.font.render(
            "XENOTREE", True, self.text_color, self.background_color
        )
        self.main_menu_img_rect = self.main_menu_img.get_rect()
        self.main_menu_img_rect.midtop = self.rect.midtop
        self.main_menu_img_rect.y += 60

    def check_buttons(self, mouse_pos):
        """
        Return 1 if play button clicked
        Return 2 if quit button clicked
        """
        if self.play_button.check_button(mouse_pos):
            return 1
        elif self.quit_button.check_button(mouse_pos):
            return 2
        elif self.settings_button.check_button(mouse_pos):
            return 3
        return -1

    def update(self):
        self.fill(self.background_color, self.rect)
        self.blit(self.main_menu_img, self.main_menu_img_rect)
        self.play_button.blitme()
        self.settings_button.blitme()
        self.quit_button.blitme()
