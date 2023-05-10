"""
FILE: player.py
Author: Michelle Fu

Contains code for the console player agent.
"""

class Player:
    def __init__(self, color, board):
        self.name = "player"
        self.color = color
        self.board = board

    def get_move(self):
        move_input = input("Please enter your move in standard algebraic notation. Type 'help' for examples. Type 'quit' to resign. ")
        if move_input.strip() == "help":
            print("e4, Nf3, Qxb4, bxc6, 0-0, Nfd2")
        elif move_input.strip() == "quit":
            return "quit"
        while True:
            try:
                move = self.board.parse_san(move_input.strip())
                break
            except ValueError:
                move_input = input("Oops, that input was illegal. Please try again. ")
        print(self.board.san(move))
        return move