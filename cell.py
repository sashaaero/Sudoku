from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QFont, QColor, QPen
from PyQt5.QtCore import Qt

class Cell(QWidget):

    def __init__(self, field, i, j, value):
        super().__init__()
        self.i = i
        self.j = j
        self.value = value
        self.field = field
        # self.resize(50, 50)
        self.active = False
        self.valid = True

    def __hash__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return str(self.value) if self.value > 0 else ''

    def empty(self):
        return self.value == 0

    def set(self, i=None, j=None, value=None):
        if i:
            self.i = i
        if j:
            self.j = j
        if value:
            self.value = value

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw(qp, e)
        qp.end()

    def draw(self, painter, event):

        font = QFont('Ubuntu Mono', 24, QFont.Light)
        painter.setFont(font)

        # drawing main border
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.drawRect(0, 0, self.size().width(), self.size().height())

        # drawing exclusive borders

        if self.j == 2 or self.j == 5:
            painter.setPen(QPen(Qt.black, 4, Qt.SolidLine))
            painter.drawLine(self.size().width(), 0, self.size().width(), self.size().height())

        if self.j == 3 or self.j == 6:
            painter.setPen(QPen(Qt.black, 4, Qt.SolidLine))
            painter.drawLine(0, 0, 0, self.size().height())

        if self.i == 2 or self.i == 5:
            painter.setPen(QPen(Qt.black, 4, Qt.SolidLine))
            painter.drawLine(0, self.size().height(), self.size().width(), self.size().height())

        if self.i == 3 or self.i == 6:
            painter.setPen(QPen(Qt.black, 4, Qt.SolidLine))
            painter.drawLine(0, 0, self.size().width(), 0)

        if self.active:
            painter.setPen(QPen(Qt.blue, 2, Qt.SolidLine))

        painter.drawText(event.rect(), Qt.AlignCenter, str(self))


    def mouseReleaseEvent(self, e):
        # self.emit(SIGNAL('clicked()'))
        # self.active = True
        self.field.solve()
        self.repaint()


