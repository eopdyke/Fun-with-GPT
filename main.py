import pygame
import sys
from base import PlayerBase, EnemyBase  # Ensure this matches your actual file and class names
from colors import WHITE, BLACK, RED  # Import specific colors as needed
from units import FriendlyUnit, EnemyUnit
import time
import upgradesystem
import settings
from round_state import Round
from buttons import Button
import save_and_load
from fsm import GameState

def check_game_fsm(game_fsm):
    print("------------------")
    for attribute in dir(game_fsm):
        if not attribute.startswith('__'):
            print(f"{attribute}: {getattr(game_fsm, attribute)}")
    
    print("------------------")


def check_friendlies(friendlies):
    print("------------------")
    for soldier in friendlies:
        print("Name: "+soldier.type)
    
    print("------------------")

def check_units(player_base):
    warrior = 1
    archer = 2
    horseman = 4
    calc = 0
    for unit_type in player_base.available_units:
        if unit_type == "warrior":
            calc += 1
        elif unit_type == "archer":
            calc += 2
        elif unit_type == "horseman":
            calc +=4
    return calc

def main_menu(game_fsm, screen, player_base):
    global loaded_level, loaded_level_flag

    menu_running = True
    while menu_running:
        screen.fill(BLACK)
        options = ["Start Next Round", "Go to Upgrade Menu", "Save Game", "Load Game","Exit Game"]
        for i, option in enumerate(options):
            menu_text = settings.myfont.render(f"{i+1}. {option}", False, WHITE)
            screen.blit(menu_text, (settings.SCREEN_WIDTH // 2 - 100, 200 + i * 40))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_fsm.start_playing()
                    # Start Next Round
                    return 'start'
            
                elif event.key == pygame.K_2:
                    # Go to Upgrade Menu
                    game_fsm.upgrade(upgrade_system)
                    # Return to the main menu after upgrades

                elif event.key == pygame.K_3:
                    # save Game
                    game_state = {
                        'player_base': {
                            'health': player_base.health,
                            'food_rate': player_base.food_rate,
                            'gold': player_base.gold,
                            'food_level': player_base.food_level,
                            'available_units': player_base.available_units
                        },
                        'current_level': player_base.level,
                        # Add more attributes as necessary
                    }
                    save_and_load.save_game(game_state)
                    print(game_state)

                elif event.key == pygame.K_4:
                    # load Game
                    loaded_state = save_and_load.load_game()
                    player_base.health = loaded_state['player_base']['health']
                    player_base.food_rate = loaded_state['player_base']['food_rate']
                    player_base.gold = loaded_state['player_base']['gold']
                    player_base.food_level = loaded_state['player_base']['food_level']
                    print("food level is reported as "+str(player_base.food_level))
                    player_base.available_units = loaded_state['player_base']["available_units"]
                    loaded_level_flag = True
                    loaded_level = loaded_state['current_level']
                    print("loaded save file")

                elif event.key == pygame.K_5:
                    # Exit Game
                    return 'exit'

def reset_game_state(level, player_base, game_fsm):
    global current_round, enemy_base, enemy_units, friendly_units, level_details, player_base_rect, enemy_base_rect, progress_bar_y
    global first_enemy_spawned, time_since_last_update, last_enemy_spawn_time, last_update_time, loaded_level_flag, progress_bar_x
    global progress_bar_width, progress_bar_height, progress_bar_fill

    print(str(game_fsm.state))
    check_game_fsm(game_fsm)

    # Time tracking for food generation
    time_since_last_update = 0
    last_enemy_spawn_time = pygame.time.get_ticks()  # Get the current time in milliseconds
    last_update_time = pygame.time.get_ticks() 

    try:
        if loaded_level_flag:
            level = loaded_level
            print("Loading level "+ str(loaded_level))
            print("loaded gamestate is "+str(game_fsm.state))
    except NameError:
        loaded_level_flag = False

    # Reinitialize the enemy base with its starting attributes
 
    level_details = settings.levels[level-1]

    
    enemy_base = EnemyBase(settings.SCREEN_WIDTH - 80, settings.SCREEN_HEIGHT / 2 - 40, level_details)

    print(str(game_fsm.state))
    if game_fsm.state == GameState.DEFEAT or game_fsm.state == GameState.MAIN_MENU:
        print("building new base")
        base_health = player_base.max_health
        base_food_rate = player_base.food_rate
        base_gold = player_base.gold
        food_level = player_base.food_level
        available_units = player_base.available_units
        player_base = PlayerBase(20, settings.SCREEN_HEIGHT / 2 - 40)
        print(str(player_base.food_rate))
        player_base.reset(base_health, base_food_rate, base_gold, food_level, available_units)
        print(str(player_base.food_rate))
    elif game_fsm.state == GameState.PLAYING:
        pass

    player_base_rect = pygame.Rect(player_base.x, player_base.y, player_base.width, player_base.height)
    enemy_base_rect = pygame.Rect(enemy_base.x, enemy_base.y, enemy_base.width, enemy_base.height)
    
    current_round = Round(player_base, enemy_base, level_details)
    current_round.reset_for_new_round(level_details)  # Prepare for the round

    print("current level is "+ str(current_round.level))
    print("Enemy power: "+str(current_round.enemy_power))
    print("Enemy HP: "+str(current_round.enemy_health))
    print("Base HP "+str(player_base.health))
    print("PlayerBase.alive = "+str(player_base.alive))
    # Clear the lists of units for a fresh start
    print("Length of Enemies is: "+str(len(enemy_units)))
    print("Length of Friendlies is: "+str(len(friendly_units)))
    enemy_units.clear()
    friendly_units.clear()  # Optionally clear this list if you want to reset friendly units as well
    print("Length of Enemies is: "+str(len(enemy_units)))
    print("Length of Friendlies is: "+str(len(friendly_units)))

    #friendly_spawn_x = player_base.x + player_base.width  # Spawn to the right of the player base
    #friendly_spawn_y = player_base.y + player_base.height // 2 - 10
    #friendly_units.append(FriendlyUnit(friendly_spawn_x, friendly_spawn_y, level_details))

    first_enemy_spawned = False  # Reset the flag at the start of each round
    loaded_level_flag = False

    if player_base.health < player_base.max_health:
        print("Resetting base health")
        player_base.health = player_base.max_health

    game_fsm.start_playing()

    # Progress bar properties
    progress_bar_x = 150  # X position
    progress_bar_y = 5  # Y position
    progress_bar_width = 200  # Total width
    progress_bar_height = 20  # Height
    progress_bar_fill = 0  # Current fill level (0 to progress_bar_width)
    # Time tracking for food generation

    return player_base

def spawn_initial_enemy_units():
    global last_enemy_spawn_time, first_enemy_spawned

    current_time = pygame.time.get_ticks()
    
    # Apply the initial delay only for the first enemy spawn of the round
    if not first_enemy_spawned:
        if (current_time - last_enemy_spawn_time) >= (enemy_base.delay * 1000):
            first_enemy_spawned = True  # Update the flag after the first spawn
    else:
        if (current_time - last_enemy_spawn_time) >= (enemy_base.spawn_rate * 1000):
            # Spawn logic for subsequent enemies without the initial delay
            if enemy_base.deployed < enemy_base.units:
                enemy_spawn_x = enemy_base.x - 20
                enemy_spawn_y = enemy_base.y + enemy_base.height // 2 - 10
                if enemy_base.deployed in (5,6,12,13,17):
                    print("sending out an archer")
                    enemy_units.append(EnemyUnit(enemy_spawn_x, enemy_spawn_y, level_details, "enemy_archer"))
                else:
                    enemy_units.append(EnemyUnit(enemy_spawn_x, enemy_spawn_y, level_details, "enemy_warrior"))
                enemy_base.deployed += 1
                print(str(enemy_base.deployed))
                last_enemy_spawn_time = current_time  # Update the time of the last spawn

def evaluate_end_round(victory, game_fsm, player_base):
    print("evaluting round")
    global screen
    #print(str(current_round.gold))
    current_round.process_end_of_round(player_base)
    #print(str(player_base.gold))
    if victory:
        game_fsm.state = GameState.VICTORY
        print("Victory - You Won!")
        print("Before Upgrade, food level is: "+str(player_base.food_level))
        upgrade_system.display_end_of_round_screen(True, player_base)
        print("your victory state is "+str(game_fsm.state))
        player_base.level += 1
        action = main_menu(game_fsm, screen, player_base)
        print("User selected "+action)
        if action == 'start':
            # Reinitialize for next round
            print("The current level is: "+str(current_round.level))
            reset_game_state(current_round.level + 1, player_base, game_fsm)
        elif action == 'exit':
            pygame.quit()
            sys.exit()
        
    else:
        game_fsm.defeat()
        print("Game Over - You Lost!")
        print("Before Upgrade, food level is: "+str(player_base.food_level))
        upgrade_system.display_end_of_round_screen(False, player_base )
        print("Did we change "+str(game_fsm.state))
        #reset_game_state(current_round.level)
        #print(current_round.health)
        print("Before MM -")
        print(player_base.available_units)
        action = main_menu(game_fsm, screen, player_base)
        print("User selected "+action)
        print("still in end_round")
        if action == 'start':
            game_fsm.defeat()
            # Reinitialize for next round
            #game_running = False
            #print("The current level is: "+str(current_round.level))
            player_base = reset_game_state(current_round.level, player_base, game_fsm)
            game(game_fsm, player_base)
        elif action == 'exit':
            pygame.quit()
            sys.exit()

def setup_game(game_fsm):
    global clock, friendly_units, enemy_units, progress_bar_fill, progress_bar_height, progress_bar_width, progress_bar_y, progress_bar_x
    global upgrade_system, exit_round, screen, buy_warrior, buy_horseman, buy_archer

    pygame.init()
    pygame.font.init()  

    # Screen dimensions
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

    clock = pygame.time.Clock()

    # Instantiate bases
    player_base = PlayerBase(20, settings.SCREEN_HEIGHT / 2 - 40)
    #enemy_base = EnemyBase(settings.SCREEN_WIDTH - 80, settings.SCREEN_HEIGHT / 2 - 40)

    # Initialize Upgrade System
    upgrade_system = upgradesystem.UpgradeSystem(player_base, screen, settings.myfont)
    # Initialize unit lists
    friendly_units = []
    enemy_units = []


    exit_round = Button(RED, 850, 5, 100, 100, 'Exit Round')
    buy_warrior = Button(RED, 550, 600, 100, 100, 'Buy Warrior')
    buy_archer = Button(RED, 650, 600, 100, 100, 'Buy Archer')
    buy_horseman = Button(RED, 750, 600, 100, 00, 'Buy Horseback')

    # Progress bar properties
    progress_bar_x = 150  # X position
    progress_bar_y = 5  # Y position
    progress_bar_width = 200  # Total width
    progress_bar_height = 20  # Height
    progress_bar_fill = 0  # Current fill level (0 to progress_bar_width)
    # Time tracking for food generation

    # Game state
    level = 1

    action = main_menu(game_fsm, screen, player_base)
    if action == 'start':
        player_base = reset_game_state(level, player_base, game_fsm)  # Resets the game state for the next round
        print("Game is reset")
        print(str(player_base.food_level))
        game(game_fsm, player_base)
    elif action == 'exit':
        pygame.quit()
        sys.exit()

def get_target_in_range(friendly, enemy_units, enemy_base):
    # Initialize closest target and its distance
    closest_target = None
    min_distance = float('inf')

    # Check distance to each enemy unit
    for enemy in enemy_units:
        distance = ((friendly.x - enemy.x) ** 2 + (friendly.y - enemy.y) ** 2) ** 0.5
        if distance <= friendly.range and distance < min_distance:
            closest_target = enemy
            min_distance = distance

    # Check distance to enemy base
    distance_to_base = ((friendly.x - enemy_base.x) ** 2 + (friendly.y - enemy_base.y) ** 2) ** 0.5
    if distance_to_base <= friendly.range and distance_to_base < min_distance:
        closest_target = enemy_base

    return closest_target

def game(game_fsm, player_base):
    pygame.display.flip()
    print(str(player_base.alive))
    print(player_base.available_units)
    global current_round, enemy_base, enemy_units, friendly_units, level_details, player_base_rect, enemy_base_rect
    global first_enemy_spawned, time_since_last_update, last_enemy_spawn_time, last_update_time, loaded_level_flag
    global clock, progress_bar_fill, progress_bar_height, progress_bar_width, progress_bar_y, progress_bar_x
    global upgrade_system, exit_round, buy_horseman, buy_archer, buy_warrior
    check_game_fsm(game_fsm)
    while game_fsm.state == GameState.PLAYING:
        current_time = pygame.time.get_ticks()
        dt = (current_time - last_update_time) /1000   # Calculate the delta time since last frame
        last_update_time = current_time


        spawn_initial_enemy_units()

        #generate food
        time_since_last_update += dt

        fill_rate_per_second = progress_bar_width / current_round.food_generation_period
        #print(f"Before Fill Update: Fill: {progress_bar_fill}, dt: {dt}")
        progress_bar_fill += fill_rate_per_second * dt 
        # Ensure the progress bar is drawn after screen.fill and before pygame.display.flip()
        
        # If the bar is full, reset it and increment the food
        #print(f"Food Rate: {player_base.food_rate}, Fill: {progress_bar_fill}, Period: {food_generation_period}")
        progress_bar_fill = max(0, progress_bar_fill)
        #print(f"After Fill Update: Fill: {progress_bar_fill}")
        if progress_bar_fill >= progress_bar_width:
            current_round.generate_food()
            progress_bar_fill = 0  # Reset the progress bar
            time_since_last_update = 0  # Reset the timer

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_round.is_over(pos):
                    print("user requested exit!")
                    game_fsm.state = GameState.DEFEAT
                
                elif buy_warrior.is_over(pos):
                    if current_round.food >= settings.unit_types["warrior_cost"]: # Assuming a unit costs 10 food
                        # Spawn a unit
                        friendly_units.append(FriendlyUnit(player_base.x + player_base.width, player_base.y + player_base.height // 2 - 10, level_details, "warrior"))
                        current_round.buy_unit(settings.unit_types["warrior_cost"])
                        check_friendlies(friendly_units)
                elif buy_archer.is_over(pos):
                    check_unit = check_units(player_base)
                    print(str(int(check_unit)))
                    if check_unit in (2, 3, 6):
                        print("I shouldnt be here")
                        if current_round.food >= settings.unit_types["archer_cost"]: # Assuming a unit costs 10 food
                            # Spawn a unit
                            friendly_units.append(FriendlyUnit(player_base.x + player_base.width, player_base.y + player_base.height // 2 - 10, level_details, "archer"))
                            current_round.buy_unit(settings.unit_types["archer_cost"])
                            check_friendlies(friendly_units)
                        else:
                            print("You have the unit tech but not enough food")
                    else:
                        print("You dont have the tech")

                elif buy_horseman.is_over(pos):
                    if current_round.food >= settings.unit_types["horseback_cost"]: # Assuming a unit costs 10 food
                        # Spawn a unit
                        friendly_units.append(FriendlyUnit(player_base.x + player_base.width, player_base.y + player_base.height // 2 - 10, level_details, "horseback"))
                        current_round.buy_unit(settings.unit_types["horseback_cost"])
                        check_friendlies(friendly_units)

        #Update and manage archer arrows
        for friendly in friendly_units:
            if friendly.type == "archer":
                # Existing code for managing current_arrow and ready_to_shoot
                if friendly.current_arrow is not None:
                    if not friendly.current_arrow.alive:
                        friendly.ready_to_shoot = True  # Arrow has hit or is no longer active; ready to shoot again
                        friendly.current_arrow = None  # Clear the current arrow reference
                    else:
                        # Update and draw the arrow if it's still active
                        friendly.current_arrow.update(dt)

        # Existing event loop and screen clearing code
        screen.fill(BLACK)
        
        # Process friendly units
        for friendly in friendly_units:
            friendly_engaged = False
            friendly_rect = pygame.Rect(friendly.x, friendly.y, friendly.width, friendly.height)
        
            if friendly.type == "archer":
                target = get_target_in_range(friendly, enemy_units, enemy_base)
                if target:
                    #print("Target in range!")
                    friendly.shoot_arrow(target, player_base, current_round, current_time, level_details)
                    friendly_engaged = True
                    
                    # Update and draw current arrow, if it exists
                    if friendly.current_arrow is not None:
                        friendly.current_arrow.update(dt)
                        if not friendly.current_arrow.alive:
                            friendly.ready_to_shoot = True
                            friendly.current_arrow = None
                        else:
                            friendly.current_arrow.draw(screen)
                    
                    # Update and draw projectiles
                    for arrow in friendly.projectiles[:]:
                        arrow.update(dt)
                        arrow_rect = pygame.Rect(arrow.x, arrow.y, 5, 2)  # Assuming arrow size for collision detection
                        
                        target_rect = pygame.Rect(target.x, target.y, target.width, target.height)
                        if arrow_rect.colliderect(target_rect):
                            target.take_damage(friendly.attack_power, player_base, current_round, level_details)
                            arrow.alive = False
                        
                        if arrow.alive:
                            arrow.draw(screen)
                        else:
                            friendly.projectiles.remove(arrow)
                
            else:
                #print("I'm a "+ str(friendly.type))
                # Check collision with enemy units
                for enemy in enemy_units:
                    enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                    if friendly_rect.colliderect(enemy_rect):
                        # If there is a collision with an enemy unit, engage and attack
                        friendly.attack(enemy, player_base, current_round, current_time, level_details)
                        enemy.attack(friendly, player_base, current_round, current_time, level_details)
                        friendly_engaged = True
                        break  # Stop checking other enemies since we're already engaged

                # Check collision with the enemy base
                if not friendly_engaged and friendly_rect.colliderect(enemy_base_rect):
                    # If there is a collision with the base and not engaged with enemy units, attack the base
                    friendly.attack_base(enemy_base, player_base, current_round, current_time, level_details)
                    friendly_engaged = True
            

            # If not engaged with either enemy units or the base, move towards the enemy base
            if not friendly_engaged:
                if friendly.type == "warrior":
                    friendly.sword_angle = 0
                friendly.move(settings.SCREEN_WIDTH)
            
            for friendly in friendly_units:
                friendly.draw(screen, WHITE)

        # Process enemy units with similar logic
        for enemy in enemy_units:
            enemy_engaged = False
            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)

            if enemy.type == "enemy_archer":
                target = get_target_in_range(enemy, friendly_units, player_base)
                if target:
                    #print("Target in range!")
                    enemy.shoot_arrow(target, enemy_base, current_round, current_time, level_details)
                    enemy_engaged = True
                    
                    # Update and draw current arrow, if it exists
                    if enemy.current_arrow is not None:
                        enemy.current_arrow.update(dt)
                        if not enemy.current_arrow.alive:
                            enemy.ready_to_shoot = True
                            enemy.current_arrow = None
                        else:
                            enemy.current_arrow.draw(screen)
                    
                    # Update and draw projectiles
                    for arrow in enemy.projectiles[:]:
                        arrow.update(dt)
                        arrow_rect = pygame.Rect(arrow.x, arrow.y, 5, 2)  # Assuming arrow size for collision detection
                        
                        target_rect = pygame.Rect(target.x, target.y, target.width, target.height)
                        if arrow_rect.colliderect(target_rect):
                            target.take_damage(enemy.attack_power, enemy_base, current_round, level_details)
                            arrow.alive = False
                        
                        if arrow.alive:
                            arrow.draw(screen)
                        else:
                            enemy.projectiles.remove(arrow)
                
            else:
                for friendly in friendly_units:
                    friendly_rect = pygame.Rect(friendly.x, friendly.y, friendly.width, friendly.height)
                    if enemy_rect.colliderect(friendly_rect):
                        enemy.attack(friendly, player_base, current_round, current_time, level_details)
                        friendly.attack(enemy, player_base, current_round,current_time, level_details)
                        enemy_engaged = True
                        break  # Stop checking other friendlies since we're already engaged

            if not enemy_engaged and enemy_rect.colliderect(player_base_rect):
                enemy.attack_base( player_base, enemy_base, current_round, current_time, level_details)
                enemy_engaged = True

            if not enemy_engaged:
                enemy.move(0)

            enemy.draw(screen, RED)

        if not player_base.alive:
            print("no base anymore")
            evaluate_end_round(False, game_fsm, player_base)

        elif not enemy_base.alive:
            evaluate_end_round(True, game_fsm, player_base)


        # Draw bases, remove dead units, update display, and tick clock
        player_base.draw(screen)
        enemy_base.draw(screen)
        friendly_units = [unit for unit in friendly_units if unit.alive]
        enemy_units = [unit for unit in enemy_units if unit.alive]
        food_text = settings.myfont.render('Food: ' + str(int(current_round.food)), False, WHITE)
        gold_text = settings.myfont.render('Gold: ' + str(current_round.gold), False, WHITE)
        level_text = settings.myfont.render('Level: ' + str(current_round.level), False, WHITE)
        food_speed_text = settings.smallfont.render(str(player_base.food_rate)+"/s", False, RED)

        screen.blit(food_text, (0, 0))  # Adjust position as needed
        screen.blit(gold_text, (0, 30))  # Adjust position as needed
        screen.blit(level_text, (150, 30))  # Adjust position as needed
        screen.blit(food_speed_text,(360,5))

        exit_round.draw(screen, BLACK)
        for unit_type in player_base.available_units:
            #print("Checking if you can buy that unit")
            #print(player_base.available_units)
            #print("Checking unit: "+unit_type)
            if unit_type.lower()== "warrior" and buy_warrior:
                buy_warrior.draw(screen, BLACK)
            elif unit_type.lower()== "archer" and buy_archer:
                buy_archer.draw(screen, BLACK)
            elif unit_type.lower() == "horseback" and buy_horseman:
                buy_horseman.draw(screen, BLACK)

        pygame.draw.rect(screen, WHITE, (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height))
        # Draw the filled portion
        pygame.draw.rect(screen, RED, (progress_bar_x, progress_bar_y, progress_bar_fill, progress_bar_height))
        for friendly in friendly_units:
            if friendly.type == "archer" and friendly.current_arrow is not None:
            # Draw the arrow if it's still active
                friendly.current_arrow.draw(screen)
         
        pygame.display.flip()
        clock.tick(settings.FPS)


