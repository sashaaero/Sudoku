import sys
from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication

class Main(QWidget):

    def __init__(self):
        super().__init__()
        self.initGUI()

    def initGUI(self):
        grid = QGridLayout()
        self.setLayout(grid)


