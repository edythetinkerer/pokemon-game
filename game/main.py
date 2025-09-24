"""
The main entry point for the game. This file initializes all game
systems and runs the main game loop.
"""
# START:MAIN_IMPORTS
import pygame
from engine import Engine
from player import Player
from tile import Tile
# This single, complete line fixes the crash
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_VERSION, VERSION_HISTORY, LIGHT_BLUE, GREEN, PINK, NATIVE_WIDTH, NATIVE_HEIGHT
from assets import load_pixel_art
from maps import STARTING_TOWN_MAP
from fighter import Fighter
from battle import BattleSystem
from battle_ui import BattleUI
# END:MAIN_IMPORTS

# START:MAIN_GAME_CLASS
class Game:
    """ Manages the main game state and logic. """

    # START:GAME_INIT
    def __init__(self):
        # Initialize Pygame and create the screen FIRST
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption(f"Pocket Creatures Adventure - {GAME_VERSION}")
    
        # Now, create the engine and pass the screen to it
        self.engine = Engine(screen)
        self.assets = load_pixel_art()
    
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.map_sprites = pygame.sprite.Group()
    
        # Define the mapping from map characters to assets and colors
        tile_definitions = {
            'g': (self.assets['grass'], {'g': GREEN}),
            'f': (self.assets['flower'], {'g': GREEN, 'f': PINK})
        }
    
        # Build the map (this is now safe to do)
        for y, row in enumerate(STARTING_TOWN_MAP):
            for x, char in enumerate(row):
                if char in tile_definitions:
                    shape, colors = tile_definitions[char]
                    tile = Tile(x, y, shape, colors)
                    self.map_sprites.add(tile)
    
        # Create the player
        self.player = Player(400, 300, self.assets) # Centered player start
        
        # Add sprites to the main group in the correct render order
        self.all_sprites.add(self.map_sprites)
        self.all_sprites.add(self.player)
    
        # UI Elements
        self.version_square = pygame.Rect(30, 30, 32, 32)
        self.show_versions = False
        self.running = True

        # Game state management
        self.game_state = "exploring"
        self.current_battle = None
        self.battle_ui = BattleUI(self.engine.world_surface)
    # END:GAME_INIT

    # START:GAME_RUN_LOOP
    def run(self):
        """ The main game loop. """
        while self.running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        if self.player.rect.colliderect(self.version_square):
                            self.show_versions = not self.show_versions
                    if event.key == pygame.K_b and self.game_state == "exploring":
                        # TEMP: Start a battle with 'B' key
                        player_fighter = Fighter("Hero", 100, 20, 5)
                        wild_fighter = Fighter("Wild Creature", 50, 15, 3)
                        self.current_battle = BattleSystem(player_fighter, wild_fighter)
                        self.game_state = "battle"
                
                # New mouse click handling for battle menu
                if event.type == pygame.MOUSEBUTTONDOWN and self.game_state == "battle":
                    if self.current_battle.turn == "player":
                        scaled_pos = (event.pos[0] * NATIVE_WIDTH / self.engine.screen.get_width(),
                                      event.pos[1] * NATIVE_HEIGHT / self.engine.screen.get_height())
                        
                        action = self.battle_ui.action_menu.handle_click(scaled_pos)
                        if action == 'attack':
                            self.current_battle.player_turn_attack()
                        elif action == 'flee':
                            print("You flee from battle!") # Placeholder
                            self.current_battle.winner = self.current_battle.wild_fighter # End battle
            
            # Update
            if self.game_state == "exploring":
                if not self.show_versions:
                    self.all_sprites.update()
            elif self.game_state == "battle":
                self.current_battle.update()
                # Check for a winner after each turn
                if self.current_battle.winner:
                    self.game_state = "exploring"
                    self.current_battle = None
                
            # Render
            if self.game_state == "exploring":
                elements_to_draw = [(self.version_square, LIGHT_BLUE)]
                self.engine.render(self.all_sprites, elements_to_draw)

                if self.show_versions:
                    self.engine.render_version_history(VERSION_HISTORY)
            elif self.game_state == "battle":
                self.battle_ui.render(self.current_battle)

            self.engine.update_display()
            self.engine.tick(60)

        pygame.quit()
    # END:GAME_RUN_LOOP
