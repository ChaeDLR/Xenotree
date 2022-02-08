from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP

from game_files import ScreenBase
from .settings_screens.sound_settings import SoundSettings
from .settings_screens.keybindings_settings import KeybindSettings


class SettingsMenu(ScreenBase):
    """
    Settings menu
    Allow user to adjust sound volume
    """

    def __init__(self):
        super().__init__()

        self.screen_rows = self.rect.height / 6
        self.screen_columns = self.rect.width / 6

        self.active_settings_screen = "settings"

        self.sound_screen = SoundSettings(self.set_main_screen, self.image)
        self.keybind_screen = KeybindSettings(self.set_main_screen, self.image)

        self.settings_menu_img, self.settings_menu_img_rect = self.create_text(
            (self.rect.centerx, 60), "SETTINGS"
        )
        self.buttons: list = self.create_buttons(["sound", "keybindings", "back"])

    def __check_button_down(self, mouse_pos):
        """
        Respond to mouse down events
        """
        for button in self.buttons:
            button.check_button(mouse_pos)

    def __check_button_up(self, mouse_pos):
        """
        respond to mouse up events
        """
        for button in self.buttons:
            if button.check_button(mouse_pos, True):
                    if button.name == "sound":
                        self.active_settings_screen = "sound"
                    elif button.name == "keybindings":
                        self.active_settings_screen = "key_bindings"
                    elif button.name == "back":
                        ScreenBase.change_screen = True
                        ScreenBase.current_screen_key = "main_menu"
            else:
                for button in self.buttons:
                    button.reset_alpha()

    def set_main_screen(self):
        """
        set the screen to the main settings screen
        """
        self.active_settings_screen = "settings"

    def check_events(self, event):
        if self.active_settings_screen == "sound":
            self.sound_screen.check_events(event)
        elif self.active_settings_screen == "key_bindings":
            self.keybind_screen.check_events(event)
        elif event.type == MOUSEBUTTONDOWN:
            self.__check_button_down(event.pos)
        elif event.type == MOUSEBUTTONUP:
            self.__check_button_up(event.pos)

    def update(self):
        self.image.fill(self.background_color, self.rect)
        if self.active_settings_screen == "settings":
            self.image.blit(self.settings_menu_img, self.settings_menu_img_rect)
            self.image.blits([(button.image, button.rect) for button in self.buttons])

        elif self.active_settings_screen == "sound":
            self.sound_screen.update()

        elif self.active_settings_screen == "key_bindings":
            self.keybind_screen.update()
