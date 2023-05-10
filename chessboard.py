import chess
import random


PIECES = {
    "pawn": chess.PAWN,
    "knight": chess.KNIGHT, 
    "bishop": chess.BISHOP,
    "rook": chess.ROOK,
    "queen": chess.QUEEN,
    "king": chess.KING
}

class Chessboard:
    def __init__(self, player_color, agent1, agent2, verbose = True):
        self.board = chess.Board()
        # self.minimaxagent = MinimaxAgent(player_color, self.board, eval)
        self.player_color = player_color
        self.agent1 = agent1
        self.agent1.board = self.board
        self.agent2 = agent2
        self.agent2.board = self.board
        self.verbose = verbose
    
    # print out the board
    def display(self):
        display = self.render(self.board)
        print(display)
        # print(self.board)
        print("")
    
    # Attribution: adapted from https://github.com/healeycodes/andoma/blob/main/ui.py
    def render(self, board: chess.Board) -> str:
        """
        Print a side-relative chess board with special chess characters.
        Currently only works if you're playing white, oops
        """
        board_string = list(str(board))
        # admittedly this looks a little odd on dark mode...
        uni_pieces = {
            "R": "♖",
            "N": "♘",
            "B": "♗",
            "Q": "♕",
            "K": "♔",
            "P": "♙",
            "r": "♜",
            "n": "♞",
            "b": "♝",
            "q": "♛",
            "k": "♚",
            "p": "♟",
            ".": "·",
        }
        for idx, char in enumerate(board_string):
            if char in uni_pieces:
                board_string[idx] = uni_pieces[char]
        ranks = ["1", "2", "3", "4", "5", "6", "7", "8"]
        display = []
        for rank in "".join(board_string).split("\n"):
            rank_num = ranks.pop()
            rank_disp = " " + rank_num + "  " + rank
            if self.player_color == chess.BLACK:
                rank_disp = " " + rank_num + "  " + "".join(reversed(rank))
            display.append(rank_disp)
        if self.player_color == chess.BLACK:
            display.reverse()
        files = "    a b c d e f g h"
        if self.player_color == chess.BLACK:
            files = "    h g f e d c b a"
        display.append(files)
        return "\n" + "\n".join(display)

    # make a move:
    def move(self, agent):
        move = agent.get_move()
        if agent.name != "player" and self.verbose:
            print("Computer makes move:", self.board.san(move))
        self.board.push(move) 
        
        if self.verbose:
            self.display()
    
    def is_end(self):
        if self.board.is_game_over():   
            # Will need to clean this up
            print(self.board.outcome())
            return True
        # else
        return False

