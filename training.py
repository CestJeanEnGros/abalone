import argparse
import asyncio
import os
from os.path import basename, splitext, dirname
import platform
import sys
import json
from loguru import logger
from board_abalone import BoardAbalone
from player_abalone import PlayerAbalone
from master_abalone import MasterAbalone
from game_state_abalone import GameStateAbalone
from seahorse.player.proxies import InteractivePlayerProxy, LocalPlayerProxy, RemotePlayerProxy
from seahorse.utils.gui_client import GUIClient
from seahorse.utils.recorders import StateRecorder
from seahorse.game.game_layout.board import Piece
from seahorse.utils.custom_exceptions import PlayerDuplicateError
from main_abalone import play

log_level = "DEBUG"
port = 16001
address= "localhost"
gui = False
record = True
config = "classic"
gui_path = os.path.join(dirname(os.path.abspath(__file__)),'GUI','index.html')
time_limit = 15*60
list_players = ["my_player.py", "my_player1.py"]
folder = dirname(list_players[0])
sys.path.append(folder)
player1_class = __import__(splitext(basename(list_players[0]))[0], fromlist=[None])
folder = dirname(list_players[1])
sys.path.append(folder)
player2_class = __import__(splitext(basename(list_players[1]))[0], fromlist=[None])
player1 = player1_class.MyPlayer("W", name=splitext(basename(list_players[0]))[0]+"_1", time_limit=time_limit)
player2 = player2_class.MyPlayer("B", name=splitext(basename(list_players[1]))[0]+"_2", time_limit=time_limit)
print(gui_path)

record_file = None
record_file = play(player1=player1, player2=player2, log_level=log_level, port=port, address=address, gui=gui, record=record, gui_path=gui_path, config=config)+".json"

with open(record_file, 'r') as f:
    data = json.load(f)

print(data)