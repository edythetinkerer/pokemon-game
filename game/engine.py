"""
Contains the core Engine class that manages the Pygame window,
rendering, and the game clock.
"""
# START:ENGINE_IMPORTS
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, GREY, GAME_VERSION
# END:ENGINE_IMPORTS

# START:ENGINE_CLASS_HEADER
class Engine:
    """ Manages the main game window, clock, and rendering. """
# END:ENGINE_CLASS_HEADER

# START:ENGINE_INIT
# START:ENGINE_INIT
def __init__(self, screen):
    # The engine now receives the screen instead of creating it
    self.screen = screen
    pygame.init() # Pygame modules still need to be initialized
    pygame.font.init() # Font module needs to be initialized
    
    self.clock = pygame.time.Clock()
    self.font = pygame.font.Font(None, 32)
    self.title_font = pygame.font.Font(None, 48)
# END:ENGINE_INIT
# END:ENGINE_INIT
# END:ENGINE_INIT
# END:ENGINE_INIT
# END:ENGINE_INIT
# END:ENGINE_INIT
# END:ENGINE_INIT
# END:ENGINE_INIT

# START:ENGINE_RENDER
    def render(self, all_sprites, elements_to_draw):
        """ Renders all game objects to the screen. """
        self.screen.fill(BLACK)
        for element, color in elements_to_draw:
            pygame.draw.rect(self.screen, color, element)
        all_sprites.draw(self.screen)
# END:ENGINE_RENDER

# START:ENGINE_RENDER_HISTORY
    def render_version_history(self, history):
        """ Renders the version history overlay. """
        overlay_rect = pygame.Rect(50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100)
        pygame.draw.rect(self.screen, GREY, overlay_rect)
        pygame.draw.rect(self.screen, WHITE, overlay_rect, 2)
        
        y_offset = 70
        self.draw_text("Version History", (overlay_rect.centerx, y_offset), self.title_font, WHITE, center=True)
        y_offset += 60

        for i, line in enumerate(history):
            self.draw_text(line, (overlay_rect.x + 30, y_offset + i * 40), self.font, WHITE)
# END:ENGINE_RENDER_HISTORY

# START:ENGINE_DRAW_TEXT
    def draw_text(self, text, pos, font, color, center=False):
        """ Helper function to draw text on the screen. """
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.centerx = pos[0]
            text_rect.top = pos[1]
        else:
            text_rect.topleft = pos
        self.screen.blit(text_surface, text_rect)
# END:ENGINE_DRAW_TEXT

# START:ENGINE_UPDATE_DISPLAY
    def update_display(self):
        """ Updates the full display Surface to the screen. """
        pygame.display.flip()
# END:ENGINE_UPDATE_DISPLAY

# START:ENGINE_TICK
    def tick(self, fps):
        """ Advances the game clock. """
        self.clock.tick(fps)
# END:ENGINE_TICK

# START:ENGINE_HANDLE_RESIZE
# START:ENGINE_LOGIC
import pygame
from config import NATIVE_WIDTH, NATIVE_HEIGHT, BLACK, WHITE, GREY

class Engine:
    """ Manages the game window, a fixed-resolution world surface, and rendering. """

    # START:ENGINE_INIT
    def __init__(self, screen):
        self.screen = screen # The main display window
        # Create the fixed-size surface where the actual game world is drawn
        self.world_surface = pygame.Surface((NATIVE_WIDTH, NATIVE_HEIGHT))
        
        pygame.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.title_font = pygame.font.Font(None, 48)
    # END:ENGINE_INIT

    # START:ENGINE_RENDER
    def render(self, all_sprites, elements_to_draw):
        """ Renders all game objects to the internal world_surface. """
        # All drawing now happens on the world_surface, not the main screen
        self.world_surface.fill(BLACK)
        for element, color in elements_to_draw:
            pygame.draw.rect(self.world_surface, color, element)
        all_sprites.draw(self.world_surface)
    # END:ENGINE_RENDER
        
    # START:ENGINE_RENDER_HISTORY
    def render_version_history(self, history):
        """ Renders the version history overlay onto the world_surface. """
        overlay_rect = pygame.Rect(50, 50, NATIVE_WIDTH - 100, NATIVE_HEIGHT - 100)
        pygame.draw.rect(self.world_surface, GREY, overlay_rect)
        pygame.draw.rect(self.world_surface, WHITE, overlay_rect, 2)
        
        y_offset = 70
        self.draw_text("Version History", (overlay_rect.centerx, y_offset), self.title_font, WHITE, center=True)
        y_offset += 60

        for i, line in enumerate(history):
            self.draw_text(line, (overlay_rect.x + 30, y_offset + i * 40), self.font, WHITE)
    # END:ENGINE_RENDER_HISTORY

    # START:ENGINE_DRAW_TEXT
    def draw_text(self, text, pos, font, color, center=False):
        """ Helper function to draw text on the world_surface. """
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.centerx = pos[0]
            text_rect.top = pos[1]
        else:
            text_rect.topleft = pos
        # Blit to the world_surface
        self.world_surface.blit(text_surface, text_rect)
    # END:ENGINE_DRAW_TEXT

    # START:ENGINE_UPDATE_DISPLAY
    def update_display(self):
        """ Scales the world_surface to the window and updates the display. """
        # Get the current size of the window
        screen_width, screen_height = self.screen.get_size()
        
        # Calculate the best scale to fit the window without stretching
        scale = min(screen_width / NATIVE_WIDTH, screen_height / NATIVE_HEIGHT)
        scaled_width = int(NATIVE_WIDTH * scale)
        scaled_height = int(NATIVE_HEIGHT * scale)
        
        # Scale the world surface to the calculated size
        scaled_surface = pygame.transform.scale(self.world_surface, (scaled_width, scaled_height))
        
        # Calculate the position to center the scaled surface on the screen
        pos_x = (screen_width - scaled_width) / 2
        pos_y = (screen_height - scaled_height) / 2
        
        # Clear the main screen (to create black bars) and draw the scaled game
        self.screen.fill(BLACK)
        self.screen.blit(scaled_surface, (pos_x, pos_y))
        
        pygame.display.flip()
    # END:ENGINE_UPDATE_DISPLAY

    # START:ENGINE_TICK
    def tick(self, fps):
        """ Advances the game clock. """
        self.clock.tick(fps)
    # END:ENGINE_TICK

    # START:ENGINE_HANDLE_RESIZE
    def handle_resize(self, event):
        """ Handles the window being resized by updating the screen reference. """
        self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
    # END:ENGINE_HANDLE_RESIZE
# END:ENGINE_LOGIC
    # END:ENGINE_HANDLE_RESIZE
# END:ENGINE_LOGIC
# END:ENGINE_HANDLE_RESIZE
    # END:ENGINE_HANDLE_RESIZE
        """ Handles the window being resized. """
        self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
# END:ENGINE_HANDLE_RESIZE
