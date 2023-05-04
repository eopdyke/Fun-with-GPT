import sys
import random
import pygame
from config import all_sprites, enemies_killed, current_level, screen, score, width, height, last_shot
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
    global current_level, enemies_killed, enemies_to_kill, enemy_spawn_delay
    current_level += 1
    enemies_killed = 0
    enemies_to_kill += 5

    if current_level % 3 == 0:
        enemy_spawn_delay = max(enemy_spawn_delay - 500, 500)
    pygame.time.set_timer(SPAWNENEMY, enemy_spawn_delay // current_level)

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
    global last_shot
    now = pygame.time.get_ticks()
    if now - last_shot > player.fire_rate:
        last_shot = now
        for i in range(player.projectile_count):
            offset_x = (i - (player.projectile_count - 1) / 2) * 20  # Position projectiles with a 20-pixel spacing
            projectile = Projectile(player.rect.centerx + offset_x, player.rect.top, player, player.damage_type)
            all_sprites.add(projectile)
            projectiles.add(projectile)


def handle_level_up():
    global current_level
    if enemies_killed == current_level * 5:
        current_level += 1
        level_up()

def draw_game_text(player):
    draw_text(screen, f"Score: {score}", width // 2, 10)
    draw_text(screen, f"Health: {player.health}", 60, 10)
    draw_text(screen, f"DMG: {player.damage}", 60, 40)
    draw_text(screen, f"Level: {current_level}", width - 60, 10)
    draw_text(screen, f"Money: {player.money}", width - 60, 40)  # New line to display money


def spawn_new_pos(sprite, width, height):
    sprite.rect.x = random.randrange(width - sprite.rect.width)
    sprite.rect.y = random.randrange(-100, -40)
    sprite.speedy = random.randrange(1, 4)
