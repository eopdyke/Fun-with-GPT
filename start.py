from fsm import GameFSM
import main
import settings

def start_game():
    fsm = GameFSM()
    print(str(fsm.state))
    main.setup_game(fsm)


start_game()