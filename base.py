import pygame
from colors import WHITE, BLACK, RED  # Import specific colors as needed
import settings

class Base:
    def __init__(self, x, y, name, health, value):
        self.x = x
        self.y = y
        self.name = name
        self.value = value
        self.health = health
        self.max_health = health
        self.width = 60
        self.height = 80
        self.alive = True
        self.level = 1

    def take_damage(self, amount, player_base, current_round, level_details):
        self.health -= amount
        print(self.name +":" + str(self.health))
        if self.health < 0:
            self.health = 0
            self.alive = False
            if self.name == "EnemyBase":
                current_round.gold += level_details["enemy_base_value"]
                screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
                gold_text = settings.myfont.render('Gold: ' + str(current_round.gold), False, WHITE)
                screen.blit(gold_text, (0, 30))  # Adjust position as needed
    
    def reset(self, health, food_rate, base_gold, food_level, avialble_units):
        self.alive = True
        self.health = 100
        self.max_health = health
        self.food_rate = food_rate
        self.gold = base_gold
        self.food_level = food_level
        self.available_units = avialble_units

    def draw(self, screen):
        # Draw the base as a simple rectangle for now
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))
        # Health bar above the base
        health_bar_width = (self.health / self.max_health) * self.width
        pygame.draw.rect(screen, (255,0,0), (self.x, self.y - 10, health_bar_width, 5))
        if self.name == "EnemyBase":
            enemy_base_hp_text = settings.smallfont.render(str(self.health)+"hp", False, RED)
            screen.blit(enemy_base_hp_text,(self.x + 20, self.y - 30))

class PlayerBase(Base):
    def __init__(self, x, y):
        super().__init__(x, y, name="PlayerBase", health=100, value = 1)
        self.food_rate = .1  # Base rate of food generation per second
        #self.food = 0  # Initial amount of food
        self.gold = 0  # Initial amount of gold
        self.food_level = 0
        self.available_units = ["warrior"]


    def generate_food(self, dt):
        """Generate food based on the elapsed time (dt in seconds)."""
        self.food += self.food_rate * dt

    def spend_food(self, amount):
        """Spend a certain amount of food if available."""
        if self.food >= amount:
            self.food -= amount
            return True
        return False
    

class EnemyBase(Base):
    def __init__(self, x, y, level_details):
        super().__init__(x, y, name="EnemyBase", health=level_details["base_hp"], value = level_details["enemy_base_value"])
        self.spawn_rate = level_details["spawn_rate"]
        self.units = level_details["enemies"]
        self.deployed = 0
        self.delay = level_details["spawn_delay"]
