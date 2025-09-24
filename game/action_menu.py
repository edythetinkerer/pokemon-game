# START:ACTION_MENU_IMPORTS
import pygame
from config import NATIVE_WIDTH, NATIVE_HEIGHT, WHITE, GREY
# END:ACTION_MENU_IMPORTS

# START:ACTION_MENU_CLASS_HEADER
class ActionMenu:
    """ Manages the UI for player actions in battle. """
# END:ACTION_MENU_CLASS_HEADER

# START:ACTION_MENU_INIT
    def __init__(self):
        self.font = pygame.font.Font(None, 32)
        self.buttons = []
        self.create_buttons()
# END:ACTION_MENU_INIT

# START:ACTION_MENU_CREATE_BUTTONS
    def create_buttons(self):
        # We will dynamically create buttons here
        button_width = 200
        button_height = 50
        button_y = NATIVE_HEIGHT - 120
        
        # Attack button
        attack_rect = pygame.Rect(NATIVE_WIDTH // 4 - button_width // 2, button_y, button_width, button_height)
        self.buttons.append({'text': 'Attack', 'rect': attack_rect, 'action': 'attack'})
        
        # Flee button
        flee_rect = pygame.Rect(NATIVE_WIDTH * 3 // 4 - button_width // 2, button_y, button_width, button_height)
        self.buttons.append({'text': 'Flee', 'rect': flee_rect, 'action': 'flee'})
# END:ACTION_MENU_CREATE_BUTTONS

# START:ACTION_MENU_RENDER
    def render(self, screen):
        for button in self.buttons:
            pygame.draw.rect(screen, GREY, button['rect'], 0, 5) # Draw filled rect
            pygame.draw.rect(screen, WHITE, button['rect'], 2, 5) # Draw border
            
            text_surface = self.font.render(button['text'], True, WHITE)
            text_rect = text_surface.get_rect(center=button['rect'].center)
            screen.blit(text_surface, text_rect)
# END:ACTION_MENU_RENDER

# START:ACTION_MENU_HANDLE_CLICK
    def handle_click(self, pos):
        for button in self.buttons:
            if button['rect'].collidepoint(pos):
                return button['action']
        return None
# END:ACTION_MENU_HANDLE_CLICK