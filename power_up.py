import random
import pygame
from config import width, height

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 4)
        self.player = player

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > height:
            spawn_new_pos(self, width, height)

        # Attract power-up if within player's magnet_radius
        if pygame.sprite.collide_circle_ratio(self.player.magnet_radius / self.rect.width)(self, self.player):
            dx = self.player.rect.centerx - self.rect.centerx
            dy = self.player.rect.centery - self.rect.centery
            distance = (dx**2 + dy**2)**0.5
            self.rect.x += int(dx / distance * 5)
            self.rect.y += int(dy / distance * 5)
