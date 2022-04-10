import chess
import chess.svg
import numpy as np

class ChessDriver:
    def __init__(self, board: chess.Board):
        self.board = board

    def get_legal_moves_list(self):
        return [self.board.san(move) for move in self.board.legal_moves]

    def make_move(self, move_string: str):
        self.board.push_san(move_string)

    def undo_move(self):
        self.board.pop()

    def validate_move(self, move_string: str):
        try:
            self.board.parse_san(move_string)
        except:
            return False

        return True

    def set_custom_fen(self, fen_string):
        self.board.set_fen(fen_string)

    def generate_attacks_svg(self, color):
        pieces = chess.SquareSet(chess.BB_EMPTY)
        for i in chess.PIECE_TYPES:
            pieces = pieces | self.board.pieces(i, color)

        attacks = np.array(chess.SquareSet(chess.BB_EMPTY).tolist(), dtype="int16")
        for square in pieces:
            attacks += np.array(self.board.attacks(square).tolist(), dtype="int16")

        maxattacks = max(attacks)

        fills = {}
        for idx, val in enumerate(attacks):
            if val > 0:
                intensity = hex(255 - ((255 - 80) + 80 // maxattacks * val))[2:]
                if len(intensity) < 2:
                    intensity = '0' + intensity
                fills[chess.SQUARES[idx]] = "#FF" + intensity + intensity

        return chess.svg.board(self.board, fill=fills)

    def generate_key_squares_svg(self):
        pieces = [chess.SquareSet(chess.BB_EMPTY)] * 2
        fills = {}

        for color in chess.COLORS:
            for piece in chess.PIECE_TYPES:
                pieces[color] = pieces[color] | self.board.pieces(piece, color)

            for square in pieces[color]:
                num_defenders = sum(self.board.attackers(color, square).tolist())
                num_attackers = sum(self.board.attackers(not color, square).tolist())
                if num_defenders < num_attackers:
                    fills[square] = "#FF0000"

        return chess.svg.board(self.board, fill=fills)