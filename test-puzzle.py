"""
FILE: test-puzzle.py
Author: Roger Xia

Test performance of agent against lichess puzzles.
"""
from chessboard import Chessboard
import chess
import sys
import pandas as pd

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

# TODO: run puzzle
def run_puzzle(board : Chessboard, white, black) -> int:
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
    """
    Command format: python test-puzzle.py <agent> <puzzles.csv>
    """
    args = sys.argv
    agent = args[1]

    agent_wins = 0

    puzzles_df = pd.read_csv(args[2])

    for index, row in puzzles_df.iterrows()::
        FEN = row['FEN']

        # TODO: set up chessboard according to puzzle
        if active_move == white:
            white = init_agent(agent, chess.WHITE)
        else:
            black = init_agent(agent, chess.BLACK)
        board = Chessboard(None, white, black, verbose=False)
        board.board = chess.Board(fen)

        # TODO: run puzzle
        winner = run_puzzle(board, white, black)

        board.display()

        if winner == 1:
            agent_wins += 1
    print("Agent wins:", agent_wins)

if __name__ == "__main__":
    main()