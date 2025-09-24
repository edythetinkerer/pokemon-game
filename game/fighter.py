# START:FIGHTER_IMPORTS
import pygame
from creature import Creature
from config import TILE_SIZE, WHITE, RED
# END:FIGHTER_IMPORTS

# START:FIGHTER_CLASS_HEADER
class Fighter(Creature):
    """ Represents a creature that can engage in battle. """
# END:FIGHTER_CLASS_HEADER

# START:FIGHTER_INIT
    def __init__(self, name="Fighter", max_hp=100, attack=10, defense=5):
        # Call the parent class's constructor
        super().__init__(name)
        
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attack = attack
        self.defense = defense
        
        # Override the sprite image for fighters
        self.image = pygame.Surface([TILE_SIZE * 4, TILE_SIZE * 4])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
# END:FIGHTER_INIT

# START:FIGHTER_TAKE_DAMAGE
    def take_damage(self, amount):
        """ Calculates damage taken and updates HP. """
        damage_taken = max(0, amount - self.defense)
        self.current_hp -= damage_taken
        if self.current_hp < 0:
            self.current_hp = 0
        return damage_taken
# END:FIGHTER_TAKE_DAMAGE

# START:FIGHTER_IS_ALIVE
    def is_alive(self):
        """ Checks if the fighter is still alive. """
        return self.current_hp > 0
# END:FIGHTER_IS_ALIVE

# START:FIGHTER_HEAL
    def heal(self, amount):
        """ Heals the fighter, up to their max HP. """
        self.current_hp += amount
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp
# END:FIGHTER_HEAL