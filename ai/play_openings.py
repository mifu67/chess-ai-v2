"""
FILE: play_openings.py
Author: Roger Xia

Contains opening moves for agent to play when encountered.
"""
import chess

def play_openings(board):
    def ruy_lopez(board):
        if board.fen() == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1":
            return board.parse_san("e4")
        elif board.fen() == "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1":
            return board.parse_san("e5")
        elif board.fen() == "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2":
            return board.parse_san("Nf3")
        elif board.fen() == "rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2":
            return board.parse_san("Nc6")
        elif board.fen() == "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3":
            return board.parse_san("Bb5")

    def queens_gambit(board):
        if board.fen() == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1":
            return board.parse_san("d4")
        elif board.fen() == "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1":
            return board.parse_san("d5")
        elif board.fen() == "rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 2":
            return board.parse_san("c4")
            
    openings = [ruy_lopez, queens_gambit]
    for opening in openings:
        move = opening(board)
        if move != None:
            return move