# START:BATTLE_IMPORTS
import pygame
from config import NATIVE_WIDTH, NATIVE_HEIGHT, BLACK, WHITE
# END:BATTLE_IMPORTS

# START:BATTLE_CLASS_HEADER
class BattleSystem:
    """ Manages a single combat encounter between two fighters. """
# END:BATTLE_CLASS_HEADER

# START:BATTLE_INIT
    def __init__(self, player_fighter, wild_fighter):
        self.player_fighter = player_fighter
        self.wild_fighter = wild_fighter
        self.winner = None
        self.turn = "player"
        self.battle_log = []
        self.last_action_message = f"A wild {wild_fighter.name} appeared!"
# END:BATTLE_INIT

# START:BATTLE_UPDATE
    def update(self):
        """ The main update loop for the battle system. """
        # The battle logic is now driven by user input and turns.
        # This update loop will be expanded for animations, etc.
        if self.turn == "wild":
            # Wild creature's turn
            if self.wild_fighter.is_alive():
                damage = self.wild_fighter.attack
                self.player_fighter.take_damage(damage)
                self.last_action_message = f"{self.wild_fighter.name} attacks! It deals {damage} damage."
                self.battle_log.append(self.last_action_message)
                if not self.player_fighter.is_alive():
                    self.winner = self.wild_fighter
                    self.last_action_message = f"{self.player_fighter.name} was defeated!"
                    self.battle_log.append(self.last_action_message)
            self.turn = "player"
# END:BATTLE_UPDATE

# START:BATTLE_RENDER
    def render(self, screen):
        """ Renders the battle screen. """
        pass # Rendering is now handled by the BattleUI class
# END:BATTLE_RENDER

# START:BATTLE_PLAYER_TURN_LOGIC
    def player_turn_attack(self):
        """ Handles the player's attack turn. """
        if self.turn == "player" and self.player_fighter.is_alive():
            damage = self.player_fighter.attack
            self.wild_fighter.take_damage(damage)
            self.last_action_message = f"You attack! You deal {damage} damage."
            self.battle_log.append(self.last_action_message)
            if not self.wild_fighter.is_alive():
                self.winner = self.player_fighter
                self.last_action_message = f"{self.wild_fighter.name} was defeated!"
                self.battle_log.append(self.last_action_message)
            else:
                self.turn = "wild"
# END:BATTLE_PLAYER_TURN_LOGIC