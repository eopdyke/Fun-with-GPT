class Round:
    def __init__(self, player_base, enemy_base, level_details):
        self.player_base = player_base
        self.enemy_base = enemy_base
        self.food = 0  # Round-specific food
        self.gold = 0
        self.level = level_details["level"]
        self.spawned_enemies = []  # Track enemies spawned this round
        self.food_generation_period = 1 /self.player_base.food_rate  # Seconds to generate 1 food unit
        self.enemy_power = level_details["power"]
        self.enemy_health = level_details["hp"]


    def reset_for_new_round(self, level_details):
        # Reset or initialize round-specific stats
        #self.player_base = 'waiting'
        #self.enemy_base = 'waiting'
        self.food = 0# Reset food to some initial value
        self.gold = 0
        self.food = level_details["start_food"]
        self.spawned_enemies.clear()  # Clear enemies from the previous round
        # Potentially reset other round-specific states here

    def generate_food(self):
        # Similar to player_base.generate_food but round-specific
        self.food += 1
        print("generated 1 food")

    def spawn_enemy(self):
        # Logic to spawn an enemy and add it to spawned_enemies
        pass

    def process_end_of_round(self, player_base):
        self.player_base.gold += self.gold

    def buy_unit(self, food_cost):
        self.food -= food_cost
        print("Bought unit for "+str(food_cost))