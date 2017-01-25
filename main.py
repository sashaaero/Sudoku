import sys
from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication
from gui import MainWindow
import storage


def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

main()


