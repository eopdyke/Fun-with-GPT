from enum import Enum, auto
import upgradesystem


class GameState(Enum):
    MAIN_MENU = auto()
    PLAYING = auto()
    PAUSE = auto()
    GAME_OVER = auto()
    VICTORY = auto()
    DEFEAT = auto()

class GameFSM:
    def __init__(self):
        self.state = GameState.MAIN_MENU

    def to_main_menu(self):
        self.state = GameState.MAIN_MENU
        #upgradesystem.main_menu(player_base, upgrade_system, screen)

    def start_playing(self):
        self.state = GameState.PLAYING

    def pause(self):
        self.state = GameState.PAUSE
        # Code to pause the game

    def game_over(self, victory):
        if victory:
            self.state = GameState.VICTORY
            # Code to handle victory scenario
        else:
            self.state = GameState.MAIN_MENU
    
    def upgrade(self, upgrade_system):
         upgrade_system.display_upgrade_options()

    def defeat(self):
        self.state = GameState.DEFEAT

    def update(self):
        if self.state == GameState.PLAYING:
            # Main game loop code
            pass
        elif self.state == GameState.MAIN_MENU:
            # Main menu handling code
            pass
    
    def check_state(self):
        return self.state
        # Implement update logic for other states as needed

