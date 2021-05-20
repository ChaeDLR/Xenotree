from pygame import Surface, transform
import pygame

class ActiveWeapon:

    def __init__(self, coords: tuple, assets: dict):
        self.x = float(coords[0])
        self.y = float(coords[1])
        self.starting_y = coords[1]
        
        self.assets = assets
        self.moving_up = True

        self.__load_weapon_bar()

    def __load_weapon_bar(self):
        """
        Initial loading of the weapon ui element
        """
        fb_img = self.assets["red_fb_idle_imgs"][0]
        fb_img = transform.scale(fb_img, (17, 25))
        fb_rect = fb_img.get_rect()
        fb_rect.x, fb_rect.y = self.x, self.y

        self.image = fb_img
        self.rect = fb_rect

    def update(self, active_fireball: str=None):
        """
        'red', 'blue', 'purple'
        """
        if self.moving_up:
            self.y -= 0.2
            self.rect.y = self.y
            if self.rect.y <= 5:
                self.moving_up = False
        
        else:
            self.y += 0.2
            self.rect.y = self.y
            if self.rect.y >= self.starting_y:
                self.moving_up = True
