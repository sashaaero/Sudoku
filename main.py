import sys
from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication
from gui import GUI
import storage


def main():
    app = QApplication(sys.argv)
    ex = GUI()
    print(ex.field.extract())
    storage.get_fields()
    sys.exit(app.exec_())

main()


