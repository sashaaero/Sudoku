from pprint import pprint
from cell import Cell
from PyQt5.QtWidgets import QWidget

class Field(QWidget):

    def __init__(self, size=9):
        self.fsize = size
        self.field = self._create_field()
        self._generate_field()

    def print(self):
        for row in self.field:
            print('\t'.join(map(str, row)))
            print()

    def _create_field(self):
        """
        Creates a field with size of given size
        :return: field (double dimensioned list)
        """
        field = []
        for x in range(self.fsize):
            field.append(list())
            for y in range(self.fsize):
                field[x].append(Cell())

        return field

    @staticmethod
    def _put_line_in_line(line1, line2):
        """
        Put values from line1 into line1 in place
        :param line1: line that should be edited
        :param line2: values for line1
        :return: None
        """
        assert len(line1) == len(line2)
        for i in range(len(line1)):
            line1[i] = line2[i]

    @staticmethod
    def _shifted_line(line, num):
        """
        Shifts line by given number of indexes
        :param line: line that will be shifted
        :param num: number of indexes that will shift
        :return shifted_line: shifted line
        """
        shifted_line = []
        for i in range(len(line)):
            shifted_line.append(line[(i + num) % len(line)])

        return shifted_line

    def _transpose(self):
        for i in range(self.fsize):
            for j in range(self.fsize):
                self.field[i][j], self.field[j][i] = self.field[j][i], self.field[i][j]

    def _generate_field(self):
        """
        Generates a field for a game
        :return field: game field
        """
        district_size = self.fsize // 3

        def calc_shift(n):
            return (n // district_size) + district_size * (n % district_size)

        for i in range(len(self.field)):
            ins_line = self._shifted_line(list(range(1, 10)), calc_shift(i))
            self._put_line_in_line(self.field[i], ins_line)

        self._transpose()



def main():
    field = Field()
    field.print()

main()