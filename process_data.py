import csv 
import chess
import numpy as np
from tqdm import tqdm

# convert to 1-hot vec of length 772
def fen_to_vec(pos):
    board = chess.Board(fen=pos)
    wp = board.pieces(chess.PAWN, chess.WHITE)
    wn = board.pieces(chess.KNIGHT, chess.WHITE)
    wb = board.pieces(chess.BISHOP, chess.WHITE)
    wr = board.pieces(chess.ROOK, chess.WHITE)
    wq = board.pieces(chess.QUEEN, chess.WHITE)
    wk = board.pieces(chess.KING, chess.WHITE)

    bp = board.pieces(chess.PAWN, chess.BLACK)
    bn = board.pieces(chess.KNIGHT, chess.BLACK)
    bb = board.pieces(chess.BISHOP, chess.BLACK)
    br = board.pieces(chess.ROOK, chess.BLACK)
    bq = board.pieces(chess.QUEEN, chess.BLACK)
    bk = board.pieces(chess.KING, chess.BLACK) 

    bitboards = np.array([wp, wn, wb, wr, wq, wk, bp, bn, bb, br, bq, bk], dtype = np.uint64)

    board_array = bitboards_to_array(bitboards)
    color = 1 if board.turn == chess.WHITE else 0
    K = 1 if board.has_kingside_castling_rights(chess.WHITE) else 0
    Q = 1 if board.has_queenside_castling_rights(chess.WHITE) else 0
    k = 1 if board.has_kingside_castling_rights(chess.BLACK) else 0
    q = 1 if board.has_queenside_castling_rights(chess.BLACK) else 0

    vec = np.append(board_array, [color, K, Q, k, q])
    return vec

def bitboards_to_array(bitboards):
    bb = np.asarray(bitboards, dtype=np.uint64)[:, np.newaxis]
    s = 8 * np.arange(7, -1, -1, dtype=np.uint64)
    b = (bb >> s).astype(np.uint8)
    b = np.unpackbits(b, bitorder="little").astype(np.single)
    return b

# def main():
#     csv_data = csv.reader(open('chess-data-test.csv', 'r'))
#     csv_new = csv.writer(open('chess-data-processed.csv', 'w'))

#     for i, row in tqdm(enumerate(csv_data)):
#         if i == 0:
#             row.append("Encoding")
#             row.append("Label")
#             csv_new.writerow(row)
#         else:
#             fen = row[0]
#             eval = row[1]
#             if eval == "0": # remove examples with evaluation of 0 for simplicity
#                 continue
#             if eval[0:2] == "#-":
#                 row[1] = -15000 # giving it a large numerical value
#             if eval[0:2] == "#+":
#                 row[1] = 15000
#             row[1] = int(row[1])/100 # convert to pawns from centipawns
#             encoding = fen_to_vec(fen)
#             label = max(np.sign(int(row[1])), 0)
#             row.append(encoding)
#             row.append(label)
#             csv_new.writerow(row)


if __name__ == "__main__":
    main()