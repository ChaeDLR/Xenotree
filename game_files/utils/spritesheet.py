# Code taken from
# https://ehmatthes.github.io/pcc_2e/beyond_pcc/pygame_sprite_sheets/
# made minor changes

import pygame
from pygame import sprite


class SpriteSheet:
    def __init__(self, filename):
        """ load sheet """
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet: {filename}")
            raise SystemExit(e)

    def image_at(self, rectangle, colorkey=None):
        """ Load specific image from a specific rectangle """
        # Loads image from x, y, x+offset, y+offset
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects: list, colorkey=None) -> list:
        """ Load a whole numch of images and return them as a list """
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey=None):
        """ Load a whole strip of images, and return them as a list """
        tups = [
            (rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
            for x in range(image_count)
        ]
        return self.images_at(tups, colorkey)

    def load_grid_images(
        self,
        num_rows: int,
        num_cols: int,
        x_margin: int = 0,
        x_padding: int = 0,
        y_margin: int = 0,
        y_padding: int = 0,
    ):
        """
        Load a grid of images
        Assumes symmetrical padding on the left and right.
        Same reasoning for y.
        Calls self.images_at() to get list of images
        """
        sheet_rect = self.sheet.get_rect()
        sheet_width, sheet_height = sheet_rect.size

        # Calculate the size of each sprite
        # subtract two margins, and the padding between each row, then divide by columnes
        x_sprite_size = (
            sheet_width - 2 * x_margin - (num_cols - 1) * x_padding
        ) / num_cols
        y_sprite_size = (
            sheet_height - 2 * y_margin - (num_rows - 1) * y_padding
        ) / num_rows

        sprite_rects = []
        for row_num in range(num_cols):
            for col_num in range(num_cols):
                # Position of sprite rect is margin + one sprite size
                # and one padding size for each row. Same for y.
                x = x_margin + col_num * (x_sprite_size + x_padding)
                y = y_margin + row_num * (y_sprite_size + y_padding)
                sprite_rect = (x, y, x_sprite_size, y_sprite_size)
                sprite_rects.append(sprite_rect)

        return self.images_at(sprite_rects)
