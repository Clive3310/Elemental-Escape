import json
import pathlib
from src.constants import *


def save_level_data(level_id: int, key: str, new_data):
    player_data = None
    try:
        with open(pathlib.Path(__file__).absolute().parent / "player_data.json", "r") as player_data_json:
            player_data = json.load(player_data_json)
    except FileNotFoundError:
        print("Save error: player_data wasn't found")
        return
    if str(level_id) in player_data["Levels"].keys():
        if key in player_data["Levels"][str(level_id)].keys():
            player_data["Levels"][str(level_id)][key] = new_data
        else:
            print("Save error: wrong key")
            return
    else:
        print("Save error: wrong level ID")
        return
    with open(pathlib.Path(__file__).absolute().parent / "player_data.json", "w") as player_data_json:
        json.dump(player_data, player_data_json, indent=2)


def load_level_data(level_id: int):
    player_data = None
    try:
        with open(pathlib.Path(__file__).absolute().parent / "player_data.json", "r") as player_data_json:
            player_data = json.load(player_data_json)
        if str(level_id) in player_data["Levels"].keys():
            return player_data["Levels"][str(level_id)]
        else:
            print("Load error: wrong key")
    except FileNotFoundError:
        print("Load error: player_data wasn't found")


def reset__all_data():
    try:
        with open(pathlib.Path(__file__).absolute().parent / "player_data.json", "w") as player_data_json:
            json.dump(BASE_LEVEL_DATA, player_data_json, indent=2)
    except FileNotFoundError:
        print("Reset error: player_data wasn't found")
        return


if __name__ == "__main__":
    reset__all_data()  # Удаляет ВСЁ!!!
