"""Functions for printing pretty ASCII tables.

Dependencies:
    * texttable
"""
from .terminals import get_terminal_size

from texttable import Texttable


def pprint_table(data, header_row=False):
    """Prints 2-dimensional iterable as a pretty looking table.

    :param data: 2-dimensional array containing the data
    :param header_row: If True, uses the first row as column labels.
    """

    cols, lines = get_terminal_size()

    table = Texttable(max_width=cols)
    table.add_rows(data, header=header_row)

    print table.draw()

