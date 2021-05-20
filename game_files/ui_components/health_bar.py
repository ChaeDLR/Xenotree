from pygame import Surface

class HealthBar(Surface):

    def __init__(self, coords: tuple):
        """
        Player health bar surface object
        """
        super().__init__((100, 25))
        self.x, self.y = coords

        self.__update_health()

    def __create_bar_bg(self):
        """
        Create the bar background
        """
        self.fill((10, 10, 10))
        self.base_img_rect = self.get_rect()
        self.base_img_rect.x, self.base_img_rect.y = self.x, self.y

    def __update_health(self, health: int=100) -> None:
        """
        Create the heal bars base image
        black rect
        """
        self.__create_bar_bg()

        healthbar_img = Surface(
            (health-20, self.base_img_rect.height-10)
            )
        healthbar_rect = healthbar_img.get_rect()
        healthbar_rect.x, healthbar_rect.y = self.base_img_rect.x, self.base_img_rect.y-5
        healthbar_img.fill((192, 16, 16))

        self.blit(healthbar_img, healthbar_rect)

        self.rect = self.base_img_rect
    
    def update(self, health_percentage: int):
        """
        Take the players current health percentage 
        to the nearest whole number
        """
        self.__update_health(health_percentage)
        