# END:MAIN_GAME_CLASS

# START:MAIN_ENTRY_POINT
"""
The main entry point for the game. This file initializes all game
systems and runs the main game loop.
"""
# START:MAIN_IMPORTS
import pygame
import random
from engine import Engine
from player import Player
from tile import Tile
# This single, complete line fixes the crash
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_VERSION, VERSION_HISTORY, LIGHT_BLUE, GREEN, PINK, NATIVE_WIDTH, NATIVE_HEIGHT, TILE_SIZE, WHITE, BLACK, GREY, DARK_GREEN
from assets import load_pixel_art
from maps import STARTING_TOWN_MAP
from fighter import Fighter
from battle import BattleSystem
from battle_ui import BattleUI
from sound_manager import SoundManager
from ui_elements import draw_health_bar
# END:MAIN_IMPORTS

# START:MAIN_GAME_CLASS
class Game:
    """ Manages the main game state and logic. """

    # START:GAME_INIT
    def __init__(self):
        # Initialize Pygame and create the screen FIRST
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption(f"Pocket Creatures Adventure - {GAME_VERSION}")
    
        # Now, create the engine and pass the screen to it
        self.engine = Engine(screen)
        self.assets = load_pixel_art()
    
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.map_sprites = pygame.sprite.Group()
    
        # Define the mapping from map characters to assets and colors
        tile_definitions = {
            'g': (self.assets['grass'], {'g': GREEN}),
            'f': (self.assets['flower'], {'g': GREEN, 'f': PINK}),
            't': (self.assets['tall_grass'], {'t': DARK_GREEN})
        }
    
        # Build the map (this is now safe to do)
        for y, row in enumerate(STARTING_TOWN_MAP):
            for x, char in enumerate(row):
                if char in tile_definitions:
                    shape, colors = tile_definitions[char]
                    tile = Tile(x, y, shape, colors)
                    self.map_sprites.add(tile)
    
        # Create the player
        self.player = Player(400, 300, self.assets) # Centered player start
        self.player_creature = Fighter("Hero's Creature", 120, 15, 6) # A placeholder creature for the player
        
        # Add sprites to the main group in the correct render order
        self.all_sprites.add(self.map_sprites)
        self.all_sprites.add(self.player)
    
        # UI Elements
        self.version_square = pygame.Rect(30, 30, 32, 32)
        self.running = True

        # Game state management
        self.game_state = "start_screen"
        self.current_battle = None
        self.battle_ui = BattleUI(self.engine.world_surface)
        self.settings_open = False
        self.settings_tab = "audio" # New variable to track the active tab

        # Sound Management
        self.sound_manager = SoundManager()
        self.sound_manager.load_music("exploration")
    # END:GAME_INIT

    # START:GAME_RUN_LOOP
    def run(self):
        """ The main game loop. """
        while self.running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.game_state == "exploring" or self.settings_open:
                        self.settings_open = not self.settings_open
                if self.game_state == "start_screen":
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        self.game_state = "exploring"
                        self.sound_manager.play_music()
                elif self.game_state == "exploring":
                    if event.type == pygame.KEYDOWN:
                        pass # No other key presses on the map for now
                elif self.game_state == "battle":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.current_battle.turn == "player":
                            scaled_pos = (event.pos[0] * NATIVE_WIDTH / self.engine.screen.get_width(),
                                          event.pos[1] * NATIVE_HEIGHT / self.engine.screen.get_height())
                            
                            action = self.battle_ui.action_menu.handle_click(scaled_pos)
                            if action == 'attack':
                                self.current_battle.player_turn_attack()
                            elif action == 'flee':
                                print("You flee from battle!") # Placeholder
                                self.current_battle.winner = self.current_battle.wild_fighter # End battle
                # Check for settings menu click
                if self.settings_open and event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_settings_input(event.pos)
                
            # Update
            if self.game_state == "exploring" and not self.settings_open:
                self.all_sprites.update()
                self.trigger_battle()
            elif self.game_state == "battle":
                self.current_battle.update()
                # Check for a winner after each turn
                if self.current_battle.winner:
                    self.game_state = "exploring"
                    self.current_battle = None
                    self.sound_manager.load_music("exploration")
                    self.sound_manager.play_music()
                
            # Render
            if self.settings_open:
                self.draw_settings_menu()
            elif self.game_state == "start_screen":
                # Render directly to the world_surface, not the screen
                self.engine.world_surface.fill(BLACK)
                title_text = self.engine.title_font.render("Pocket Creatures Adventure", True, WHITE)
                start_text = self.engine.font.render("Press any key to start", True, WHITE)
                version_text = self.engine.font.render(GAME_VERSION, True, WHITE)
                title_rect = title_text.get_rect(center=(NATIVE_WIDTH / 2, NATIVE_HEIGHT / 2 - 50))
                start_rect = start_text.get_rect(center=(NATIVE_WIDTH / 2, NATIVE_HEIGHT / 2 + 50))
                version_rect = version_text.get_rect(bottomright=(NATIVE_WIDTH - 10, NATIVE_HEIGHT - 10))
                self.engine.world_surface.blit(title_text, title_rect)
                self.engine.world_surface.blit(start_text, start_rect)
                self.engine.world_surface.blit(version_text, version_rect)
            elif self.game_state == "exploring":
                elements_to_draw = [(self.version_square, LIGHT_BLUE)]
                self.engine.render(self.all_sprites, elements_to_draw)
                self.draw_exploration_ui()
            elif self.game_state == "battle":
                self.battle_ui.render(self.current_battle)

            self.engine.update_display()
            self.engine.tick(60)

        pygame.quit()
    # END:GAME_RUN_LOOP

    # START:GAME_BATTLE_TRIGGER
    def trigger_battle(self):
        """ Checks if a battle should be triggered. """
        # Get the tile the player is currently on
        player_tile_x = int(self.player.rect.centerx / (TILE_SIZE * 4))
        player_tile_y = int(self.player.rect.centery / (TILE_SIZE * 4))

        # Check if the player is on a 't' (tall grass) tile
        if 0 <= player_tile_y < len(STARTING_TOWN_MAP) and 0 <= player_tile_x < len(STARTING_TOWN_MAP[0]):
            current_tile_char = STARTING_TOWN_MAP[player_tile_y][player_tile_x]
            
            # Check for a random battle encounter only when the player is moving
            if current_tile_char == 't' and self.player.is_moving:
                # 1 in 10 chance to trigger a battle
                if random.randint(1, 10) == 1:
                    print("A wild creature appeared!")
                    self.sound_manager.stop_music()
                    self.sound_manager.play_sfx("encounter.ogg")
                    self.sound_manager.load_music("battle")
                    self.sound_manager.play_music()
                    player_fighter = Fighter("Hero", 100, 20, 5)
                    wild_fighter = Fighter("Wild Creature", 50, 15, 3)
                    self.current_battle = BattleSystem(player_fighter, wild_fighter)
                    self.game_state = "battle"
    # END:GAME_BATTLE_TRIGGER

    # START:GAME_EXPLORATION_UI
    def draw_exploration_ui(self):
        """ Renders the UI elements for exploration mode. """
        # Draw a semi-transparent background at the bottom of the screen
        ui_background = pygame.Surface((NATIVE_WIDTH, 100), pygame.SRCALPHA)
        ui_background.fill((0, 0, 0, 128)) # Semi-transparent black
        ui_rect = ui_background.get_rect(bottomleft=(0, NATIVE_HEIGHT))
        self.engine.world_surface.blit(ui_background, ui_rect)
        
        # Player creature info
        creature_name_text = self.engine.font.render(self.player_creature.name, True, WHITE)
        self.engine.world_surface.blit(creature_name_text, (10, NATIVE_HEIGHT - 90))
        
        # HP text
        hp_text = self.engine.font.render("HP:", True, WHITE)
        self.engine.world_surface.blit(hp_text, (10, NATIVE_HEIGHT - 60))

        # Health bar
        draw_health_bar(self.engine.world_surface, self.player_creature, (50, NATIVE_HEIGHT - 60), bar_width=250)
        
        # Buttons (placeholder)
        menu_button_text = self.engine.font.render("Menu", True, WHITE)
        menu_button_rect = menu_button_text.get_rect(topright=(NATIVE_WIDTH - 20, NATIVE_HEIGHT - 90))
        self.engine.world_surface.blit(menu_button_text, menu_button_rect)

        # Draw a temporary box around the version square to make it more visible
        pygame.draw.rect(self.engine.world_surface, WHITE, self.version_square, 2)
    # END:GAME_EXPLORATION_UI

    # START:GAME_SETTINGS_LOGIC
    def draw_settings_menu(self):
        """ Renders the settings menu. """
        self.engine.world_surface.fill(BLACK)
        
        # Tabs
        tab_rects = {
            "audio": pygame.Rect(NATIVE_WIDTH/2 - 150, 50, 150, 50),
            "log": pygame.Rect(NATIVE_WIDTH/2, 50, 150, 50)
        }
        
        # Draw active tab background
        pygame.draw.rect(self.engine.world_surface, GREY, tab_rects[self.settings_tab])
        
        # Draw tab text and borders
        for tab_name, rect in tab_rects.items():
            text = self.engine.font.render(tab_name.capitalize(), True, WHITE)
            text_rect = text.get_rect(center=rect.center)
            self.engine.world_surface.blit(text, text_rect)
            pygame.draw.rect(self.engine.world_surface, WHITE, rect, 2)
            
        # Draw content based on active tab
        if self.settings_tab == "audio":
            self.draw_audio_tab()
        elif self.settings_tab == "log":
            self.draw_log_tab()
            
        # Draw Back and Quit buttons
        back_text = self.engine.font.render("Back", True, WHITE)
        back_rect = back_text.get_rect(center=(NATIVE_WIDTH / 2, NATIVE_HEIGHT - 160))
        self.engine.world_surface.blit(back_text, back_rect)

        quit_text = self.engine.font.render("Quit", True, WHITE)
        quit_rect = quit_text.get_rect(center=(NATIVE_WIDTH / 2, NATIVE_HEIGHT - 100))
        self.engine.world_surface.blit(quit_text, quit_rect)
    
    def draw_audio_tab(self):
        """ Renders the audio settings. """
        # Draw Music Volume slider
        music_text = self.engine.font.render("Music Volume:", True, WHITE)
        self.engine.world_surface.blit(music_text, (NATIVE_WIDTH / 4, NATIVE_HEIGHT / 2 - 50))
        # Draw slider line
        slider_x = NATIVE_WIDTH / 2
        slider_y = NATIVE_HEIGHT / 2 - 40
        slider_length = NATIVE_WIDTH / 4
        pygame.draw.line(self.engine.world_surface, WHITE, (slider_x, slider_y), (slider_x + slider_length, slider_y), 5)
        # Draw slider button
        music_slider_pos = slider_x + slider_length * self.sound_manager.music_volume
        pygame.draw.circle(self.engine.world_surface, GREY, (music_slider_pos, slider_y), 10)

        # Draw SFX Volume slider
        sfx_text = self.engine.font.render("SFX Volume:", True, WHITE)
        self.engine.world_surface.blit(sfx_text, (NATIVE_WIDTH / 4, NATIVE_HEIGHT / 2 + 50))
        # Draw slider line
        sfx_slider_x = NATIVE_WIDTH / 2
        sfx_slider_y = NATIVE_HEIGHT / 2 + 60
        sfx_slider_length = NATIVE_WIDTH / 4
        pygame.draw.line(self.engine.world_surface, WHITE, (sfx_slider_x, sfx_slider_y), (sfx_slider_x + sfx_slider_length, sfx_slider_y), 5)
        # Draw slider button
        sfx_slider_pos = sfx_slider_x + sfx_slider_length * self.sound_manager.sfx_volume
        pygame.draw.circle(self.engine.world_surface, GREY, (sfx_slider_pos, sfx_slider_y), 10)

    def draw_log_tab(self):
        """ Renders the version history log. """
        self.engine.render_version_history(VERSION_HISTORY)

    def handle_settings_input(self, pos):
        """ Handles input for the settings menu. """
        # Scale mouse position from screen to world_surface
        scaled_pos_x = pos[0] * NATIVE_WIDTH / self.engine.screen.get_width()
        scaled_pos_y = pos[1] * NATIVE_HEIGHT / self.engine.screen.get_height()
        scaled_pos = (scaled_pos_x, scaled_pos_y)

        # Tab buttons
        tab_rects = {
            "audio": pygame.Rect(NATIVE_WIDTH/2 - 150, 50, 150, 50),
            "log": pygame.Rect(NATIVE_WIDTH/2, 50, 150, 50)
        }
        for tab_name, rect in tab_rects.items():
            if rect.collidepoint(scaled_pos):
                self.settings_tab = tab_name
                return
        
        # Quit button
        quit_rect = pygame.Rect(NATIVE_WIDTH / 2 - 50, NATIVE_HEIGHT - 120, 100, 40)
        if quit_rect.collidepoint(scaled_pos):
            self.running = False
            return

        # Back button
        back_rect = pygame.Rect(NATIVE_WIDTH / 2 - 50, NATIVE_HEIGHT - 180, 100, 40)
        if back_rect.collidepoint(scaled_pos):
            self.settings_open = False
            return
        
        # Audio tab input
        if self.settings_tab == "audio":
            # Music slider
            music_slider_y = NATIVE_HEIGHT / 2 - 40
            if scaled_pos_y > music_slider_y - 10 and scaled_pos_y < music_slider_y + 10:
                slider_x = NATIVE_WIDTH / 2
                slider_length = NATIVE_WIDTH / 4
                new_volume = (scaled_pos_x - slider_x) / slider_length
                if new_volume >= 0 and new_volume <= 1:
                    self.sound_manager.music_volume = new_volume
                    pygame.mixer.music.set_volume(new_volume)

            # SFX slider
            sfx_slider_y = NATIVE_HEIGHT / 2 + 60
            if scaled_pos_y > sfx_slider_y - 10 and scaled_pos_y < sfx_slider_y + 10:
                sfx_slider_x = NATIVE_WIDTH / 2
                sfx_slider_length = NATIVE_WIDTH / 4
                new_volume = (scaled_pos_x - sfx_slider_x) / sfx_slider_length
                if new_volume >= 0 and new_volume <= 1:
                    self.sound_manager.sfx_volume = new_volume
    # END:GAME_SETTINGS_LOGIC
# END:MAIN_GAME_CLASS

# START:MAIN_ENTRY_POINT
if __name__ == "__main__":
    game = Game()
    game.run()
# END:MAIN_ENTRY_POINT
# END:MAIN_ENTRY_POINT
# END:MAIN_ENTRY_POINT
# END:MAIN_ENTRY_POINT
# END:MAIN_ENTRY_POINT
# END:MAIN_ENTRY_POINT
# END:MAIN_ENTRY_POINT
# END:MAIN_ENTRY_POINT
# END:MAIN_ENTRY_POINT
# END:MAIN_ENTRY_POINT
# END:MAIN_ENTRY_POINT
# END:MAIN_ENTRY_POINT
# END:MAIN_ENTRY_POINT
# END:MAIN_ENTRY_POINT