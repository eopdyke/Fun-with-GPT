import pygame
from colors import WHITE, BLACK, RED  # Import specific colors as needed
import settings
import save_and_load

class UpgradeSystem:
    def __init__(self, player_base, screen, font):
        self.player_base = player_base
        self.screen = screen
        self.font = font
        self.upgrade_options = [
            {"description": "Increase unit health", "cost": 1000, "effect": self.increase_unit_health},
            {"description": "Increase food generation rate", "cost": int(self.player_base.food_level * 6), "effect": self.increase_food_rate},
            {"description": "Purchase new units", "cost":0}
            # Add more upgrade options as needed
        ]
        self.unit_options = [{"name":"Archer", "cost":500, "effect":"unit"}, {"name":"Horseback", "cost":1500, "effect":"unit"}]


    def display_end_of_round_screen(self, victory, player_base):
        self.player_base = player_base
        print("in here your level is"+str(self.player_base.food_level))
        # Clear the screen
        self.screen.fill(BLACK)

        if victory:
            message = "Victory! Choose your upgrade."
        else:
            message = "Defeat. Game Over."

        text_surface = self.font.render(message, False, WHITE)
        self.screen.blit(text_surface, (settings.SCREEN_WIDTH // 2 - 100, settings.SCREEN_HEIGHT // 2))

        pygame.display.flip()
        # Instead of pygame.time.wait(2000), consider a short loop that processes events
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 2000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.time.delay(100)  # Short delay to reduce CPU usage

        if victory:
            self.display_upgrade_options()
        else:
            self.display_upgrade_options()
        
        return self.player_base

    def update_upgrade_costs(self):
        # Example: Updating the cost of increasing food generation rate
        for option in self.upgrade_options:
            #print('well here it is '+str(self.player_base.food_level))
            if option["description"] == "Increase food generation rate":
                option["cost"] = int(self.player_base.food_level * 6)  # Recalculate cost based on the new food level`

    def display_upgrade_options(self):
        selecting = True
        print("Upgrade menu: "+str(self.player_base.gold))
        self.update_upgrade_costs()
        while selecting:
            self.screen.fill(BLACK)  # Clear the screen each time for updating

            # Display available gold
            account_balance = self.font.render(f"Gold: {self.player_base.gold}", False, WHITE)
            food_stats = self.font.render(f"Food Rate: {self.player_base.food_rate}/s", False, RED)
            health_stats = self.font.render(f"Base Health: {self.player_base.health}", False, RED)


            self.screen.blit(account_balance, (settings.SCREEN_WIDTH - 200, 10))
            self.screen.blit(food_stats, (settings.SCREEN_WIDTH - 250, 50))
            self.screen.blit(health_stats, (settings.SCREEN_WIDTH - 250, 100))

            
            # Display upgrade options
            for i, option in enumerate(self.upgrade_options):
                text_surface = self.font.render(f"{i+1}: {option['description']} (Cost: {option['cost']} Gold)", False, WHITE)
                self.screen.blit(text_surface, (50, 30 + i * 30))
            
            pygame.display.flip()  # Update the display after drawing everything

            # Event handling within the upgrade screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1 or event.key == pygame.K_2:
                        # Process the selection for the corresponding upgrade option
                        self.process_selection(int(event.unicode) - 1, self.upgrade_options)  # Converts key to index
                    elif event.key == pygame.K_3:
                        self.display_new_units()
                    elif event.key == pygame.K_ESCAPE:
                        # Let ESC key be the signal to exit upgrade screen
                        selecting = False


    def display_new_units(self):
        selecting = True
        print("Upgrade menu: "+str(self.player_base.gold))
        while selecting:
            self.screen.fill(BLACK)  # Clear the screen each time for updating
            account_balance = self.font.render(f"Gold: {self.player_base.gold}", False, WHITE)
            food_stats = self.font.render(f"Food Rate: {self.player_base.food_rate}/s", False, RED)
            health_stats = self.font.render(f"Base Health: {self.player_base.health}", False, RED)

            self.screen.blit(account_balance, (settings.SCREEN_WIDTH - 200, 10))
            self.screen.blit(food_stats, (settings.SCREEN_WIDTH - 250, 50))
            self.screen.blit(health_stats, (settings.SCREEN_WIDTH - 250, 100))

            # Display upgrade options
            self.update_upgrade_costs()
            for i, option in enumerate(self.unit_options):
                if not option["name"] in self.player_base.available_units:
                    text_surface = self.font.render(f"{i+1}: {option['name']} (Cost: {option['cost']} Gold)", False, WHITE)
                    self.screen.blit(text_surface, (50, 30 + i * 30))
                
            pygame.display.flip()  # Update the display after drawing everything

            # Event handling within the upgrade screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1 or event.key == pygame.K_2:
                        # Process the selection for the corresponding upgrade option
                        self.process_selection(int(event.unicode) - 1, self.unit_options)  # Converts key to index
                    elif event.key == pygame.K_ESCAPE:
                        # Let ESC key be the signal to exit upgrade screen
                        selecting = False


    def increase_unit_health(self):
        # Implement the logic to increase unit health globally
        pass

    def increase_food_rate(self):
        self.player_base.food_rate += 0.02
        self.player_base.food_rate = round(self.player_base.food_rate, 2)
        self.player_base.food_level += 1

    def process_selection(self, selection, parent_list):
        if 0 <= selection < len(parent_list):
            option = parent_list[selection]
            if self.player_base.gold >= option["cost"]:
                self.player_base.gold -= option["cost"]
                if option["effect"] == "unit":
                    self.player_base.available_units.append(option["name"])
                else:
                    option["effect"]()  # Apply the effect of the upgrade
                    self.update_upgrade_costs()
            else:
                print("Not enough gold for this upgrade.")  # Adjust for in-game message display
