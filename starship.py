import pygame
import sys
import random

pygame.init()
SPAWNENEMY = pygame.USEREVENT + 1
clock = pygame.time.Clock()

# Game window dimensions
width = 800
height = 600

# Set up the display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Starship Game')

UPGRADE_COSTS = {
    "health": 50,
    "speed": 75,
    "magnet_radius": 100
}

def spawn_new_pos(sprite, width, height):
    sprite.rect.x = random.randrange(width - sprite.rect.width)
    sprite.rect.y = random.randrange(-100, -40)
    sprite.speedy = random.randrange(1, 4)

class FlashText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, size, color, duration=500):
        super().__init__()
        self.font = pygame.font.Font(None, size)
        self.image = self.font.render(str(text), True, color)  # Convert the f-string to a string
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.duration = duration
        self.creation_time = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.creation_time > self.duration:
            self.kill()

class UpgradeMenu:
    def __init__(self, player, screen):
        self.player = player
        self.screen = screen
        self.upgrades = [
            {"name": "Health", "cost": 20, "effect": lambda: setattr(player, "health", min(player.health + 25, 100))},
            {"name": "Speed", "cost": 30, "effect": lambda: setattr(player, "speed", player.speed + 1)},
            {"name": "Magnet Radius", "cost": 40, "effect": lambda: setattr(player, "magnet_radius", player.magnet_radius + 25)},
            {"name": "Weapon Upgrade", "cost": 50, "effect": self.upgrade_weapon},
            {"name": "Continue", "cost": 0, "effect": lambda: None}
        ]
        self.selected = 0

    def draw(self):
         # Display player's stats on the screen
        draw_text(self.screen, f"Score: {score}", 60, 10)
        draw_text(self.screen, f"Health: {player.health}", 60, 40)
        draw_text(self.screen, f"Speed: {player.speed}", 60, 70)
        draw_text(self.screen, f"Magnet Radius: {player.magnet_radius}", 60, 100)
        draw_text(self.screen, f"Fire Rate: {player.fire_rate}", 60, 130)

        draw_text(self.screen, f"Damage Rate: {player.damage}", 60, 160)


        for i, upgrade in enumerate(self.upgrades):
            upgrade_name = upgrade['name']
            cost = upgrade['cost']
            color = (255, 0, 0) if self.player.money < cost else (255, 255, 255)  # Default color is white, change to red if not enough money
            if i == self.selected:
                color = (255, 255, 0)  # Keep the selected item yellow
            if cost == 0 and upgrade_name == "Continue":
                draw_text(self.screen, f"{upgrade_name}", self.screen.get_width() // 2, 100 + i * 50, color=color)
            else:
                draw_text(self.screen, f"{upgrade_name} - ${cost}", self.screen.get_width() // 2, 100 + i * 50, color=color)

        # Display player's money on the screen
        draw_text(self.screen, f"Money: ${self.player.money}", self.screen.get_width() // 2, self.screen.get_height() - 100)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.upgrades)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.upgrades)
            elif event.key == pygame.K_RETURN:
                selected_upgrade = self.upgrades[self.selected]
                cost = selected_upgrade['cost']

                if self.player.money >= cost:
                    self.player.money -= cost
                    selected_upgrade['effect']()

                    if selected_upgrade['name'] == "Continue":
                        return "next_level"  # Return a value to indicate the player wants to continue to the next level

            return None
        
    def upgrade_weapon(self):
        if self.player.fire_rate > 100:  # Don't let the fire rate go below 100ms
            self.player.fire_rate -= 100  # Decrease fire rate by 100ms
        if self.player.projectile_count < 3:  # Limit the number of projectiles to 3
            self.player.projectile_count += 1  # Increase the number of projectiles by 1
        self.player.damage += 1

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

class Enemy(pygame.sprite.Sprite):
   
    def __init__(self, current_level):
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
            player.health -= 10  # Reduce player health when an enemy reaches the bottom of the screen

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, player, damage_type="default"):
        super().__init__()
        self.image = pygame.Surface((4, 10))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10
        self.player = player
        self.damage = player.damage
        self.damage_type = damage_type

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > height:
            spawn_new_pos(self, width, height)

        # Attract power-up if within player's magnet_radius
        if pygame.sprite.collide_circle_ratio(player.magnet_radius / self.rect.width)(self, player):
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            distance = (dx**2 + dy**2)**0.5
            self.rect.x += int(dx / distance * 5)
            self.rect.y += int(dy / distance * 5)

class MainMenu:
    def __init__(self):
        self.options = ["Weapon Upgrades", "Ship Upgrades"]
        self.selected_option = 0

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option]

    def draw(self, screen):
        for index, option in enumerate(self.options):
            color = (255, 255, 255) if index == self.selected_option else (100, 100, 100)
            draw_text(screen, option, width // 2, 200 + index * 40, color=color)

class WeaponUpgrades(pygame.sprite.Sprite):
    def __init__(self, Player):
        super().__init__()
        self.player = Player
        self.upgrades = weapon_upgrades_list
        self.upgrades.append({"name": "Continue", "cost": 0, "effect": lambda: None})  # Add "Continue" option
        self.selected_upgrade = 0

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_upgrade = (self.selected_upgrade - 1) % len(self.upgrades)
            elif event.key == pygame.K_DOWN:
                self.selected_upgrade = (self.selected_upgrade + 1) % len(self.upgrades)
            elif event.key == pygame.K_RETURN:
                selected_upgrade = self.upgrades[self.selected_upgrade]
                cost = selected_upgrade['cost']

                if self.player.money >= cost:
                    self.player.money -= cost
                    selected_upgrade['effect']()

                    if selected_upgrade['name'] == "Continue":
                        return "main"

    def draw(self, screen):
        for index, upgrade in enumerate(self.upgrades):
            color = (255, 255, 255) if index == self.selected_upgrade else (100, 100, 100)
            draw_text(screen, f"{upgrade['name']} - Cost: {upgrade['cost']}", width // 2, 200 + index * 40, color=color)

    def apply_upgrade(self, upgrade):
        if upgrade['name'] == "Upgrade 1":
            # Apply the effects of Upgrade 1
            self.player.damage += 5
        elif upgrade['name'] == "Upgrade 2":
            # Apply the effects of Upgrade 2
            self.player.fire_rate -= 100
        # Add more upgrade logic here based on the upgrade's name

class ShipUpgrades(pygame.sprite.Sprite):
    def __init__(self, Player):
        super().__init__()
        self.player = Player
        self.upgrades = ship_upgrades_list
        self.upgrades.append({"name": "Back", "cost": 0, "effect": lambda: None})  # Add "Back" option
        self.selected_upgrade = 0

    def handle_input(self, key):
        if key == pygame.K_DOWN:
            self.selected += 1
            if self.selected >= len(self.upgrades):
                self.selected = 0
        elif key == pygame.K_UP:
            self.selected -= 1
            if self.selected < 0:
                self.selected = len(self.upgrades) - 1
        elif event.key == pygame.K_RETURN:
            selected_upgrade = self.upgrades[self.selected_upgrade]
            cost = selected_upgrade['cost']

            if self.player.money >= cost:
                self.player.money -= cost
                selected_upgrade['effect']()

                if selected_upgrade['name'] == "Back":
                    return "main"

    def draw(self, screen):
        for index, upgrade in enumerate(self.upgrades):
            color = (255, 255, 255) if index == self.selected_upgrade else (100, 100, 100)
            draw_text(screen, f"{upgrade['name']} - Cost: {upgrade['cost']}", width // 2, 200 + index * 40, color=color)

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

weapon_upgrades_list = [
{"name": "Upgrade 1", "cost": 100},
{"name": "Upgrade 2", "cost": 200},
{"name": "Upgrade 3", "cost": 300},
{"name": "Upgrade 4", "cost": 400},
{"name": "Upgrade 5", "cost": 500},
{"name": "Upgrade 6", "cost": 600},
{"name": "Upgrade 7", "cost": 700},
{"name": "Upgrade 8", "cost": 800},
{"name": "Upgrade 9", "cost": 900},
{"name": "Upgrade 10", "cost": 1000},
]

ship_upgrades_list = [
{"name": "Upgrade 1", "cost": 100},
{"name": "Upgrade 2", "cost": 200},
{"name": "Upgrade 3", "cost": 300},
{"name": "Upgrade 4", "cost": 400},
{"name": "Upgrade 5", "cost": 500},
{"name": "Upgrade 6", "cost": 600},
{"name": "Upgrade 7", "cost": 700},
{"name": "Upgrade 8", "cost": 800},
{"name": "Upgrade 9", "cost": 900},
{"name": "Upgrade 10", "cost": 1000},
]

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


def fire_projectile():
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


def draw_game_text():
    draw_text(screen, f"Score: {score}", width // 2, 10)
    draw_text(screen, f"Health: {player.health}", 60, 10)
    draw_text(screen, f"DMG: {player.damage}", 60, 40)
    draw_text(screen, f"Level: {current_level}", width - 60, 10)
    draw_text(screen, f"Money: {player.money}", width - 60, 40)  # New line to display money

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

enemies = pygame.sprite.Group()

projectiles = pygame.sprite.Group()

power_ups = pygame.sprite.Group()

score = 0
current_level = 1
enemies_killed = 0
enemies_to_kill = 5
enemy_spawn_delay = 4000

pygame.time.set_timer(SPAWNENEMY, enemy_spawn_delay)

last_shot = pygame.time.get_ticks()
fire_rate = player.fire_rate

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
            fire_projectile()

        if event.type == SPAWNENEMY:
            enemy = Enemy(current_level)
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
    draw_game_text()

    pygame.display.flip()

pygame.quit()