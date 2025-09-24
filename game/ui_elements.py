# START:UI_ELEMENTS_IMPORTS
import pygame
from config import WHITE, BLACK, GREEN, RED
# END:UI_ELEMENTS_IMPORTS

# START:UI_ELEMENTS_DRAW_HEALTH_BAR
def draw_health_bar(surface, fighter, position, bar_width=200, bar_height=20):
    """
    Draws a health bar for a fighter on the given surface.
    """
    # Health bar dimensions
    border_width = 2
    
    # Calculate health ratio for the health bar width
    health_ratio = fighter.current_hp / fighter.max_hp
    
    # Determine color based on health ratio
    if health_ratio > 0.5:
        health_color = GREEN
    elif health_ratio > 0.2:
        health_color = (255, 165, 0) # Orange
    else:
        health_color = RED
        
    # Draw the background of the health bar (max HP)
    pygame.draw.rect(surface, BLACK, (position[0], position[1], bar_width, bar_height))
    pygame.draw.rect(surface, WHITE, (position[0], position[1], bar_width, bar_height), border_width)

    # Draw the current health bar
    pygame.draw.rect(surface, health_color, (position[0] + border_width, position[1] + border_width, (bar_width - border_width * 2) * health_ratio, bar_height - border_width * 2))
# END:UI_ELEMENTS_DRAW_HEALTH_BAR