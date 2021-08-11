from pygame import font, Surface

from game_files import Settings
from game_files import GameSound
from game_files import ScreenColors
from ..asset_manager import AssetManager


class ScreenBase:

    change_screen: bool = False
    current_screen_key: str = "main_menu"
    width: int = Settings.screen_width
    height: int = Settings.screen_height

    def __init__(self, flags: int = 0) -> None:
        self.settings = Settings()
        self.sound = GameSound()
        self.image = Surface((self.width, self.height), flags=flags)
        self.rect = self.image.get_rect()

        self.screen_columns = self.rect.width / 6
        self.screen_rows = self.rect.height / 6

        self.background_color: tuple = ScreenColors.bg_color()
        self.text_color: tuple = ScreenColors.text_color()

        self.projectile_assets: dict = AssetManager.get_projectile_assets()
        self.turret_assets: dict = AssetManager.get_turret_assets()
        self.player_assets: dict = AssetManager.get_player_images()
        self.background_assets: dict = AssetManager.get_background_assets(
            self.rect.size
        )
        self.env_assets: dict = AssetManager.get_env_assets()

    def create_text(
        self,
        x_y: tuple,
        text: str,
        textsize: int = 56,
        boldtext: bool = True,
    ) -> tuple:
        """
        x_y: tuple -> positions using center of the rect
        Tuple -> (text_img, text_rect)
        """
        text_font = font.SysFont(None, textsize, bold=boldtext)
        text_img = text_font.render(text, True, self.text_color)
        text_rect = text_img.get_rect()
        text_rect.center = x_y
        return (text_img, text_rect)
