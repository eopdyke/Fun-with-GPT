import pygame
from config import width, height


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((64, 64), pygame.SRCALPHA)
        self.color = (0, 255, 0)
        self.points = [(32, 0), (0, 60), (64, 60)]
        pygame.draw.polygon(self.image, self.color, self.points)
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
