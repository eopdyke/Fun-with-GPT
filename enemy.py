import random
import pygame
from config import width, height
from utils import spawn_new_pos
from player import Player


class Enemy(pygame.sprite.Sprite):
   
    def __init__(self, current_level, player):
        super().__init__()

        enemy_hp = {
        1: {"hp": 3, "kill_count": 1},
        2: {"hp": 3, "kill_count": 1},
        3: {"hp": 6, "kill_count": 2},
        4: {"hp": 9, "kill_count": 2},
        5: {"hp": 11, "kill_count": 3},
        6: {"hp": 16, "kill_count": 3},
        # Add more levels as needed
        }

        self.image = pygame.Surface((64, 64), pygame.SRCALPHA)
        self.color = (255, 0, 0)
        self.points = [(32, 60), (0, 0), (64, 0)]
        pygame.draw.polygon(self.image, self.color, self.points)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 4)
        self.health = enemy_hp[current_level]["hp"]

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > height:
            spawn_new_pos(self, width, height)
            self.player.health -= 10  # Reduce player health when an enemy reaches the bottom of the screen
