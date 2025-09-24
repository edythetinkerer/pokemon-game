"""
Defines the Player class, which handles the character's appearance,
position, and response to user input.
"""
# START:PLAYER_IMPORTS
import pygame
from config import TILE_SIZE, WHITE
# END:PLAYER_IMPORTS

# START:PLAYER_CLASS_HEADER
class Player(pygame.sprite.Sprite):
    """ Represents the player character, with an image generated from pixel data at creation. """
# END:PLAYER_CLASS_HEADER

# START:PLAYER_INIT
    def __init__(self, x, y, assets):
        super().__init__()
        
        # This function builds the sprite image ONCE during initialization.
        self.image = self.generate_sprite(assets['player'], WHITE)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 4
# END:PLAYER_INIT

# START:PLAYER_GENERATE_SPRITE
    def generate_sprite(self, shape_data, color):
        """
        Generates a final, optimized sprite surface from pixel data.
        This function is called only once.
        """
        scale_factor = 4 # How much to scale up each "pixel"
        final_size = TILE_SIZE * scale_factor
        
        # Create a temporary surface to draw on
        temp_surface = pygame.Surface([final_size, final_size], pygame.SRCALPHA)
        temp_surface.fill((0, 0, 0, 0)) # Fill with fully transparent

        pixel_size = scale_factor
        skin_color = (255, 220, 180) # A simple skin tone

        for y, row in enumerate(shape_data):
            for x, pixel in enumerate(row):
                if pixel == '1': # Draw a main body pixel
                    pygame.draw.rect(temp_surface, color, (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
                elif pixel == '.': # Draw a skin-tone pixel
                    pygame.draw.rect(temp_surface, skin_color, (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
        
        # Return the final, high-performance converted surface.
        return temp_surface.convert_alpha()
# END:PLAYER_GENERATE_SPRITE

# START:PLAYER_UPDATE
    def update(self):
        """ Update the player's position based on key presses. """
        self.handle_input()
# END:PLAYER_UPDATE

# START:PLAYER_HANDLE_INPUT
"""
Defines the Player class, which handles the character's appearance,
position, and response to user input.
"""
# START:PLAYER_IMPORTS
import pygame
from config import TILE_SIZE, WHITE
# END:PLAYER_IMPORTS

# START:PLAYER_CLASS_HEADER
class Player(pygame.sprite.Sprite):
    """ Represents the player character, with an image generated from pixel data at creation. """
# END:PLAYER_CLASS_HEADER

# START:PLAYER_INIT
    def __init__(self, x, y, assets):
        super().__init__()
        
        # This function builds the sprite image ONCE during initialization.
        self.image = self.generate_sprite(assets['player'], WHITE)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 4
        self.is_moving = False
# END:PLAYER_INIT

# START:PLAYER_GENERATE_SPRITE
    def generate_sprite(self, shape_data, color):
        """
        Generates a final, optimized sprite surface from pixel data.
        This function is called only once.
        """
        scale_factor = 4 # How much to scale up each "pixel"
        final_size = TILE_SIZE * scale_factor
        
        # Create a temporary surface to draw on
        temp_surface = pygame.Surface([final_size, final_size], pygame.SRCALPHA)
        temp_surface.fill((0, 0, 0, 0)) # Fill with fully transparent

        pixel_size = scale_factor
        skin_color = (255, 220, 180) # A simple skin tone

        for y, row in enumerate(shape_data):
            for x, pixel in enumerate(row):
                if pixel == '1': # Draw a main body pixel
                    pygame.draw.rect(temp_surface, color, (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
                elif pixel == '.': # Draw a skin-tone pixel
                    pygame.draw.rect(temp_surface, skin_color, (x * pixel_size, y * pixel_size, pixel_size, pixel_size))
        
        # Return the final, high-performance converted surface.
        return temp_surface.convert_alpha()
# END:PLAYER_GENERATE_SPRITE

# START:PLAYER_UPDATE
    def update(self):
        """ Update the player's position based on key presses. """
        self.handle_input()
# END:PLAYER_UPDATE

# START:PLAYER_HANDLE_INPUT
    def handle_input(self):
        """ Checks for keyboard input and moves the player. """
        keys = pygame.key.get_pressed()
        self.is_moving = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.is_moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
            self.is_moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.is_moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
            self.is_moving = True
# END:PLAYER_HANDLE_INPUT
# END:PLAYER_HANDLE_INPUT

