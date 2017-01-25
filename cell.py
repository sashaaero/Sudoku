from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QFont, QColor, QPen
from PyQt5.QtCore import Qt, QEvent


class Cell(QWidget):
    START_POSITION = 50

    def __init__(self, parent, field, i, j, value):
        super().__init__()
        self.parent = parent
        self.field = field
        self.i = i
        self.j = j
        self.value = value
        self.active = False
        self.valid = True
        self.changeable = False

    def __hash__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return str(self.value) if self.value > 0 else ''

    def empty(self):
        return self.value == 0

    def set(self, i=None, j=None, value=None):
        if i is not None:
            self.i = i
        if j is not None:
            self.j = j
        if value is not None:
            self.value = value

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw(qp, e)
        qp.end()

    def draw(self, painter, event):
        font = QFont('Ubuntu Mono', 24, QFont.Light if self.changeable else QFont.Bold)
        painter.setFont(font)

        # validate
        self.valid = \
            self.field.validate_col(self.j) and \
            self.field.validate_row(self.i) and \
            self.field.validate_district(self.i, self.j)

        if not self.changeable:
            painter.fillRect(0, 0, self.size().width(), self.size().height(), Qt.gray)

        if not self.valid:
            painter.fillRect(0, 0, self.size().width(), self.size().height(), Qt.red)

        # drawing main border
        painter.setPen(QPen(Qt.blue if self.active else Qt.black, 2, Qt.SolidLine))
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

        # change color if active
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.drawText(event.rect(), Qt.AlignCenter, str(self))

    def activate(self):
        self.active = True
        self.repaint()

    def deactivate(self):
        self.active = False
        self.repaint()

    def mouseReleaseEvent(self, e):
        self.parent.reactivate(self)

