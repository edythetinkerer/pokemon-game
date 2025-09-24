# START:BATTLE_UI_IMPORTS
import pygame
from config import NATIVE_WIDTH, NATIVE_HEIGHT, BLACK, WHITE, GREY, RED, GREEN
from action_menu import ActionMenu
from ui_elements import draw_health_bar
# END:BATTLE_UI_IMPORTS

# START:BATTLE_UI_CLASS_HEADER
class BattleUI:
    """ Renders the visual components of a battle. """
# END:BATTLE_UI_CLASS_HEADER

# START:BATTLE_UI_INIT
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 32)
        self.action_menu = ActionMenu()
# END:BATTLE_UI_INIT

# START:BATTLE_UI_RENDER
    def render(self, battle_system):
        self.screen.fill(GREY) # A neutral background color

        # Draw player fighter
        player_x = NATIVE_WIDTH / 4
        player_y = NATIVE_HEIGHT / 2
        battle_system.player_fighter.rect.center = (player_x, player_y)
        self.screen.blit(battle_system.player_fighter.image, battle_system.player_fighter.rect)

        # Draw wild fighter
        wild_x = NATIVE_WIDTH * 3 / 4
        wild_y = NATIVE_HEIGHT / 2 - 50
        battle_system.wild_fighter.rect.center = (wild_x, wild_y)
        self.screen.blit(battle_system.wild_fighter.image, battle_system.wild_fighter.rect)

        # Battle Log
        log_surface = pygame.Surface((NATIVE_WIDTH, 100))
        log_surface.fill(BLACK)
        log_rect = log_surface.get_rect(bottomleft=(0, NATIVE_HEIGHT))
        self.screen.blit(log_surface, log_rect)
        
        # Display the last action message
        log_text = self.font.render(battle_system.last_action_message, True, WHITE)
        self.screen.blit(log_text, (20, NATIVE_HEIGHT - 75))

        # Render the action menu
        self.action_menu.render(self.screen)

        # Draw health bars
        draw_health_bar(self.screen, battle_system.player_fighter, (50, 50))
        draw_health_bar(self.screen, battle_system.wild_fighter, (NATIVE_WIDTH - 250, 50))

        # Display HP text
        player_hp_text = self.font.render(f"{battle_system.player_fighter.current_hp}/{battle_system.player_fighter.max_hp}", True, WHITE)
        self.screen.blit(player_hp_text, (50 + 200 + 10, 50))
        
        wild_hp_text = self.font.render(f"{battle_system.wild_fighter.current_hp}/{battle_system.wild_fighter.max_hp}", True, WHITE)
        self.screen.blit(wild_hp_text, (NATIVE_WIDTH - 250 + 200 + 10, 50))
# END:BATTLE_UI_RENDER

# START:BATTLE_UI_DRAW_HEALTH_BAR
    def draw_health_bar(self, fighter, position):
        # This method is now obsolete and will be replaced
        pass
# END:BATTLE_UI_DRAW_HEALTH_BAR