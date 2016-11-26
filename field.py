from pprint import pprint
from cell import Cell
from random import randint, choice, shuffle
from PyQt5.QtWidgets import QWidget

class Field(QWidget):

    def __init__(self, size=9):
        self.fsize = size # I use fsize because size is inherited property of QWidget
        self.dsize = size // 3 # district size
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
        """
        Transposing the field
        """
        self.field = list(map(list, zip(*self.field)))

    def _swap_rows_inside_district(self):
        """
        Swaps rows inside district
        """
        tmp = [0] * self.fsize
        d_num = randint(0, self.dsize - 1) # pick random horizontal district
        rows_l = [i for i in range(self.dsize)]
        del rows_l[choice(rows_l)]
        """
            Some explanation
            We just pick exceptional row from list of 3 rows
            So, others 2 rows will be swapped
        """
        self._put_line_in_line(tmp, self.field[d_num * 3 + rows_l[0]])
        self._put_line_in_line(
            self.field[d_num * 3 + rows_l[0]],
            self.field[d_num * 3 + rows_l[1]])

        self._put_line_in_line(self.field[d_num * 3 + rows_l[1]], tmp)

    def _swap_districts_rows(self):
        """
        Swaps districts as rows (e.g. swap first 3 rows with last 3 rows)
        """
        districts = [i for i in range(self.dsize)]
        del districts[choice(districts)]

        for i in range(self.dsize):
            swap = [0] * self.fsize
            self._put_line_in_line(
                swap,
                self.field[self.dsize * districts[0] + i]
            )
            self._put_line_in_line(
                self.field[self.dsize * districts[0] + i],
                self.field[self.dsize * districts[1] + i]
            )
            self._put_line_in_line(
                self.field[self.dsize * districts[1] + i],
                swap
            )

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

        # self._transpose()
        # self._swap_rows_inside_district()
        # self._swap_districts_rows()
        level = 3 # number of operations to shake field
        operations = [self._transpose for i in range(level)]
        operations.extend([self._swap_districts_rows for i in range(level)])
        operations.extend([self._swap_rows_inside_district for i in range(level)])

        shuffle(operations)

        for operation in operations:
            operation()

    def validate_field(self):
        """
        Checks if generated field is valid
        Can be used as solve checker
        :return: true if field is valid, false otherwise
        """
        # check rows
        for row in self.field:
            if len(set(row)) != self.fsize:
                return False

        # check columns
        for j in range(self.fsize):
            if len(set([self.field[i][j] for i in range(self.fsize)])) != self.fsize:
                return False

        # check districts
        d_size = self.fsize // 3
        for i in range(d_size):
            for j in range(d_size):
                # start point is i * 3, j * 3
                d_list = []
                for x in range(d_size):
                    for y in range(d_size):
                        d_list.append(self.field[i * d_size + x][j * d_size + y])

                if len(set(d_list)) != self.fsize:
                    return False

        return True


def main():
    field = Field()
    field.print()

    print(field.validate_field())

main()