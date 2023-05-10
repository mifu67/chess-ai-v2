import chess
import math

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
    def __init__(self, color, board):
        self.name = "minimax"
        self.depth = 2
        self.board = board
        self.isComputer = True
        self.color = color
        self.opponent_color = not color
    
    def eval(self):
        my_count = 0
        opp_count = 0
        for i in range(len(PIECES)):
            my_count += PIECES_WEIGHTS[i] * len(self.board.pieces(PIECES[i], self.color))
            opp_count += PIECES_WEIGHTS[i] * len(self.board.pieces(PIECES[i], self.opponent_color))
        return my_count - opp_count
    
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
                # if self.quiesce_on == True:
                #     return self.quiesce(alpha, beta, board, 3)
                eval = self.eval()
                return eval

            # minimax
            else:
                # legalMoves = self.order_moves(list(board.legal_moves))
                legalMoves = list(board.legal_moves)
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

        # legalMoves = self.order_moves(list(self.board.legal_moves))
        legalMoves = list(self.board.legal_moves)
        maxAction = legalMoves[0]
        maxValue = -math.inf
        alpha = -math.inf
        beta = math.inf
        for action in legalMoves:
            self.board.push(action)
            value = alphaBeta(self.board, not self.isComputer, self.depth, alpha, beta)
            self.board.pop()
            print(self.board.san(action), ":", value)

            if value > maxValue:
                maxAction = action
                maxValue = value
                alpha = max(alpha, maxValue)

        return maxAction