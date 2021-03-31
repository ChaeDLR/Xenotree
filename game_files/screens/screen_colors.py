class ScreenColors:
    """
    This class holds the color scheme for the game menu
    """

    def __init__(self) -> None:
        # color theme from https://color.adobe.com/color%20theme_PWV11YQrPHs-color-theme-17351237
        self.__dark_blue = (26, 26, 38)
        self.__dark_brown = (72, 65, 46)
        self.__med_grey = (191, 180, 159)
        self.__black = (18, 16, 21)
        self.__blu = (60, 94, 130)

    @property
    def level_one_bg(self) -> tuple:
        return self.__dark_blue

    @property
    def button_color(self) -> tuple:
        return self.__blu

    @property
    def bg_color(self) -> tuple:
        return self.__black

    @property
    def text_color(self) -> tuple:
        return self.__med_grey
