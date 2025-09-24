"""
Contains the Tile class, which represents a single square on the game map.
"""
# START:TILE_IMPORTS
import pygame
from config import TILE_SIZE
# END:TILE_IMPORTS

# START:TILE_CLASS_HEADER
class Tile(pygame.sprite.Sprite):
    """ Represents a single, static tile in the game world. """
# END:TILE_CLASS_HEADER

    # START:TILE_INIT
    def __init__(self, x, y, shape_data, colors):
        super().__init__()
        self.image = self.generate_sprite(shape_data, colors)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE * 4 # We multiply by TILE_SIZE and scale factor
        self.rect.y = y * TILE_SIZE * 4
    # END:TILE_INIT

    # START:TILE_GENERATE_SPRITE
    def generate_sprite(self, shape_data, colors):
        """
        Generates a final, optimized sprite surface from pixel data.
        This function is called only once when the tile is created.
        """
        scale_factor = 4
        final_size = TILE_SIZE * scale_factor
        
        temp_surface = pygame.Surface([final_size, final_size], pygame.SRCALPHA)
        temp_surface.fill((0, 0, 0, 0))

        pixel_size = scale_factor

        for y, row in enumerate(shape_data):
            for x, pixel_char in enumerate(row):
                if pixel_char in colors:
                    pygame.draw.rect(temp_surface, colors[pixel_char], (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
        
        return temp_surface.convert_alpha()
    # END:TILE_GENERATE_SPRITE
