import pygame
from colors import  WHITE, BLACK, RED, DARK_GREY, STEEL_BLUE # Import specific colors as needed
import settings
import math
import sys

class Unit:
    def __init__(self, x, y, level_details, name, health, speed, attack_power, value, attack_speed):
        self.x = x
        self.y = y
        self.name = name
        self.value = value
        self.health = health
        self.speed = speed
        self.attack_power = attack_power
        self.width = 20  # You can adjust the unit's width and height as needed
        self.height = 20
        self.max_health = health  # Keep track of the max health for the health bar calculation
        self.alive = True
        self.engaged = False  # Add this line
        self.attack_speed = attack_speed
        self.last_attack_time = 0
        if self.name == "enemy":
            self.health = level_details["hp"]
            self.max_health = level_details["hp"]
            self.attack_power = level_details["power"]
            self.speed = level_details["speed"]
            self.value = level_details["enemy_value"]
            self.attack_speed = level_details["attack_speed"]
            self.last_attack_time = 0
            self.type = "enemy"

    def move(self, target_x):
        # Move towards a target x position
        if self.x < target_x:
            self.x += min(self.speed, target_x - self.x)
        elif self.x > target_x:
            self.x -= min(self.speed, self.x - target_x)

    def take_damage(self, amount, player_base, current_round, level_details):
        self.health -= amount
        if self.health <= 0:
            self.alive = False
            self.engaged = False
            if self.name == "enemy":
                current_round.gold += level_details["enemy_value"]
                screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
                gold_text = settings.myfont.render('Gold: ' + str(current_round.gold), False, WHITE)
                screen.blit(gold_text, (0, 30))  # Adjust position as needed
                

    def attack(self, target, player_base, current_round, current_time, level_details):
        # Check if enough time has passed since the last attack
        if current_time - self.last_attack_time >= (self.attack_speed * 1000):  # Convert seconds to milliseconds
            diff = current_time - self.last_attack_time
            #print("Diff: "+str(int(diff)))
            #print("Attack: "+ str(int(self.attack_speed * 1000)))
            #print("Attacking now")
            if self.type == "warrior":
                if self.sword_angle <= 90:
                    self.sword_angle += 90
                    target.take_damage(self.attack_power, player_base, current_round, level_details)
                    self.engaged = True
                    self.last_attack_time = current_time  # Update the time of the last attack
                    
                else:
                    self.sword_angle = 0

            target.take_damage(self.attack_power, player_base, current_round, level_details)
            self.engaged = True
            self.last_attack_time = current_time  # Update the time of the last attack

    def attack_base(self, base, player_base, current_round, current_time, level_details):
        # Check if enough time has passed since the last attack
        if current_time - self.last_attack_time >= self.attack_speed * 1000:  # Convert seconds to millisecond
        # Attack the base if the unit is not already engaged with another unit
            if self.alive and base.alive:
                base.take_damage(self.attack_power, player_base, current_round, level_details)
                self.engaged = True
                self.last_attack_time = current_time  # Update the time of the last attack

    def draw(self, screen, color):
        if self.type in ("archer", "enemy_archer"):
            # Calculate the center position of the unit
            center_x = self.x + self.width // 2
            center_y = self.y + self.height // 2

            # Define points for the triangle
            point1 = (center_x, self.y)  # Top center point
            point2 = (self.x, self.y + self.height)  # Bottom left point
            point3 = (self.x + self.width, self.y + self.height)  # Bottom right point

            # Draw the triangle
            pygame.draw.polygon(screen, color, [point1, point2, point3])

        elif self.type == "warrior":
            body_center = (self.x + self.width // 2, self.y + self.height // 2)
            body_size = (20, 40)
            body_rect = pygame.Rect(body_center[0] - body_size[0] // 2, body_center[1] - body_size[1] // 2, *body_size)
            pygame.draw.rect(screen, DARK_GREY, body_rect)

            # Draw the swordsman's head
            head_radius = 10
            pygame.draw.circle(screen, DARK_GREY, (body_center[0], body_center[1] - body_size[1] // 2 - head_radius), head_radius)

            # Calculate and draw the swordsman's sword
            sword_length = 40
            sword_end_x = body_center[0] + sword_length * math.sin(math.radians(self.sword_angle))
            sword_end_y = body_center[1] - sword_length * math.cos(math.radians(self.sword_angle))
            pygame.draw.line(screen, STEEL_BLUE, (body_center[0], body_center[1] - body_size[1] // 2), (sword_end_x, sword_end_y), 5)
       
        else:
            # Default drawing for other units
            pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

        # Health bar (common for all units)
        health_ratio = self.health / self.max_health
        health_bar_width = self.width * health_ratio
        health_bar_height = 5  # Height of the health bar; you can adjust as needed
        pygame.draw.rect(screen, RED, (self.x, self.y - health_bar_height - 2, health_bar_width, health_bar_height))

    def shoot_arrow(self, target, player_base, current_round, current_time, level_details):
        if self.alive and self.ready_to_shoot:
            # Check if enough time has passed since the last attack
            if current_time - self.last_attack_time >= self.attack_speed * 1000:  
                self.ready_to_shoot = False
                self.last_attack_time = current_time  # Update the time of the last attack

                # Create and shoot the arrow
                start_pos = (self.x + self.width / 2, self.y + self.height / 2)
                target_pos = (target.x + target.width / 2, target.y + target.height / 2)
                self.current_arrow = Arrow(start_pos, target_pos, 100)  # Adjust speed as needed
                self.projectiles.append(self.current_arrow)

                # Apply damage immediately or upon arrow hit based on your game's design
                #target.take_damage(self.attack_power, player_base, current_round, level_details)

class Arrow:
    def __init__(self, start_pos, target_pos, speed):
        self.x, self.y = start_pos
        self.target_x, self.target_y = target_pos
        self.speed = speed
        self.alive = True

    def update(self, dt):
        # Calculate the direction vector
        direction_x, direction_y = self.target_x - self.x, self.target_y - self.y
        distance = (direction_x**2 + direction_y**2)**0.5
        direction_x, direction_y = direction_x/distance, direction_y/distance

        # Update the arrow's position
        self.x += direction_x * self.speed * dt
        self.y += direction_y * self.speed * dt

        # Check if the arrow has reached its target or gone off-screen
        if distance < 10 or not (0 <= self.x <= settings.SCREEN_WIDTH and 0 <= self.y <= settings.SCREEN_HEIGHT):
            self.alive = False

    def draw(self, screen):
        pygame.draw.line(screen, RED, (self.x, self.y), (self.x + 5, self.y), 2)


class FriendlyUnit(Unit):
    def __init__(self, x, y, level_details, unit_type):
        super().__init__(x, y, level_details, name="friendly", health=100, speed=1, attack_power=10, value=1, attack_speed=1)
        self.type = unit_type
        if unit_type == "warrior":
            self.cost = 5
            self.attack_power = 5
            self.attack_speed = 3
            self.sword_angle = 0
        elif unit_type == "archer":
            self.cost = 7
            self.attack_power = 15
            self.range = 300  # Example range, adjust as needed
            self.projectiles = []
            self.ready_to_shoot =True
            self.current_arrow = None
            self.attack_speed = 3
            self.hp = 40
            self.speed = .5
        elif unit_type == "horseback":
            self.cost = 15
            self.attack_power = 20
            self.speed = .30
            self.attack_speed = 4



class EnemyUnit(Unit):
    def __init__(self, x, y, level_details, unit_type):
        super().__init__(x, y, level_details, name="enemy", health=level_details["hp"], speed=level_details["speed"], attack_power=level_details["power"], value=level_details["enemy_value"], attack_speed=level_details["attack_speed"])
        self.type = unit_type
        if unit_type == "enemy_warrior":
            self.cost = 5
            self.attack_power = 5
            self.attack_speed = 3
            self.sword_angle = 0
        elif unit_type == "enemy_archer":
            self.cost = 7
            self.attack_power = 15
            self.range = 300  # Example range, adjust as needed
            self.projectiles = []
            self.ready_to_shoot =True
            self.current_arrow = None
            self.attack_speed = 3
            self.hp = 40
            self.speed = .5
        elif unit_type == "enemy_horseback":
            self.cost = 15
            self.attack_power = 20
            self.speed = .30
            self.attack_speed = 4
        # Additional attributes or methods specific to enemy units