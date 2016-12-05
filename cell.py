from PyQt5.QtWidgets import QWidget


class Cell(QWidget):

    def __init__(self, value=0):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return self.value
