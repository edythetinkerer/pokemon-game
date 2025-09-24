"""
Defines the base class for all creatures in the game.
"""
# START:CREATURE_IMPORTS
import pygame
from config import TILE_SIZE, RED
# END:CREATURE_IMPORTS

# START:CREATURE_CLASS_HEADER
class Creature(pygame.sprite.Sprite):
    """ A base class for creatures. """
# END:CREATURE_CLASS_HEADER

# START:CREATURE_INIT
# START:CREATURE_INIT
    def __init__(self, name="Creature"):
        super().__init__()
        # For now, creatures will be simple red squares
        self.name = name
        self.image = pygame.Surface([TILE_SIZE * 4, TILE_SIZE * 4])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
# END:CREATURE_INIT
# END:CREATURE_INIT

