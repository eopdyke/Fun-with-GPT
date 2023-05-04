import pygame
import random
from player import Player
from enemy import Enemy
from projectile import Projectile, FlashText
from menu import UpgradeMenu, WeaponUpgrades, ShipUpgrades
from power_up import PowerUp
from utils import draw_game_text , draw_text, fire_projectile, clear_enemies, display_stats, level_up, handle_level_up, spawn_new_pos
from config import width, height, screen, enemy_spawn_delay, current_level, all_sprites, enemies, projectiles, power_ups, score, enemies_killed

pygame.init()
SPAWNENEMY = pygame.USEREVENT + 1
clock = pygame.time.Clock()



# Set up the display
pygame.display.set_caption('Starship Game')

UPGRADE_COSTS = {
    "health": 50,
    "speed": 75,
    "magnet_radius": 100
}

class LaserBeam:
    def __init__(self, cost):
        self.cost = cost

    def apply(self, player):
        player.laser_damage += 5

class ExplosiveProjectiles:

    def __init__(self, cost):
        self.cost = cost

    def apply(self, player):
        player.blast_radius += 50
        player.explosion_damage += 10

player = Player()
all_sprites.add(player)

fire_rate = player.fire_rate

pygame.time.set_timer(SPAWNENEMY, enemy_spawn_delay)

running = True
while running:
    clock.tick(60)
    if player.health <= 0:
        running = False
        print("Game Over! Your score:", score)

# Display the Game Over screen (optional)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            fire_projectile(player, projectiles)

        if event.type == SPAWNENEMY:
            enemy = Enemy(current_level, player)
            all_sprites.add(enemy)
            enemies.add(enemy)

    all_sprites.update()

    # Check for collisions
    enemy_projectile_hits = pygame.sprite.groupcollide(enemies, projectiles, False, True)
    for enemy in enemy_projectile_hits:
        for projectile in enemy_projectile_hits[enemy]:
            enemy.health -= projectile.damage
            flash_text = FlashText(enemy.rect.x, enemy.rect.y, f"-{player.damage}", 20, (255, 255, 255))
            all_sprites.add(flash_text)
            if enemy.health <= 0:
                points_earned = 10
                score += points_earned
                player.money += points_earned
                enemy.kill()
                enemies_killed += 1
                if random.random() < 0.1:  # 10% chance of dropping a power-up
                    power_up = PowerUp()
                    all_sprites.add(power_up)
                    power_ups.add(power_up)

    player_powerup_hits = pygame.sprite.spritecollide(player, power_ups, True)
    for power_up in player_powerup_hits:
        score += 20
        player.health = min(player.health + 25, 100)  # Heal the player by 25, up to a maximum of 100

    # Level up
    handle_level_up()

    # Draw / render
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    draw_game_text(player)

    pygame.display.flip()

pygame.quit()