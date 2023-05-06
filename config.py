
import pygame

# Game window dimensions
width = 800
height = 600

score = 0
current_level = 1
enemies_killed = 0
enemies_to_kill = 5
enemy_spawn_delay = 4000

screen = pygame.display.set_mode((width, height))
last_shot = pygame.time.get_ticks()
all_sprites = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
power_ups = pygame.sprite.Group()
SPAWNENEMY = pygame.USEREVENT + 1
