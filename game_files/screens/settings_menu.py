import pygame.font
import pygame.transform
import os
from .button import Button
from .menu_base import MenuBase
from .settings_screens.sound_settings import SoundSettings
from .settings_screens.keybindings_settings import KeybindSettings


class SettingsMenu(MenuBase):
    """
    Settings menu
    Allow user to adjust sound volume
    """

    def __init__(self, w_h: tuple, stats: object, settings: object, game_sound: object):
        super().__init__(w_h, stats, settings)

        self.screen_rows = w_h[1] / 6
        self.screen_columns = w_h[0] / 6

        self.game_sound = game_sound
        self.settings = settings

        self.active_settings_screen = "settings"

        self.sound_screen = SoundSettings(w_h, stats, settings, game_sound, self.set_main_screen, self)
        self.keybind_screen = KeybindSettings(w_h, stats, settings, self.set_main_screen, self)

        self.__load_title()
        self.__load_buttons()
    
    def __load_buttons(self):
        """
        Create buttons that will take the user to the selected settings screen
        """
        self.sound_button = Button(self, "Sound")
        self.sound_button.set_position(
            self.rect.centerx-(self.sound_button.width/2), 
            self.settings_menu_img_rect.y + 100
            )

        self.keybindings_button = Button(self, "Key bindings", font_size=29)
        self.keybindings_button.resize(
            (self.keybindings_button.width, self.keybindings_button.height)
            )
        self.keybindings_button.set_position(
            self.rect.centerx-(self.keybindings_button.width/2), 
            self.sound_button.rect.y + 100
            )
        
        self.back_button = Button(self, "Back")
        self.back_button.set_position(
            self.rect.centerx-(self.back_button.width/2), 
            self.keybindings_button.rect.y + 100
            )

    def __load_title(self):
        """ load settings title """
        font = pygame.font.SysFont(None, 56, bold=True)
        self.settings_menu_img = font.render(
            "SETTINGS", True, self.text_color, self.background_color
        )
        self.settings_menu_img_rect = self.settings_menu_img.get_rect()
        self.settings_menu_img_rect.midtop = self.rect.midtop
        self.settings_menu_img_rect.y += 60

    def check_button_down(self, mouse_pos):
        """
        Respond to mouse down events
        """
        self.sound_button.check_button(mouse_pos)
        self.keybindings_button.check_button(mouse_pos)
        self.back_button.check_button(mouse_pos)
    
    def check_button_up(self, mouse_pos):
        """
        respond to mouse up events
        """
        if self.sound_button.check_button(mouse_pos, True):
            self.active_settings_screen = "sound"
        elif self.keybindings_button.check_button(mouse_pos, True):
            self.active_settings_screen = "key_bindings"
        elif self.back_button.check_button(mouse_pos, True):
            self.stats.set_active_screen(main_menu=True)
    
    def set_main_screen(self):
        """
        set the screen to the main settings screen
        """
        self.active_settings_screen = "settings"

    def update(self):
        self.fill(self.background_color, self.rect)
        if self.active_settings_screen == "settings":
            self.check_base_events(self.check_button_down, self.check_button_up)
            self.blit(self.settings_menu_img, self.settings_menu_img_rect)
            self.sound_button.blitme()
            self.keybindings_button.blitme()
            self.back_button.blitme()

        elif self.active_settings_screen == "sound":
            self.check_base_events(self.sound_screen.check_button_down, self.sound_screen.check_button_up)
            self.sound_screen.update()

        elif self.active_settings_screen == "key_bindings":
            self.keybind_screen.update(
                self.check_base_events(
                    self.keybind_screen.check_button_down, 
                    self.keybind_screen.check_button_up
                    )
                )
