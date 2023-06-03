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

def run_puzzle(board : Chessboard, white, black, moves, active_move) -> int:
    winner = 0
    if active_move == 'w':
        agent_move = black
    else:
        agent_move = white

    for i in range(0, len(moves), 2):
        # make first puzzle move
        board.board.push(chess.Move.from_uci(moves[i]))
        agent_move.board = board.board

        # make agent move
        agent_move_object = agent_move.get_move()
        board.board.push(agent_move_object)
        agent_move.board = board.board

        print(agent_move_object.uci())
        print(moves[i+1])

        # if incorrect, agent loses and terminate
        if agent_move_object != chess.Move.from_uci(moves[i+1]):
            return winner

    winner = 1
    return winner

def main():
    """
    Command format: python test-puzzle.py <agent> <puzzles.csv> <num_puzzles>
    """
    args = sys.argv
    agent_name = args[1]

    agent_wins = 0

    puzzles_df = pd.read_csv(args[2])
    num_puzzles = int(args[3])

    for index, row in puzzles_df.head(num_puzzles).iterrows():
        FEN = row['FEN']
        split_FEN = FEN.strip().split(' ')
        active_move = split_FEN[1]
        moves = row['Moves']
        split_moves = moves.strip().split(' ')

        # set up chessboard according to puzzle
        white = init_agent(agent_name, chess.WHITE)
        black = init_agent(agent_name, chess.BLACK)
        board = Chessboard(None, white, black, verbose=False)
        board.board = chess.Board(FEN)

        # run puzzle
        winner = run_puzzle(board, white, black, split_moves, active_move)

        # display final board of puzzle
        board.display()

        if winner == 1:
            agent_wins += 1
    print("Agent wins:", agent_wins)

if __name__ == "__main__":
    main()