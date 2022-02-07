import os
import pygame

from typing import Callable
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from game_files import ScreenBase

from ..button import Button
from ....asset_manager import AssetManager


class SoundSettings(ScreenBase):
    def __init__(
        self,
        back: Callable,
        screen: pygame.Surface,
    ):
        super().__init__()
        self.main_screen = screen

        # function to return to main settings screen
        self.back_func = back

        self.music_plus_pressed, self.music_minus_pressed = False, False
        self.effects_plus_pressed, self.effects_minus_pressed = False, False

        self.sound_menu_img, self.sound_menu_img_rect = self.create_text(
            (self.rect.centerx, 60), "SOUND"
        )

        inc_images: list = AssetManager.cut_image(
            os.path.join(os.getcwd(), "../images/inc_icons.png"),
            (2, 2),
            (24, 24),
            (30, 25, 10, 10),
        )

        # scale all of the images
        inc_images = list(
            map(
                pygame.transform.scale,
                [si.image for si in inc_images],
                [(24, 24) for _ in range(len(inc_images))],
            )
        )

        self.__load_images()
        self.__load_options_text()
        self.buttons: list = self.__load_buttons()

    def __load_images(self):
        """
        load minus.png and plus.png
        from assets folder and set positions
        """
        path = os.path.dirname(__file__)
        self.__load_music_images(path)
        self.__load_effects_images(path)
        self.__set_image_position()

    def __load_effects_images(self, path: str):
        """Grab +/- images from their folders and load them as images
        that will change the effects volume when pressed
        """
        self.effects_plus_image = pygame.image.load(
            os.path.join(path, "../menu_assets/plus.png")
        )
        self.effects_plus_filled_image = pygame.image.load(
            os.path.join(path, "../menu_assets/plus_filled.png")
        )
        self.effects_minus_image = pygame.image.load(
            os.path.join(path, "../menu_assets/minus.png")
        )
        self.effects_minus_filled_image = pygame.image.load(
            os.path.join(path, "../menu_assets/minus_filled.png")
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

    def __load_music_images(self, path: str):
        """Grab +/- images from their folders and load them as images
        that will change the music volume when pressed
        """
        self.music_plus_image = pygame.image.load(
            os.path.join(path, "../menu_assets/plus.png")
        )
        self.music_plus_filled_image = pygame.image.load(
            os.path.join(path, "../menu_assets/plus_filled.png")
        )
        self.music_minus_image = pygame.image.load(
            os.path.join(path, "../menu_assets/minus.png")
        )
        self.music_minus_filled_image = pygame.image.load(
            os.path.join(path, "../menu_assets/minus_filled.png")
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

    def __set_image_position(self):
        """Set +/- image positions"""
        self.music_plus_image_rect.y = (self.screen_rows * 2.5) + 16
        self.music_minus_image_rect.y = (self.screen_rows * 2.5) + 32

        self.music_plus_image_rect.x = self.screen_columns * 3.4
        self.music_minus_image_rect.x = self.screen_columns * 3.4

        self.effects_plus_image_rect.y = (self.screen_rows * 3) + 16
        self.effects_minus_image_rect.y = (self.screen_rows * 3) + 32

        self.effects_plus_image_rect.x = self.screen_columns * 3.4
        self.effects_minus_image_rect.x = self.screen_columns * 3.4

    def __load_buttons(self) -> list:
        """
        Create apply and back buttons
        """
        self.back_button = Button(self.main_screen, "Back")
        self.back_button.set_position(self.screen_columns, self.screen_rows * 5)
        self.save_button = Button(self.main_screen, "Save")
        self.save_button.set_position(self.screen_columns * 4, self.screen_rows * 5)
        return [self.back_button, self.save_button]

    def __load_options_text(self):
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

    def __update_signs(self):
        """
        Update plus and minus signs
        """
        self.__update_music_signs()
        self.__update_effects_signs()

    def __update_effects_signs(self):
        if self.effects_plus_pressed:
            self.main_screen.blit(self.effects_plus_image, self.effects_plus_image_rect)
            self.effects_plus_pressed = False
        else:
            self.main_screen.blit(
                self.effects_plus_filled_image, self.effects_plus_image_rect
            )

        if self.effects_minus_pressed:
            self.main_screen.blit(
                self.effects_minus_image, self.effects_minus_image_rect
            )
            self.effects_minus_pressed = False
        else:
            self.main_screen.blit(
                self.effects_minus_filled_image, self.effects_minus_image_rect
            )

    def __update_music_signs(self):
        if self.music_plus_pressed:
            self.main_screen.blit(self.music_plus_image, self.music_plus_image_rect)
            self.music_plus_pressed = False
        else:
            self.main_screen.blit(
                self.music_plus_filled_image, self.music_plus_image_rect
            )

        if self.music_minus_pressed:
            self.main_screen.blit(self.music_minus_image, self.music_minus_image_rect)
            self.music_minus_pressed = False
        else:
            self.main_screen.blit(
                self.music_minus_filled_image, self.music_minus_image_rect
            )

    def __check_button_down(self, mouse_pos):
        """
        Respond to mouse down events
        """
        self.back_button.check_button(mouse_pos)
        self.save_button.check_button(mouse_pos)

    def __check_button_up(self, mouse_pos):
        """
        Respond to mouse up events
        """
        # If the music plus rect is pressed
        if self.music_plus_image_rect.collidepoint(mouse_pos):
            self.music_plus_pressed = True
            self.sound.increase_music_volume()
            self.update_music_volume_string()
        # If the music minus rect is pressed
        elif self.music_minus_image_rect.collidepoint(mouse_pos):
            self.music_minus_pressed = True
            self.sound.decrease_music_volume()
            self.update_music_volume_string()
        # If effects plus rect
        elif self.effects_plus_image_rect.collidepoint(mouse_pos):
            self.effects_plus_pressed = True
            self.sound.increase_effects_volume()
            self.update_effects_volume_string()
        # If effects minus rect
        elif self.effects_minus_image_rect.collidepoint(mouse_pos):
            self.effects_minus_pressed = True
            self.sound.decrease_effects_volume()
            self.update_effects_volume_string()
        # If back button is pressed go to the main menu
        elif self.back_button.check_button(mouse_pos, True):
            self.back_func()
        # If save button is pressed call save_volumes() to save the volume settings
        elif self.save_button.check_button(mouse_pos, True):
            self.sound.save_volumes()
        else:
            for button in self.buttons:
                button.reset_alpha()

    def check_events(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.__check_button_down(event.pos)
        elif event.type == MOUSEBUTTONUP:
            self.__check_button_up(event.pos)

    def update_music_volume_string(self):
        music_volume_string = f"Music volume: {str(self.sound.music_volume)[2:]}"
        music_font = pygame.font.SysFont(None, 38)
        self.music_volume_image = music_font.render(
            music_volume_string, True, self.text_color, self.background_color
        )

    def update_effects_volume_string(self):
        effects_volume_string = f"Effects volume: {str(self.sound.effects_volume)[2:]}"
        effects_font = pygame.font.SysFont(None, 38)
        self.effects_volume_image = effects_font.render(
            effects_volume_string, True, self.text_color, self.background_color
        )

    def update(self):
        self.__update_signs()
        self.main_screen.blit(self.sound_menu_img, self.sound_menu_img_rect)
        self.main_screen.blit(self.music_volume_image, self.music_volume_image_rect)
        self.main_screen.blit(self.effects_volume_image, self.effects_volume_image_rect)
        self.back_button.blitme()
        self.save_button.blitme()
