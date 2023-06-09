"""
FILE: eval_fns.py
Author: Roger Xia

Contains evaluation functions for the minimax agent.
"""
import chess
import numpy as np
import torch
from process_data import fen_to_vec

PIECES = [
    chess.PAWN,
    chess.KNIGHT,
    chess.BISHOP,
    chess.ROOK,
    chess.QUEEN,
    chess.KING
]
PIECES_WEIGHTS = [100, 300, 300, 500, 900, 1]

def eval_material_count(board, color, opponent_color):
    my_count = 0
    opp_count = 0
    for i in range(len(PIECES)):
        my_count += PIECES_WEIGHTS[i] * len(board.pieces(PIECES[i], color))
        opp_count += PIECES_WEIGHTS[i] * len(board.pieces(PIECES[i], opponent_color))
    score = my_count - opp_count
    return score

def eval_pieceSquare_tables(board, color):
    # Piece-square tables (PSQT) for evaluation
    pawn_table = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    knight_table = [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-30, 5, 15, 20, 20, 15, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ]

    bishop_table = [
        [-20,-10,-10,-10,-10,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5, 10, 10,  5,  0,-10],
        [-10,  5,  5, 10, 10,  5,  5,-10],
        [-10,  0, 10, 10, 10, 10,  0,-10],
        [-10, 10, 10, 10, 10, 10, 10,-10],
        [-10,  5,  0,  0,  0,  0,  5,-10],
        [-20,-10,-10,-10,-10,-10,-10,-20]
    ]

    rook_table = [
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 5, 10, 10, 10, 10, 10, 10,  5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [ 0,  0,  0,  5,  5,  0,  0,  0]
    ]

    queen_table = [
        [-20,-10,-10, -5, -5,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5,  5,  5,  5,  0,-10],
        [ -5,  0,  5,  5,  5,  5,  0, -5],
        [  0,  0,  5,  5,  5,  5,  0, -5],
        [-10,  5,  5,  5,  5,  5,  0,-10],
        [-10,  0,  5,  0,  0,  0,  0,-10],
        [-20,-10,-10, -5, -5,-10,-10,-20]
    ]

    king_table_midgame = [
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-20,-30,-30,-40,-40,-30,-30,-20],
        [-10,-20,-20,-20,-20,-20,-20,-10],
        [ 20, 20,  0,  0,  0,  0, 20, 20],
        [ 20, 30, 10,  0,  0, 10, 30, 20]
    ]

    king_table_endgame = [
        [-50,-40,-30,-20,-20,-30,-40,-50],
        [-30,-20,-10,  0,  0,-10,-20,-30],
        [-30,-10, 20, 30, 30, 20,-10,-30],
        [-30,-10, 30, 40, 40, 30,-10,-30],
        [-30,-10, 30, 40, 40, 30,-10,-30],
        [-30,-10, 20, 30, 30, 20,-10,-30],
        [-30,-30,  0,  0,  0,  0,-30,-30],
        [-50,-30,-30,-30,-30,-30,-30,-50]
    ]

    # Function to calculate the score of a position based on the piece-square tables
    def evaluate_position(board):
        score = 0
        for row in range(8):
            for col in range(8):
                piece = board.piece_at(chess.square(col, row))
                if piece is not None:
                    piece_value = get_piece_value(piece)
                    if piece.color == chess.WHITE:
                        score += piece_value + get_piece_square_value(board, piece, row, col)
                    else:
                        score -= piece_value + get_piece_square_value(board, piece, 7 - row, col)
        return score

    # Function to get the value of a piece
    def get_piece_value(piece):
        if piece.piece_type == chess.PAWN:
            return 100
        elif piece.piece_type == chess.KNIGHT:
            return 320
        elif piece.piece_type == chess.BISHOP:
            return 330
        elif piece.piece_type == chess.ROOK:
            return 500
        elif piece.piece_type == chess.QUEEN:
            return 900
        elif piece.piece_type == chess.KING:
            return 20000

    # Function to get the piece-square value for a specific piece on a specific square
    def get_piece_square_value(board, piece, row, col):
        piece_table = None
        if piece.piece_type == chess.PAWN:
            piece_table = pawn_table
        elif piece.piece_type == chess.KNIGHT:
            piece_table = knight_table
        elif piece.piece_type == chess.BISHOP:
            piece_table = bishop_table
        elif piece.piece_type == chess.ROOK:
            piece_table = rook_table
        elif piece.piece_type == chess.QUEEN:
            piece_table = queen_table
        elif piece.piece_type == chess.KING and get_game_phase(board) == "Endgame":
            piece_table = king_table_endgame
        else:
            piece_table = king_table_midgame
        
        if piece.color == chess.WHITE:
            return piece_table[row][col]
        else:
            return piece_table[7 - row][col]

    def get_game_phase(board):
        # Count the number of remaining pieces
        piece_counts = board.piece_map().values()
        total_pieces = len(piece_counts)

        # Determine the phase based on the number of remaining pieces
        if total_pieces <= 12:
            return "Endgame"
        elif total_pieces <= 24:
            return "Midgame"
        else:
            return "Opening"

    score = evaluate_position(board)
    if color == chess.WHITE:
        #print(score)
        return score
    #print(score)
    return -score

