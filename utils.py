import sys
import random
import pygame
import config
from player import Player
from projectile import Projectile


def draw_text(surf, text, x, y, size=24, color=(255, 255, 255)):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def clear_enemies(enemies):
    for enemy in enemies:
        enemy.kill()

def display_stats(screen, player, score):
    draw_text(screen, f"Score: {score}", width // 2, 300)
    draw_text(screen, f"Health: {player.health}", width // 2, 340)
    draw_text(screen, f"Speed: {player.speed}", width // 2, 380)
    draw_text(screen, f"Magnet Radius: {player.magnet_radius}", width // 2, 420)

def level_up():
    config.current_level += 1
    config.enemies_killed = 0
    config.enemies_to_kill += 5

    if config.current_level % 3 == 0:
        config.enemy_spawn_delay = max(config.enemy_spawn_delay - 500, 500)
    pygame.time.set_timer(config.SPAWNENEMY, config.enemy_spawn_delay // config.current_level)

    upgrade_menu = UpgradeMenu(player, screen)
    result = None

    while result != "next_level":
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            result = upgrade_menu.handle_input(e)

        screen.fill((0, 0, 0))
        draw_text(screen, f"Level {current_level} - Upgrade your ship!", width // 2, 50)
        draw_text(screen, "Use the arrow keys to navigate and Enter to purchase upgrades.", width // 2, height - 50)
        upgrade_menu.draw()
        pygame.display.flip()

def fire_projectile(player, projectiles):
    now = pygame.time.get_ticks()
    if now - config.last_shot > player.fire_rate:
        config.last_shot = now
        for i in range(player.projectile_count):
            offset_x = (i - (player.projectile_count - 1) / 2) * 20  # Position projectiles with a 20-pixel spacing
            projectile = Projectile(player.rect.centerx + offset_x, player.rect.top, player, player.damage_type)
            config.all_sprites.add(projectile)
            projectiles.add(projectile)

def handle_level_up():
    if config.enemies_killed == config.current_level * 5:
        config.current_level += 1
        level_up()

def draw_game_text(player):
    # Draw player health
    draw_health_bar(config.screen, 10, 10, player.health)

    # Draw player score
    draw_text(config.screen, f"Score: {config.score}", config.width // 2, 10, 24, (255, 255, 255))

    # Draw player money
    draw_text(config.screen, f"Money: ${player.money}", config.width - 50, 10, 24, (255, 255, 255))

    # Draw player level
    draw_text(config.screen, f"Level: {config.current_level}", 50, config.height - 40, 24, (255, 255, 255))

    # Draw remaining enemies to kill
    draw_text(config.screen, f"Enemies: {config.enemies_to_kill - config.enemies_killed}", config.width - 50, config.height - 40, 24, (255, 255, 255))


def spawn_new_pos(sprite, width, height):
    sprite.rect.x = random.randrange(width - sprite.rect.width)
    sprite.rect.y = random.randrange(-100, -40)
    sprite.speedy = random.randrange(1, 4)

def draw_health_bar(screen, x, y, health):
    # Set the health bar dimensions
    bar_width = 100
    bar_height = 10

    # Calculate the health percentage and the width of the filled part of the health bar
    health_percentage = health / 100.0
    fill_width = int(bar_width * health_percentage)

    # Create a rectangle representing the outline of the health bar
    outline_rect = pygame.Rect(x, y, bar_width, bar_height)

    # Create a rectangle representing the filled part of the health bar
    fill_rect = pygame.Rect(x, y, fill_width, bar_height)

    # Set the colors for the health bar
    fill_color = (255, 0, 0)  # Red
    outline_color = (255, 255, 255)  # White

    # Draw the filled part of the health bar on the screen
    pygame.draw.rect(screen, fill_color, fill_rect)

    # Draw the outline of the health bar on the screen
    pygame.draw.rect(screen, outline_color, outline_rect, 2)  # The last argument is the line thickness
