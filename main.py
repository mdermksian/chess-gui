import sys
import chess
import chess.svg
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget
from PyQt5.QtSvg import QSvgWidget
import numpy as np

class Main(QWidget):
    def __init__(self, fen):
        super().__init__()
        self.initUI(fen)

    def initUI(self, fen=None):
        board = chess.Board(fen)

        white_svg = self.generate_svg(board, chess.WHITE)
        black_svg = self.generate_svg(board, chess.BLACK)
        white_svg_bytes = bytearray(white_svg, encoding='utf-8')
        black_svg_bytes = bytearray(black_svg, encoding='utf-8')
        whiteSvg = QSvgWidget()
        whiteSvg.renderer().load(white_svg_bytes)
        blackSvg = QSvgWidget()
        blackSvg.renderer().load(black_svg_bytes)

        hbox = QHBoxLayout()
        hbox.addWidget(whiteSvg)
        hbox.addWidget(blackSvg)
        self.setLayout(hbox)
        self.setGeometry(10, 10, 1600, 800)
        self.show()

    @staticmethod
    def generate_svg(board, color):
        pieces = chess.SquareSet(chess.BB_EMPTY)
        for i in range(1, 7):
            pieces = pieces | board.pieces(i, color)

        attacks = np.array(chess.SquareSet(chess.BB_EMPTY).tolist(), dtype="int16")
        for square in pieces:
            attacks += np.array(board.attacks(square).tolist(), dtype="int16")

        maxattacks = max(attacks)

        colors = {}
        for idx, val in enumerate(attacks):
            if val > 0:
                intensity = hex(255 - ((255 - 80) + 80 // maxattacks * val))[2:]
                if len(intensity) < 2:
                    intensity = '0' + intensity
                colors[chess.SQUARES[idx]] = "#FF" + intensity + intensity

        return chess.svg.board(board, fill=colors)


if __name__ == "__main__":
    print("Type the fen:")
    fen = input()

    if len(fen) == 0:
        fen = chess.STARTING_FEN

    app = QApplication(sys.argv)
    m = Main(fen)
    sys.exit(app.exec_())
