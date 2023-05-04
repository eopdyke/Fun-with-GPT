import pygame


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
