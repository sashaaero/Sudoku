from PyQt5.QtWidgets import QWidget,QGridLayout, QPushButton
from field import Field
from cell import Cell

class GUI(QWidget):


    def __init__(self):
        super().__init__()

        f3 = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
        self.field = Field(field=f3)
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
        print("was called")
        self.field.solve()
        self.apply()
