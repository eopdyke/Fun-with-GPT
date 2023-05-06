import pygame
import os
from config import width, height


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_image_path = os.path.join(os.path.dirname(__file__), 'level1_starship.png')
        self.image = pygame.image.load(player_image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (128, 128))  # Scale the image to the desired size
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.bottom = height - 20
        self.speed = 3
        self.health = 100
        self.money = 0
        self.magnet_radius = 100
        self.fire_rate = 500
        self.projectile_count = 1
        self.damage = 1

        self.laser_beam_level = 0
        self.laser_damage = 0

        self.explosive_projectiles_level = 0
        self.explosion_damage = 0
        self.blast_radius = 0

        self.damage_type = "default"

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < width:
            self.rect.x += self.speed
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < height:
            self.rect.y += self.speed
