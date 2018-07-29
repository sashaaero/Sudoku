from PyQt5.QtWidgets import QWidget, QGridLayout, QFormLayout
from PyQt5.QtCore import Qt
from field import Field


class Before(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layout = QFormLayout()


class GUI(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.active_cell = None
        self.field = Field(gui=self)

        grid = QGridLayout()
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)
        self.setLayout(grid)

        for i in range(self.field.size):
            for j in range(self.field.size):
                grid.addWidget(self.field.at(i, j), i, j)

        self.resize(450, 450)
        self.show()

    def operate(self):
        self.field.solve()
        self.apply()

    def keyPressEvent(self, event):
        if self.active_cell and self.active_cell.changeable:
            if Qt.Key_1 <= event.key() <= Qt.Key_9:
                self.active_cell.set(value=event.key() - Qt.Key_1 + 1)
            elif event.key() == Qt.Key_Backspace:
                self.active_cell.set(value=0)
            self.active_cell.repaint()

    def reactivate(self, cell):
        if self.active_cell:
            self.active_cell.deactivate()
            print(self.active_cell.value, " deactivated")

        self.active_cell = cell
        self.active_cell.activate()
        print(self.active_cell.value, " is now acitve")
