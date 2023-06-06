"""
FILE: play-chess.py
Author: Michelle Fu

Contains code for playing a console game.
"""

from chessboard import Chessboard
from ai.baseline import BaselineAgent
from ai.minimax import MinimaxAgent
from ai.model_only import ModelOnlyAgent
from player import Player

import sys
import chess

# the chess game lives here
def main():
    if len(sys.argv) < 2:
        print("Please specify an opponent type.")
        print("Opponents: baseline, base-minimax, fancy-minimax, linear-only, deep-only, linear-minimax, deep-minimax.")
        return
    
    # get the player's color
    white = True
    val = input("Welcome to chess! Type 'white' to play white and 'black' to play black. ")
    while True:
        if val == 'white': 
            print("Okay, you have the white pieces!")
            break
        elif val == 'black':
            print("Okay, you have the black pieces!")
            white = False
            break
        else:
            val = input("Invalid input: please type 'white' or 'black'. ")

    player_color = chess.WHITE if white else chess.BLACK
    opp_color = chess.BLACK if white else chess.WHITE

    opponent = None
    opponent_name = sys.argv[1]
    if opponent_name == 'baseline':
        opponent = BaselineAgent(opp_color, None)
    elif opponent_name == 'base-minimax':
        opponent = MinimaxAgent(opp_color, None, "simple")
    elif opponent_name == 'fancy-minimax':
        opponent = MinimaxAgent(opp_color, None, "fancy")
    elif opponent_name == "linear-only":
        opponent = ModelOnlyAgent(opp_color, None, "linear")
    elif opponent_name == "deep-only":
        opponent = ModelOnlyAgent(opp_color, None, "deep")
    elif opponent_name == "linear-minimax":
        opponent = MinimaxAgent(opp_color, None, "linear")
    elif opponent_name == "deep-minimax":
        opponent = MinimaxAgent(opp_color, None, "deep")
    else:
        print("Invalid opponent. Please select one of baseline, base-minimax, fancy-minimax, linear-only, \
              deep-only, linear-minimax, deep-minimax")

    print("Let's get started!")
    print("")

    player = Player(player_color, None)
    board = Chessboard(player_color, player, opponent)
    board.display()

    # off to the races! 
    if player_color == chess.WHITE:
        while True:
            resign = board.move(player)
            if resign:
                print("White resigns! Black wins.")
                break
            if board.is_end(): break
            board.move(opponent)
            if board.is_end(): break
    else:
        while True:
            board.move(opponent)
            if board.is_end(): break
            resign = board.move(player)
            if resign:
                print("Black resigns! White wins.")
                break
            if board.is_end(): break

if __name__ == "__main__":
    main()