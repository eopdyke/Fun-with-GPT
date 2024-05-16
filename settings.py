import pygame
pygame.font.init()  
# Initialize font module


myfont = pygame.font.SysFont('Comic Sans MS', 30)  # Create a font object
smallfont =  pygame.font.SysFont('Comic Sans MS', 15)  # Create a font object
# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

# Game settings
FPS = 60

unit_types =  {"warrior_cost": 5, "archer_cost": 7, "horseback_cost":13}


def generate_levels():
  levels = [
      {"level": 1, "start_food": 5, "unit_cost": 5, "spawn_rate": 10, "enemies": 20, "power": 12, "hp": 25, "speed": 1,
      "base_hp": 500, "spawn_delay": 0, "enemy_value": 12, "enemy_base_value": 20, "attack_speed": 3.2, "warriors": 15, "archers": 5},
  ]

  power_increase_rate = 1.1
  hp_increase_rate = 1.1
  base_hp_increase = 50
  enemy_value_increase = 1
  enemy_base_value_increase = 5
  warrior_increase = 2
  archer_increase = 2

  for level in range(2, 51):
      prev_level = levels[-1]
      new_level = {
          "level": level,
          "start_food": 5,
          "unit_cost": 5,
          "spawn_rate": round(max(1, prev_level["spawn_rate"] - 0.2), ),  # Ensuring spawn rate doesn't go below 1
          "enemies": 20,
          "power": int(prev_level["power"] * power_increase_rate),
          "hp": int(prev_level["hp"] * hp_increase_rate),
          "speed": 1,
          "base_hp": prev_level["base_hp"] + base_hp_increase,
          "spawn_delay": round(min(10, prev_level["spawn_delay"] + 0.2), 2),  # Cap at 10 seconds
          "enemy_value": prev_level["enemy_value"] + enemy_value_increase,
          "enemy_base_value": prev_level["enemy_base_value"] + enemy_base_value_increase,
          "attack_speed": 0.7,
          "warriors": prev_level["warriors"] + warrior_increase,
          "archers": prev_level["archers"] + archer_increase,
      }
      levels.append(new_level)
  return levels

levels = generate_levels()