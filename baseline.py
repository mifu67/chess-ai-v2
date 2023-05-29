import chess
import random

class BaselineAgent:
    """
    This agent plays a random legal move.
    """
    def __init__(self, color : chess.Color, board : chess.Board) -> None:
        self.name = "baseline"
        self.board = board
        self.color = color

    def get_move(self):
        legal_moves = list(self.board.legal_moves)
        return random.choice(legal_moves)

    def get_move_object(self):
        return self.get_move()