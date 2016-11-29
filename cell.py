from PyQt5.QtWidgets import QWidget


class Cell(QWidget):

    def __init__(self, value=0):
        self.value = value

    def __str__(self):
        return str(self.value) if value else ''
