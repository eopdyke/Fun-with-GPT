import pygame
import random
from player import Player
from enemy import Enemy
from projectile import Projectile, FlashText
from menu import UpgradeMenu, WeaponUpgrades, ShipUpgrades
from power_up import PowerUp
from utils import draw_game_text , draw_text, fire_projectile, clear_enemies, display_stats, level_up, handle_level_up, spawn_new_pos
import config 

pygame.init()
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
config.all_sprites.add(player)

fire_rate = player.fire_rate

pygame.time.set_timer(config.SPAWNENEMY, config.enemy_spawn_delay)

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
            fire_projectile(player, config.projectiles)

        if event.type == config.SPAWNENEMY:
            enemy = Enemy(config.current_level, player)
            config.all_sprites.add(enemy)
            config.enemies.add(enemy)

    config.all_sprites.update()

    # Check for collisions
    enemy_projectile_hits = pygame.sprite.groupcollide(config.enemies, config.projectiles, False, True)
    for enemy in enemy_projectile_hits:
        for projectile in enemy_projectile_hits[enemy]:
            enemy.health -= projectile.damage
            flash_text = FlashText(enemy.rect.x, enemy.rect.y, f"-{player.damage}", 20, (255, 255, 255))
            config.all_sprites.add(flash_text)
            if enemy.health <= 0:
                points_earned = 10
                config.score += points_earned
                print(config.score)
                player.money += points_earned
                enemy.kill()
                config.enemies_killed += 1
                if random.random() < 0.1:  # 10% chance of dropping a power-up
                    power_up = PowerUp(player)
                    config.all_sprites.add(power_up)
                    config.power_ups.add(power_up)

    player_powerup_hits = pygame.sprite.spritecollide(player, config.power_ups, True)
    for power_up in player_powerup_hits:
        config.score += 20
        player.health = min(player.health + 25, 100)  # Heal the player by 25, up to a maximum of 100

    # Level up
    handle_level_up()

    # Draw / render
    # Load the background image
    background = pygame.image.load("cityscape.png").convert()
    background = pygame.transform.scale(background, (config.width, config.height))
    # Draw the background image
    config.screen.blit(background, (0, 0))
    config.all_sprites.draw(config.screen)
    draw_game_text(player)

    pygame.display.flip()

pygame.quit()