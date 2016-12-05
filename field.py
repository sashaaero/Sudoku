from pprint import pprint
from cell import Cell
from random import randint, choice, shuffle
from PyQt5.QtWidgets import QWidget, QGridLayout

class Field(QWidget):

    def __init__(self, field=None, solve=None, size=9):
        #super().__init__()
        self.fsize = size  # I use fsize because size is inherited property of QWidget
        self.dsize = size // 3  # district size
        self.field = self.create_field()
        if field:
            self.set_from_line(field)
        elif solve:
            try:
                self.solve(solve)
                assert self.validate_field()
            except AssertionError:
                print("This sudoku have no solutions")
        else:
            self.generate_field()
            if not self.validate_field():
                raise NotValidFieldException

        self.initUI()


    def initUI(self):
        pass
        #grid = QGridLayout()
        #self.setLayout(grid)


    def set_from_line(self, line):
        for i in range(self.fsize):
            for j in range(self.fsize):
                self.field[i][j] = Cell(int(line[i * self.fsize + j]))

    def __str__(self):
        return '\n\n'.join(['\t'.join(map(str, row)) for row in self.field])

    def create_field(self):
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
    def put_line_in_line(line1, line2):
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
    def shifted_line(line, num):
        """
        Shifts line by given number of indexes
        :param line: line that will be shifted
        :param num: number of indexes that will shift
        :return shifted_line: shifted line
        """
        _shifted_line = []
        for i in range(len(line)):
            _shifted_line.append(line[(i + num) % len(line)])

        return _shifted_line

    def transpose(self):
        """
        Transposing the field
        """
        self.field = list(map(list, zip(*self.field)))

    def swap_rows_inside_district(self):
        """
        Swaps rows inside district
        """
        tmp = [0] * self.fsize
        d_num = randint(0, self.dsize - 1)  # pick random horizontal district
        rows_l = [i for i in range(self.dsize)]
        del rows_l[choice(rows_l)]
        """
            Some explanation
            We just pick exceptional row from list of 3 rows
            So, others 2 rows will be swapped
        """
        self.put_line_in_line(tmp, self.field[d_num * 3 + rows_l[0]])
        self.put_line_in_line(
            self.field[d_num * 3 + rows_l[0]],
            self.field[d_num * 3 + rows_l[1]])

        self.put_line_in_line(self.field[d_num * 3 + rows_l[1]], tmp)

    def swap_districts_rows(self):
        """
        Swaps districts as rows (e.g. swap first 3 rows with last 3 rows)
        """
        districts = [i for i in range(self.dsize)]
        del districts[choice(districts)]

        for i in range(self.dsize):
            swap = [0] * self.fsize
            self.put_line_in_line(
                swap,
                self.field[self.dsize * districts[0] + i]
            )
            self.put_line_in_line(
                self.field[self.dsize * districts[0] + i],
                self.field[self.dsize * districts[1] + i]
            )
            self.put_line_in_line(
                self.field[self.dsize * districts[1] + i],
                swap
            )

    def generate_field(self):
        """
        Generates a field for a game
        :return field: game field
        """
        district_size = self.fsize // 3

        def calc_shift(n):
            return (n // district_size) + district_size * (n % district_size)

        for i in range(len(self.field)):
            ins_line = self.shifted_line([Cell(i) for i in range(1, 10)], calc_shift(i))
            self.put_line_in_line(self.field[i], ins_line)

        level = 100  # number of operations to shake field
        operations = [self.transpose for i in range(level)]
        operations.extend([self.swap_districts_rows for i in range(level)])
        operations.extend([self.swap_rows_inside_district for i in range(level)])

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

    def extract_to_line(self):
        """
        extracts current field to a line
        :return: string representation of field
        """
        return ''.join([''.join(map(str, row)) for row in self.field])

    @staticmethod
    def same_row(i, j):
        return i // 9 == j // 9

    @staticmethod
    def same_col(i, j):
        return (i - j) % 9 == 0

    @staticmethod
    def same_district(i, j):
        return i // 27 == j // 27 and i % 9 // 3 == j % 9 // 3

    def solve(self, line):

        i = line.find('0')
        if i == -1:
            self.set_from_line(line)

        ex_nums = set()
        for j in range(len(line)):
            if self.same_row(i, j) or self.same_col(i, j) or self.same_district(i, j):
                ex_nums.add(line[j])

        print(ex_nums)

        for num in map(str, range(1, 10)):
            if num not in ex_nums:
                self.solve(line[:i] + num + line[i + 1:])

    def empty(self):
        for i in range(self.fsize):
            for j in range(self.fsize):
                if self.field[i][j].value == 0:
                    yield i, j

    def curr_row_and_col(self, i, j):
        """
        Method finds non-empty cells and returns their values
        :param i: row number
        :param j: column number
        :return: set of values
        """
        ret = set()
        for x in range(self.fsize):
            ret.add(self.field[i][x].value)
            ret.add(self.field[x][j].value)

        return ret

    def curr_district(self, i, j):
        # i // 27 == j // 27 and i % 9 // 3 == j % 9 // 3
        ret = set()
        for x in range(self.fsize):
            for y in range(self.fsize):
                a = x * self.fsize + y
                b = i * self.fsize + j
                if a // 27 == b // 27 and a % 9 // 3 == b % 9 // 3:
                    ret.add(self.field[x][y].value)

        return ret

    def mysolve(self):
        for i, j in self.empty():
            ex_nums = self.curr_row_and_col(i, j) & self.curr_district(i, j)

            print(ex_nums)

            for x in range(1, 10):
                if x not in ex_nums:
                    self.field[i][j] = x

    def __eq__(self, other):
        for i in range(self.fsize):
            for j in range(self.fsize):
                if self.field[i][j] != other.field[i][j]:
                    return False

        return True


def main():
    f3 = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
    field2 = Field(field=f3)
    print(field2)
    field2.solve(f3)


main()