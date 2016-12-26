import sys
from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication
from gui import GUI


def main():
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())

#main()