def evaluate_pawn_structure(board, color):
    score = 0

    # Evaluate pawn structure for both players
    pawn_ranks = board.pawns & board.occupied_co[color]

    # Doubled pawns
    doubled_pawns = 0

    for file in range(8):
        pawns_in_file = board.pieces(chess.PAWN, color) & chess.BB_FILES[file]
        pawns_list = list(pawns_in_file)
        if len(pawns_list) > 1:
            doubled_pawns += len(pawns_list) - 1

    score -= doubled_pawns * 10

    # Isolated pawns
    """isolated_pawns = pawn_ranks & ~(pawn_ranks << 1) & ~(pawn_ranks >> 1)
    print(isolated_pawns) # TODO: fix isolated_pawns
    score -= isolated_pawns * 20"""

    # Passed pawns
    """passed_pawns = 0
    enemy_pawn_ranks = board.pawns & board.occupied_co[not color]
    for square in chess.scan_reversed(pawn_ranks):
        if not enemy_pawn_ranks & chess.SquareSet(chess.pawn_attacks(color, square)): #TODO: pawn_attacks
            passed_pawns |= chess.square_file(square)
    score += bin(passed_pawns).count('1') * 20"""
    #print(score)
    return score

def evaluate_king_safety(board, color):
    score = 0

    # Get the square of the king for both players
    if color == chess.WHITE:
        white_king_square = board.king(chess.WHITE)
        
        # King safety for White
        white_king_file = chess.square_file(white_king_square)
        white_king_rank = chess.square_rank(white_king_square)

        # Penalize if the king is exposed on the back rank
        if white_king_rank == 0:
            score -= 20

        # Penalize if the king is exposed on the file adjacent to the center
        if white_king_file == 3 or white_king_file == 4:
            score -= 10

    else:
        black_king_square = board.king(chess.BLACK)
        # King safety for Black
        black_king_file = chess.square_file(black_king_square)
        black_king_rank = chess.square_rank(black_king_square)

        # Penalize if the king is exposed on the back rank
        if black_king_rank == 7:
            score -= 20

        # Penalize if the king is exposed on the file adjacent to the center
        if black_king_file == 3 or black_king_file == 4:
            score -= 10
    #print(score)
    return score

def eval_linear(board, color, model):
    cuda0 = torch.device('cuda:0')
    model.eval()
    # pos = torch.from_numpy(fen_to_vec(board.fen()).astype(np.single))
    pos = torch.from_numpy(fen_to_vec(board.fen()).astype(np.single)).to(cuda0)
    eval = torch.argmax(model(pos)) - 1
    if color == chess.BLACK:
        eval = -eval
    return eval

def eval_deep(board, color, model):
    cuda0 = torch.device('cuda:0')
    model.eval()
    # pos = torch.from_numpy(fen_to_vec(board.fen()).astype(np.single))
    pos = torch.from_numpy(fen_to_vec(board.fen()).astype(np.single)).to(cuda0)
    eval = model(pos)
    if color == chess.BLACK:
        eval = -eval
    return eval
