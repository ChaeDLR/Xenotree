class ScreenColors:
    """
    This class holds the color scheme for the game menu
    """
    __dark_blue = (26, 26, 38, 255)
    __dark_brown = (72, 65, 46, 255)
    __med_grey = (191, 180, 159, 255)
    __black = (18, 16, 21, 255)
    __blu = (60, 94, 130, 255)

    @classmethod
    def platform_color(cls) -> tuple:
        return cls.__black

    @classmethod
    def level_one_bg(cls) -> tuple:
        return cls.__dark_blue

    @classmethod
    def button_color(cls) -> tuple:
        return cls.__blu

    @classmethod
    def bg_color(cls) -> tuple:
        return cls.__black

    @classmethod
    def text_color(cls) -> tuple:
        return cls.__med_grey
