import sys
from .menu_base import MenuBase
from .button import Button


class MainMenu(MenuBase):
    """
    Initial screen that allows user options to
    Play the game, Enter settings menu, or Quit the game
    """

    def __init__(
        self, w_h: tuple, stats: object, settings: object, level_manager: object
    ):
        super().__init__((w_h[0], w_h[1]), stats, settings)

        self.level_manager = level_manager
        self.__load_title()
        self.buttons: list = self.__load_buttons()

    def __load_buttons(self):
        button_row = self.height / 6
        self.play_button = Button(self, "Play")
        self.quit_button = Button(self, "Quit")
        self.settings_button = Button(self, "Settings")

        self.play_button.set_position(y_pos=button_row * 2)
        self.settings_button.set_position(y_pos=button_row * 3)
        self.quit_button.set_position(y_pos=button_row * 4)
        return [self.play_button, self.quit_button, self.settings_button]

    def __load_title(self):
        """ load game title """
        self.main_menu_img = self.font.render(
            "XENOTREE", True, self.text_color, self.background_color
        )
        self.main_menu_img_rect = self.main_menu_img.get_rect()
        self.main_menu_img_rect.midtop = self.rect.midtop
        self.main_menu_img_rect.y += 60

    def check_button_down(self, mouse_pos):
        """
        Respond to button clicks mouse down events
        """
        self.play_button.check_button(mouse_pos)
        self.quit_button.check_button(mouse_pos)
        self.settings_button.check_button(mouse_pos)

    def check_button_up(self, mouse_pos):
        """
        Respond to button clicks mouse ip events
        """
        if self.play_button.check_button(mouse_pos, True):
            self.start_game()
            self.level_manager.load_test_level()
        elif self.quit_button.check_button(mouse_pos, True):
            sys.exit()
        elif self.settings_button.check_button(mouse_pos, True):
            self.stats.set_active_screen(settings_menu=True)
        else:
            for button in self.buttons:
                button.reset_alpha()

    def update(self):
        self.fill(self.background_color, self.rect)
        self.check_base_events(self.check_button_down, self.check_button_up)
        self.blit(self.main_menu_img, self.main_menu_img_rect)
        self.play_button.blitme()
        self.settings_button.blitme()
        self.quit_button.blitme()
