from random import randint, choice, shuffle
from copy import deepcopy as copy
from cell import Cell
from PyQt5.QtWidgets import QApplication
import sys
from time import time

class Field():
    EASY = 40
    MEDIUM = 35
    HARD = 30

    def __init__(self, field=None, size=9, gui=None, empty=False):
        self.gui = gui
        self.size = size
        self.dsize = size // 3  # district size
        self.field = self.create()
        self.tier = Field.MEDIUM
        if empty:
            self.create()
        elif field:
            self.set(field)
        else:
            self.generate()

        self.solved = False

    def __str__(self):
        return '\n\n'.join(['\t'.join(map(str, row)) for row in self.field])

    def __eq__(self, other):
        for i in range(self.size):
            for j in range(self.size):
                if self.field[i][j] != other.field[i][j]:
                    return False

        return True

    def set(self, field):
        if type(field) == str:
            for i in range(self.size):
                for j in range(self.size):
                    self.field[i][j].set(i, j, int(field[i * self.size + j]))

        elif type(field) == list:
            for i in range(self.size):
                for j in range(self.size):
                    self.field[i][j].set(i, j, field[i][j])

    def create(self):
        """
        Creates a field with size of given size
        :return: field (double dimensioned list)
        """
        field = []
        for x in range(self.size):
            field.append(list())
            for y in range(self.size):
                field[x].append(Cell(self.gui, self, x, y, 0))

        return field

    @staticmethod
    def set_values(line1, line2):
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
        tmp = [0] * self.size
        d_num = randint(0, self.dsize - 1)  # pick random horizontal district
        rows_l = [i for i in range(self.dsize)]
        del rows_l[choice(rows_l)]
        """
            We just pick exceptional row from list of 3 rows
            So, others 2 rows will be swapped
        """
        self.set_values(tmp, self.field[d_num * 3 + rows_l[0]])
        self.set_values(
            self.field[d_num * 3 + rows_l[0]],
            self.field[d_num * 3 + rows_l[1]])

        self.set_values(self.field[d_num * 3 + rows_l[1]], tmp)

    def swap_districts_rows(self):
        """
        Swaps districts as rows (e.g. swap first 3 rows with last 3 rows)
        """
        districts = [i for i in range(self.dsize)]
        del districts[choice(districts)]

        for i in range(self.dsize):
            swap = [0] * self.size
            self.set_values(
                swap,
                self.field[self.dsize * districts[0] + i]
            )
            self.set_values(
                self.field[self.dsize * districts[0] + i],
                self.field[self.dsize * districts[1] + i]
            )
            self.set_values(
                self.field[self.dsize * districts[1] + i],
                swap
            )

    def generate(self):
        """
        Generates a field for a game
        1. Creates basic field
        2. Create list of:
            a. transpose
            b. districts swaps
            c. rows/columns swaps (column swap = transpose -> row swap)
        3. Shake functions
        4. Apply them one by one
        :return field: game field
        """
        district_size = self.size // 3

        def calc_shift(n):
            return (n // district_size) + district_size * (n % district_size)

        for i in range(len(self.field)):
            ins_line = self.shifted_line([i for i in range(1, 10)], calc_shift(i))
            self.set_values(self.field[i], ins_line)

        level = 100  # number of operations to shake field
        operations = [self.transpose for _ in range(level)]
        operations.extend([self.swap_districts_rows for _ in range(level)])
        operations.extend([self.swap_rows_inside_district for _ in range(level)])

        shuffle(operations)

        for operation in operations:
            operation()

        for i in range(self.size):
            for j in range(self.size):
                val = self.field[i][j]
                self.field[i][j] = Cell(self.gui, self, i, j, val)

        while not self.validate():
            self.generate()

        # TODO DELETIONS
        self.deletions()

    def validate_row(self, i):
        """
        :param i: row number
        :return: does this row contain only unique numbers?
        """
        values = []
        for j in range(self.size):
            if self.field[i][j].value in values:
                return False
            if self.field[i][j].value != 0:
                values.append(self.field[i][j].value)
        return True

    def validate_col(self, j):
        """
        :param j: columns number
        :return: @see validate_row
        """
        values = []
        for i in range(self.size):
            if self.field[i][j].value in values:
                return False
            if self.field[i][j].value != 0:
                values.append(self.field[i][j].value)
        return True

    def validate_district(self, i, j):
        """
        :param i: row number
        :param j: column nuber
        :return: @see validate row
        """
        values = []
        di, dj = (i // self.dsize) * self.dsize, (j // self.dsize) * self.dsize
        for x in range(di, di+self.dsize):
            for y in range(dj, dj+self.dsize):
                if self.field[x][y].value in values:
                    return False
                if self.field[x][y].value != 0:
                    values.append(self.field[x][y].value)
        return True


    def validate(self):
        """
        :return: true if field is valid, false otherwise
        """
        # check rows
        for i in range(self.size):
            if not self.validate_row(i):
                return False

        # check columns
        for j in range(self.size):
            if not self.validate_col(j):
                return False

        # check districts
        """d_size = self.size // 3
        for i in range(d_size):
            for j in range(d_size):
                # start point is i * 3, j * 3
                d_list = []
                for x in range(d_size):
                    for y in range(d_size):
                        d_list.append(self.field[i * d_size + x][j * d_size + y])

                if len(set(d_list)) != self.size:
                    return False"""

        for i in range(self.dsize):
            for j in range(self.dsize):
                self.validate_district(i * self.dsize, j * self.dsize)

        return True

    @staticmethod
    def occupied_nums(field, i, j):
        """
        This method is static cause used in solver for a field of numbers, not cells
        :param field: given field
        :param i: row number
        :param j: column number
        :return: set of numbers that are appearing in row, column and district
        """
        nums = set()
        size = len(field)

        for x in range(size):
            nums.add(field[i][x])

        for x in range(size):
            nums.add(field[x][j])

        for x in range(size):
            for y in range(size):
                a = x * size + y
                b = i * size + j
                if a // 27 == b // 27 and a % 9 // 3 == b % 9 // 3:
                    nums.add(field[x][y])

        return nums

    @staticmethod
    def empty_cell(field):
        """
        :param field: given field
        :return: empty cell index or -1, -1 if not present
        """
        for i in range(len(field)):
            for j in range(len(field)):
                if field[i][j] == 0:
                    return i, j

        return -1, -1

    def solve(self, make_set=True):
        """
        Method uses recursive solve algorithm:
            1. Find empty cell
            2. Find numbers which can be applied there
            3. In loop put them there and recursively solve new field with new number there
            4. If there is no empty cells - that means we have found a solution
            5. Accumulate number of solutions
        :return: true if only 1 solution was found and this solution is valid
        """
        field_copy = [[cell.value for cell in row] for row in self.field]
        solutions = 0

        def inner_solver(field):
            i, j = Field.empty_cell(field)
            nums = Field.occupied_nums(field, i, j)

            if i == -1:
                if make_set:
                    self.set(field)
                nonlocal solutions
                solutions += 1
                return

            for x in set(range(1, 10)) - nums:
                field[i][j] = x
                inner_solver(copy(field))

        inner_solver(field_copy)

        return solutions == 1 and (self.validate() or not make_set)

    def deletions(self):
        """
        Deletes elements from generated puzzle
        1. Pick non-empty cell
        2. If didnt pick it - remove value from there
        3. Check if only 1 solution exists
        4. Repeat
        """
        # non_empty = [(i, j) for j in range(self.size) for i in range(self.size) if self.field[i][j].value != 0]
        non_empty = [(i, j) for j in range(self.size) for i in range(self.size) if self.field[i][j]]
        while len(non_empty) >= self.tier:
            # delete elements
            already_seen = set()
            i, j = choice(list(set(non_empty) - already_seen))
            old_value = self.field[i][j].value
            self.field[i][j].value = 0
            while not self.solve(make_set=False):
                already_seen.add((i, j))
                self.field[i][j].value = old_value

                i, j = choice(list(set(non_empty) - already_seen))
                old_value = self.field[i][j].value
                self.field[i][j].value = 0

            non_empty.remove((i, j))
            # print(self)
            print(len(non_empty))

    def at(self, i, j):
        """
        :param i: row number
        :param j: column number
        :return: value of i, j cell (cause there is no way to overload [][] operator)
        """
        return self.field[i][j]

    def extract(self):
        return ''.join(''.join(str(cell.value) for cell in row) for row in self.field)


def fmain():
    app = QApplication(sys.argv)
    #f3 = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
    #f3 = "100000000000000000000000000000000000000000000000000000000000000000000000000000000"
    field = Field()
    print(field)
    start = time()
    print(field.solve())
    print(time() - start)
    print(field)
    sys.exit(app.exec_())


# fmain()
