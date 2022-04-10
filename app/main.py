import sys
import chess
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QGridLayout, QWidget, QLineEdit, QComboBox, \
    QPushButton, QLabel, QMessageBox
from PyQt5.QtSvg import QSvgWidget

from chess_driver import ChessDriver


class Main(QWidget):
    def __init__(self, chess_driver):
        super().__init__()
        self.chess_driver = chess_driver
        self.wid = 1600
        self.hei = 650
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Chess GUI")

        self.move_options = QComboBox()
        self.update_move_options()
        self.move_options.activated.connect(self.make_dropdown_move)
        self.move_textbox = QLineEdit(self)
        self.move_textbox.returnPressed.connect(self.make_textbox_move)
        self.fen_textbox = QLineEdit(self)
        self.fen_textbox.returnPressed.connect(self.set_fen)
        self.undo_button = QPushButton("Undo Move", self)
        self.undo_button.clicked.connect(self.undo_move)

        self.white_svg = QSvgWidget()
        self.black_svg = QSvgWidget()
        self.key_squares_svg = QSvgWidget()
        self.draw_svgs()

        outerlayout = QVBoxLayout()
        interactable = QGridLayout()
        interactable.addWidget(QLabel("Legal Moves (Select to make move): "), 0, 0)
        interactable.addWidget(self.move_options, 1, 0)
        interactable.addWidget(QLabel("Type your move here (algebraic notation): "), 0, 2)
        interactable.addWidget(self.move_textbox, 1, 2)
        interactable.addWidget(self.undo_button, 0, 4)

        boards = QHBoxLayout()
        boards.addWidget(self.white_svg)
        boards.addWidget(self.black_svg)
        boards.addWidget(self.key_squares_svg)

        lowerlayout = QHBoxLayout()
        lowerlayout.addWidget(QLabel("Customize FEN: "))
        lowerlayout.addWidget(self.fen_textbox)

        outerlayout.addLayout(interactable)
        outerlayout.addLayout(boards)
        outerlayout.addLayout(lowerlayout)
        self.setLayout(outerlayout)
        self.setGeometry(0, 0, self.wid, self.hei)
        self.show()

    def draw_svgs(self):
        white_svg = self.chess_driver.generate_attacks_svg(chess.WHITE)
        black_svg = self.chess_driver.generate_attacks_svg(chess.BLACK)
        key_squares_svg = self.chess_driver.generate_key_squares_svg()
        white_svg_bytes = bytearray(white_svg, encoding='utf-8')
        black_svg_bytes = bytearray(black_svg, encoding='utf-8')
        key_squares_svg_byes = bytearray(key_squares_svg, encoding='utf-8')
        self.white_svg.renderer().load(white_svg_bytes)
        self.black_svg.renderer().load(black_svg_bytes)
        self.key_squares_svg.renderer().load(key_squares_svg_byes)

    def update_move_options(self):
        self.move_options.clear()
        legal_moves = self.chess_driver.get_legal_moves_list()
        self.move_options.addItems(legal_moves)

    def make_dropdown_move(self):
        move_string = self.move_options.currentText()
        self.make_move(move_string)

    def make_textbox_move(self):
        move_string = self.move_textbox.text()
        self.move_textbox.clear()
        self.make_move(move_string)

    def make_move(self, move_string):
        if self.chess_driver.validate_move(move_string):
            self.chess_driver.make_move(move_string)
            self.draw_svgs()
            self.update_move_options()

    def set_fen(self):
        fen_string = self.fen_textbox.text()
        try:
            self.chess_driver.set_custom_fen(fen_string)
        except ValueError as err:
            QMessageBox.question(self, "Couldn't set FEN", str(err), QMessageBox.Ok, QMessageBox.Ok)
            return

        self.fen_textbox.clear()
        self.draw_svgs()
        self.update_move_options()


    @pyqtSlot()
    def undo_move(self):
        try:
            self.chess_driver.undo_move()
        except:
            QMessageBox.question(self, "End of history", "No moves to undo", QMessageBox.Ok, QMessageBox.Ok)
            return
        self.draw_svgs()
        self.update_move_options()


if __name__ == "__main__":
    driver = ChessDriver(chess.Board())

    app = QApplication(sys.argv)
    m = Main(driver)
    sys.exit(app.exec_())
