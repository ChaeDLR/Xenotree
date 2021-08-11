from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from game_files import ScreenBase
from .button import Button
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

        self.buttons: list = self.__load_buttons()

    def __load_buttons(self):
        """
        Create buttons that will take the user to the selected settings screen
        """
        self.sound_button = Button(self.image, "Sound")
        self.sound_button.set_position(
            self.rect.centerx - (self.sound_button.width / 2),
            self.settings_menu_img_rect.y + 100,
        )

        self.keybindings_button = Button(self.image, "Key bindings", font_size=29)
        self.keybindings_button.resize(
            (self.keybindings_button.width, self.keybindings_button.height)
        )
        self.keybindings_button.set_position(
            self.rect.centerx - (self.keybindings_button.width / 2),
            self.sound_button.rect.y + 100,
        )

        self.back_button = Button(self.image, "Back")
        self.back_button.set_position(
            self.rect.centerx - (self.back_button.width / 2),
            self.keybindings_button.rect.y + 100,
        )
        return [self.sound_button, self.keybindings_button, self.back_button]

    def __check_button_down(self, mouse_pos):
        """
        Respond to mouse down events
        """
        self.sound_button.check_button(mouse_pos)
        self.keybindings_button.check_button(mouse_pos)
        self.back_button.check_button(mouse_pos)

    def __check_button_up(self, mouse_pos):
        """
        respond to mouse up events
        """
        if self.sound_button.check_button(mouse_pos, True):
            self.active_settings_screen = "sound"
        elif self.keybindings_button.check_button(mouse_pos, True):
            self.active_settings_screen = "key_bindings"
        elif self.back_button.check_button(mouse_pos, True):
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
            self.sound_button.blitme()
            self.keybindings_button.blitme()
            self.back_button.blitme()

        elif self.active_settings_screen == "sound":
            self.sound_screen.update()

        elif self.active_settings_screen == "key_bindings":
            self.keybind_screen.update()
