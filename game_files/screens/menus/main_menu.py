import sys
from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP, mouse, cursors
from game_files import ScreenBase
from .button import Button


class MainMenu(ScreenBase):
    """
    Initial screen that allows user options to
    Play the game, Enter settings menu, or Quit the game
    """

    def __init__(self):
        super().__init__()
        self.main_menu_img, self.main_menu_img_rect = self.create_text(
            (self.rect.centerx, 60), "XENOTREE"
        )

        self.buttons: list = self.__load_buttons()

    def __load_buttons(self) -> list:
        button_row = self.height / 6
        self.play_button = Button(self.image, "Play")
        self.quit_button = Button(self.image, "Quit")
        self.settings_button = Button(self.image, "Settings")

        self.play_button.set_position(y_pos=button_row * 2)
        self.settings_button.set_position(y_pos=button_row * 3)
        self.quit_button.set_position(y_pos=button_row * 4)
        return [self.play_button, self.quit_button, self.settings_button]

    def __start_game(self):
        ScreenBase.change_screen = True
        ScreenBase.current_screen_key = "test_level"
        mouse.set_cursor(cursors.broken_x)

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
            self.__start_game()
        elif self.quit_button.check_button(mouse_pos, True):
            sys.exit()
        elif self.settings_button.check_button(mouse_pos, True):
            ScreenBase.change_screen = True
            ScreenBase.current_screen_key = "settings_menu"
        else:
            for button in self.buttons:
                button.reset_alpha()

    def check_events(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.check_button_down(event.pos)
        elif event.type == MOUSEBUTTONUP:
            self.check_button_up(event.pos)

    def update(self):
        self.image.fill(self.background_color, self.rect)
        self.image.blit(self.main_menu_img, self.main_menu_img_rect)
        self.play_button.blitme()
        self.settings_button.blitme()
        self.quit_button.blitme()
