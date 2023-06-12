"""
FILE: minimax.py
Authors: Michelle Fu, Roger Xia

Contains the minimax agent.
"""
import chess
import chess.polyglot
import math
from ai.eval_fns import *
from ai.play_openings import *
from ai.multiclass import LinearModel
from ai.deep_net import DeepModel

PIECES = [
    chess.PAWN,
    chess.KNIGHT,
    chess.BISHOP,
    chess.ROOK,
    chess.QUEEN,
    chess.KING
]
PIECES_WEIGHTS = [100, 300, 300, 500, 900, 1]

class MinimaxAgent:
    """
    This agent calculates the best action using the minimax algorithm.
    """
    def __init__(self, color, board, eval):
        self.name = "minimax"
        self.depth = 2
        self.board = board
        self.isComputer = True
        self.color = color
        self.opponent_color = not color
        self.quiesce_on = False
        self.eval_fn = eval
        self.model = None
        if self.eval_fn == "linear":
            # self.model = LinearModel.load_from_checkpoint("lightning_logs/version_4/checkpoints/epoch=0-step=36294.ckpt", map_location=torch.device('cpu'))
            self.model = LinearModel.load_from_checkpoint("lightning_logs/version_4/checkpoints/epoch=0-step=36294.ckpt")
            self.model.eval()
        if self.eval_fn == "deep":
            # self.model = DeepModel.load_from_checkpoint("lightning_logs/version_5/checkpoints/epoch=0-step=36294.ckpt", map_location=torch.device('cpu'))
            self.model = DeepModel.load_from_checkpoint("lightning_logs/version_5/checkpoints/epoch=0-step=36294.ckpt")
            self.model.eval()
        self.book = chess.polyglot.MemoryMappedReader("Titans.bin")
        self.in_opening = True
            
    def eval(self, temp_board=False):
        if temp_board:
            board = self.temp_board
        else:
            board = self.board

        if self.eval_fn == "simple":
            score = eval_material_count(board, self.color, self.opponent_color)
        elif self.eval_fn == "fancy":
            score = eval_material_count(board, self.color, self.opponent_color) + eval_pieceSquare_tables(board, self.color)
            + evaluate_pawn_structure(board, self.color) + evaluate_king_safety(board, self.color)
        elif self.eval_fn == "linear":
            score = eval_linear(board, self.color, self.model)
        else:
            score = eval_deep(board, self.color, self.model)

        return score
    
    def get_move(self):
        def alphaBeta(board, isComputer, currDepth, alpha, beta):
            if board.is_game_over():
                outcome = board.outcome()
                # if the computer won
                if outcome.winner == self.color:
                    return math.inf
                # if the player won -> bad for computer
                elif outcome.winner == self.opponent_color:
                    return -math.inf
                # stalemate
                return 0

            # we've bottomed out, so call the eval function/quiesce
            elif currDepth == 0:
                if self.quiesce_on == True:
                    return self.quiesce(alpha, beta, board, 2)
                eval = self.eval()
                return eval

            # minimax
            else:
                legalMoves = self.order_moves(board, list(board.legal_moves))
                #legalMoves = list(board.legal_moves)
                if isComputer:
                    maxValue = -math.inf
                    for action in legalMoves:
                        board.push(action)
                        value = alphaBeta(board, not isComputer, currDepth - 1, alpha, beta)
                        board.pop()

                        maxValue = max(maxValue, value)
                        if maxValue >= beta:
                            break
                        alpha = max(alpha, maxValue)
                    return maxValue

                else:
                    minValue = math.inf
                    for action in legalMoves:
                        board.push(action)
                        value = alphaBeta(board, not isComputer, currDepth - 1, alpha, beta)
                        board.pop() 

                        minValue = min(minValue, value)
                        if minValue <= alpha:
                            break
                        beta = min(beta, minValue)
                    return minValue

        # Play openings
        if self.in_opening:
            if self.book.get(self.board) is None:
                self.in_opening = False
            else:
                move = self.book.weighted_choice(self.board).move
                return move

        legalMoves = self.order_moves(self.board, list(self.board.legal_moves))
        legalMoves = list(self.board.legal_moves)
        maxAction = legalMoves[0]
        maxValue = -math.inf
        alpha = -math.inf
        beta = math.inf
        for action in legalMoves:
            self.board.push(action)
            value = alphaBeta(self.board, not self.isComputer, self.depth, alpha, beta)
            self.board.pop()
            # print(self.board.san(action), ":", value)

            if value > maxValue:
                maxAction = action
                maxValue = value
                alpha = max(alpha, maxValue)

        return maxAction

    def quiesce(self, alpha, beta, board, depth):
        # if depth == 0 or board.is_game_over():
        #     return self.eval()

        cur_score = self.eval()

        if cur_score >= beta:
            return beta

        if alpha < cur_score:
            alpha = cur_score

        # Generate capturing moves
        captures = [move for move in board.legal_moves if board.is_capture(move)]
        captures = self.order_moves(board, captures)
        print(captures)

        for move in captures:
            board.push(move)
            score = -self.quiesce(-beta, -alpha, board, depth - 1)
            board.pop()

            if score >= beta:
                return beta

            if score > alpha:
                alpha = score

        return alpha

    # Function to order moves based on a simple heuristic
    def order_moves(self, board, moves):
        ordered_moves = []
        for move in moves:
            # Perform a simple evaluation of the move
            score = self.evaluate_move(board, move)
            ordered_moves.append((move, score))

        # Sort the moves based on the scores in descending order
        ordered_moves.sort(key=lambda x: x[1], reverse=True)

        # Extract the ordered moves from the list of tuples
        ordered_moves = [move for move, _ in ordered_moves]
        return ordered_moves

    def evaluate_move(self, board, move):
        # Make the move on a temporary board
        self.temp_board = board.copy()
        self.temp_board.push(move)

        # Calculate the material difference after the move
        material_diff = self.eval(temp_board=True) - self.eval()

        # Calculate other factors you want to consider for move evaluation
        # For example, piece-square tables, pawn structure, king safety, etc.

        # Combine the factors into an overall score for the move
        # move_score = material_diff + other_factors_score(temp_board)

        return material_diff
        # return move_score
