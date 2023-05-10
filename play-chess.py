from chessboard import Chessboard
from baseline import BaselineAgent
from minimax import MinimaxAgent
from player import Player

import chess

# the chess game lives here
def main():
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
    val = input("Choose your opponent's algorithm: type '1' for minimax, and '2' for deep MCTS. ")
    while True:
        if val == '1':
            opponent = MinimaxAgent(opp_color, None)
            break
        elif val == '2':
            print("haha, that's not implemented yet")
            break
        else:
            print("defaulting to random agent (for debugging)")
            opponent = BaselineAgent(opp_color, None)
            # val = input("Invalid input: please type '1' or '2'.")
            break 

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