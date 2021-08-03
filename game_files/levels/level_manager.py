from .test_level import TestLevel


class LevelManager:
    """
    This class will manage the
    loading, destorying, and returning of the level objects.
    """

    def __init__(
        self, screen_dim: tuple, settings: object, stats: object, game_sound: object
    ):
        self.width, self.height = screen_dim
        self.settings = settings
        self.stats = stats
        self.game_sound = game_sound
        self.active_level = None

    def load_test_level(self):
        self.active_level = TestLevel(
            self.settings.screen_width,
            self.settings.screen_height,
            self.settings,
            self.stats,
            self.game_sound,
        )