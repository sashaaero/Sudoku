from pprint import pprint


def create_field(i, j, fill_with=None):
    """
    Creates a field with size of given i, j arguments [i, j]
    :param i: number of rows
    :param j: number of columns
    :param fill_with: object that will be placed in cells
    :return: field (double dimensioned list)
    """
    field = []
    for x in range(i):
        field.append(list())
        for y in range(j):
            field[x].append(fill_with)

    return field


def put_line_in_line(line1, line2):
    """
    Put values from line1 into line1 in place
    :param line1: line that should be edited
    :param line2: values for line1
    :return: None
    """

def shifted_line(line, num):
    """
    Shifts line by given number of indexes
    :param line: line that will be shifted
    :param num: number of indexes that will shift
    :return shifted_line: shifted line
    """
    shifted_line_ = []
    for i in range(len(line)):
        shifted_line_.append(line[(i + num) % len(line)])




def generate_field(size=9, district_size=3):
    """
    Generates a field for a game
    :param size: size of a field [size x size]
    :param district_size: @See documentation for meaning of district
    :return field: game field
    """
    raise_line = list(range(1, 10))
    field = create_field(size, size)
    for district in range(size / district_size):
        for line in range(district_size):
            put_line_in_line(field[line * district],





def main():
    field = create_field(9, 9, 1)
    pprint(field)



main()