import json

def save_game(state, file_name='savegame.json'):
    with open(file_name, 'w') as f:
        json.dump(state, f)
    print("saved game!")

def load_game(file_name='savegame.json'):
    with open(file_name, 'r') as f:
        return json.load(f)
