import pygame.font
import pygame.transform
import os
from .button import Button
from .menu_base import MenuBase


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

        self.music_plus_pressed, self.music_minus_pressed = False, False
        self.effects_plus_pressed, self.effects_minus_pressed = False, False

        self._load_images()
        self._load_title()
        self._load_options_text()
        self._load_buttons()

    def update_music_volume_string(self):
        music_volume_string = f"Music volume: {str(self.game_sound.music_volume)[2:]}"
        font = pygame.font.SysFont(None, 38)
        self.music_volume_image = font.render(
            music_volume_string, True, self.text_color, self.background_color
        )

    def update_effects_volume_string(self):
        effects_volume_string = (
            f"Effects volume: {str(self.game_sound.effects_volume)[2:]}"
        )
        font = pygame.font.SysFont(None, 38)
        self.effects_volume_image = font.render(
            effects_volume_string, True, self.text_color, self.background_color
        )

    def _load_buttons(self):
        """
        Create apply and back buttons
        """
        self.back_button = Button(self, "Back")
        self.back_button.set_position(self.screen_columns, self.screen_rows * 5)
        self.save_button = Button(self, "Save")
        self.save_button.set_position(self.screen_columns * 4, self.screen_rows * 5)

    def _load_options_text(self):
        """
        Create available options text
        Set position
        """
        self.update_music_volume_string()
        self.update_effects_volume_string()
        self.music_volume_image_rect = self.music_volume_image.get_rect()
        self.music_volume_image_rect.y = (self.screen_rows * 2.5) + 20
        self.music_volume_image_rect.x = self.screen_rows * 2

        self.effects_volume_image_rect = self.effects_volume_image.get_rect()
        self.effects_volume_image_rect.y = (self.screen_rows * 3) + 20
        self.effects_volume_image_rect.x = self.screen_rows * 2

    def _load_images(self):
        """
        load minus.png and plus.png
        from assets folder and set positions
        """
        path = os.path.dirname(__file__)
        self._load_music_images(path)
        self._load_effects_images(path)
        self._set_image_position()

    def _load_effects_images(self, path: str):
        """Grab +/- images from their folders and load them as images
        that will change the effects volume when pressed
        """
        self.effects_plus_image = pygame.image.load(
            os.path.join(path, "menu_assets/plus.png")
        )
        self.effects_plus_filled_image = pygame.image.load(
            os.path.join(path, "menu_assets/plus_filled.png")
        )
        self.effects_minus_image = pygame.image.load(
            os.path.join(path, "menu_assets/minus.png")
        )
        self.effects_minus_filled_image = pygame.image.load(
            os.path.join(path, "menu_assets/minus_filled.png")
        )

        self.effects_plus_image = pygame.transform.scale(
            self.effects_plus_image, (16, 16)
        )
        self.effects_plus_filled_image = pygame.transform.scale(
            self.effects_plus_filled_image, (16, 16)
        )
        self.effects_minus_image = pygame.transform.scale(
            self.effects_minus_image, (16, 16)
        )
        self.effects_minus_filled_image = pygame.transform.scale(
            self.effects_minus_filled_image, (16, 16)
        )

        self.effects_plus_image_rect = self.effects_plus_image.get_rect()
        self.effects_minus_image_rect = self.effects_minus_image.get_rect()

    def _load_music_images(self, path: str):
        """Grab +/- images from their folders and load them as images
        that will change the music volume when pressed
        """
        self.music_plus_image = pygame.image.load(
            os.path.join(path, "menu_assets/plus.png")
        )
        self.music_plus_filled_image = pygame.image.load(
            os.path.join(path, "menu_assets/plus_filled.png")
        )
        self.music_minus_image = pygame.image.load(
            os.path.join(path, "menu_assets/minus.png")
        )
        self.music_minus_filled_image = pygame.image.load(
            os.path.join(path, "menu_assets/minus_filled.png")
        )

        self.music_plus_image = pygame.transform.scale(self.music_plus_image, (16, 16))
        self.music_plus_filled_image = pygame.transform.scale(
            self.music_plus_filled_image, (16, 16)
        )
        self.music_minus_image = pygame.transform.scale(
            self.music_minus_image, (16, 16)
        )
        self.music_minus_filled_image = pygame.transform.scale(
            self.music_minus_filled_image, (16, 16)
        )

        self.music_plus_image_rect = self.music_plus_image.get_rect()
        self.music_minus_image_rect = self.music_minus_image.get_rect()

    def _set_image_position(self):
        """ Set +/- image positions """
        self.music_plus_image_rect.y = (self.screen_rows * 2.5) + 16
        self.music_minus_image_rect.y = (self.screen_rows * 2.5) + 32

        self.music_plus_image_rect.x = self.screen_columns * 3.4
        self.music_minus_image_rect.x = self.screen_columns * 3.4

        self.effects_plus_image_rect.y = (self.screen_rows * 3) + 16
        self.effects_minus_image_rect.y = (self.screen_rows * 3) + 32

        self.effects_plus_image_rect.x = self.screen_columns * 3.4
        self.effects_minus_image_rect.x = self.screen_columns * 3.4

    def _load_title(self):
        """ load settings title """
        font = pygame.font.SysFont(None, 56, bold=True)
        self.settings_menu_img = font.render(
            "SETTINGS", True, self.text_color, self.background_color
        )
        self.settings_menu_img_rect = self.settings_menu_img.get_rect()
        self.settings_menu_img_rect.midtop = self.rect.midtop
        self.settings_menu_img_rect.y += 60

    def _update_signs(self):
        """
        Update plus and minus signs
        """
        self._update_music_signs()
        self._update_effects_signs()

    def _update_effects_signs(self):
        if self.effects_plus_pressed:
            self.blit(self.effects_plus_image, self.effects_plus_image_rect)
            self.effects_plus_pressed = False
        else:
            self.blit(self.effects_plus_filled_image, self.effects_plus_image_rect)

        if self.effects_minus_pressed:
            self.blit(self.effects_minus_image, self.effects_minus_image_rect)
            self.effects_minus_pressed = False
        else:
            self.blit(self.effects_minus_filled_image, self.effects_minus_image_rect)

    def _update_music_signs(self):
        if self.music_plus_pressed:
            self.blit(self.music_plus_image, self.music_plus_image_rect)
            self.music_plus_pressed = False
        else:
            self.blit(self.music_plus_filled_image, self.music_plus_image_rect)

        if self.music_minus_pressed:
            self.blit(self.music_minus_image, self.music_minus_image_rect)
            self.music_minus_pressed = False
        else:
            self.blit(self.music_minus_filled_image, self.music_minus_image_rect)

    def check_buttons(self, mouse_pos):
        """
        Respond to mouse down events
        """
        # If the music plus rect is pressed
        if self.music_plus_image_rect.collidepoint(mouse_pos):
            self.music_plus_pressed = True
            self.game_sound.increase_music_volume()
            self.update_music_volume_string()
        # If the music minus rect is pressed
        elif self.music_minus_image_rect.collidepoint(mouse_pos):
            self.music_minus_pressed = True
            self.game_sound.decrease_music_volume()
            self.update_music_volume_string()
        # If effects plus rect
        elif self.effects_plus_image_rect.collidepoint(mouse_pos):
            self.effects_plus_pressed = True
            self.game_sound.increase_effects_volume()
            self.update_effects_volume_string()
        # If effects minus rect
        elif self.effects_minus_image_rect.collidepoint(mouse_pos):
            self.effects_minus_pressed = True
            self.game_sound.decrease_effects_volume()
            self.update_effects_volume_string()
        # If back button is pressed go to the main menu
        elif self.back_button.check_button(mouse_pos):
            self.stats.set_active_screen(main_menu=True)
        # If save button is pressed call save_volumes() to save the volume settings
        elif self.save_button.check_button(mouse_pos):
            self.game_sound.save_volumes()

    def update(self):
        self.check_base_events(self.check_buttons)
        self.fill(self.background_color, self.rect)
        self.blit(self.settings_menu_img, self.settings_menu_img_rect)
        self._update_signs()
        self.blit(self.music_volume_image, self.music_volume_image_rect)
        self.blit(self.effects_volume_image, self.effects_volume_image_rect)
        self.back_button.blitme()
        self.save_button.blitme()
