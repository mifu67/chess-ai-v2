"""
FILE: eval-chess.py
Author: Michelle Fu

Run evaluation by pitting two agents against each other.
"""
from chessboard import Chessboard
import chess
import sys

from baseline import BaselineAgent
from minimax import MinimaxAgent

def init_agent(agent_name, color):
    agent = None
    if agent_name == "baseline":
        agent = BaselineAgent(color, None)
    elif agent_name == "minimax":
        agent = MinimaxAgent(color, None)
    else:
        print("haha, that's not implemented yet")
    return agent

def get_outcome(board):
    outcome = board.board.outcome()
    if outcome.winner == chess.WHITE:
        return 1
    elif outcome.winner == chess.BLACK:
        return 0
    else:
        return 0.5

def run_game(board : Chessboard, white, black) -> int:
    winner = 0
    while True:
        board.move(white)
        if board.is_end():
            winner = get_outcome(board)
            break
        board.move(black)
        if board.is_end():
            winner = get_outcome(board)
            break
    return winner
            

def main():
    args = sys.argv
    white_type = args[1]
    white = init_agent(white_type, chess.WHITE)
    black_type = args[2]
    black = init_agent(black_type, chess.BLACK)

    white_wins = 0
    black_wins = 0
    draws = 0

    for i in range(int(args[3])):
        board = Chessboard(None, white, black, verbose=False)
        winner = run_game(board, white, black)
        board.display()
        if winner == 1:
            white_wins += 1
        elif winner == 0:
            black_wins += 1
        else:
            draws += 1
    print("White wins:", white_wins)
    print("Black wins:", black_wins)
    print("Draws:", draws)

if __name__ == "__main__":
    main()