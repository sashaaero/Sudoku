from PyQt5.QtWidgets import QWidget,QGridLayout, QPushButton
from field import Field

class GUI(QWidget):


    def __init__(self):
        super().__init__()

        f3 = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
        self.field = Field(field=f3)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.apply()

        self.show()

    def apply(self):
        for i in range(self.field.size):
            for j in range(self.field.size):
                button = QPushButton(self.field.at(i, j))
                button.clicked.connect(self.operate)

                self.grid.addWidget(button, i, j)


    def operate(self):
        print("was called")
        self.field.solve()
        self.apply()
