"""
FILE: baseline.py
Author: Michelle Fu

Contains the agent that only uses the AI for move generation (no search).
"""

import chess
import random
import torch
from ai.multiclass import LinearModel
from ai.deep_net import DeepModel
from ai.eval_fns import eval_linear, eval_deep

class ModelOnlyAgent:
    """
    This agent plays a random legal move.
    """
    def __init__(self, color : chess.Color, board : chess.Board, eval : str) -> None:
        self.name = "model-only"
        self.board = board
        self.color = color
        self.eval_fn = eval
        if self.eval_fn == "linear":
            self.model = LinearModel.load_from_checkpoint("lightning_logs/version_4/checkpoints/epoch=0-step=36294.ckpt", map_location=torch.device('cpu'))
        elif self.eval_fn == "deep":
            self.model = DeepModel.load_from_checkpoint("lightning_logs/version_5/checkpoints/epoch=0-step=36294.ckpt", map_location=torch.device('cpu'))
        self.model.eval()

    def get_move(self):
        legal_moves = list(self.board.legal_moves)
    
        if self.eval_fn == "linear":
            positive_moves = []
            neutral_moves = []
            negative_moves = []
            for move in legal_moves:
                # print(self.board.san(move))
                self.board.push(move)
                score = eval_linear(self.board, self.color, self.model)
                # print(score)
                if score == 1:
                    positive_moves.append(move)
                elif score == 0:
                    neutral_moves.append(move)
                else:
                    negative_moves.append(move)
                self.board.pop()
            if len(positive_moves) > 0:
                return random.choice(positive_moves)
            elif len(neutral_moves) > 0:
                return random.choice(neutral_moves)
            else:
                return random.choice(negative_moves)
        
        else:
            # I'll vectorize this if it's too slow
            max_score = -1000
            best_move = None
            for move in legal_moves:
                print(self.board.san(move))
                self.board.push(move)
                score = eval_deep(self.board, self.color, self.model)
                print(score)
                if score > max_score:
                    max_score = score
                    best_move = move
            return best_move
        
    def get_move_object(self):
        return self.get_move()