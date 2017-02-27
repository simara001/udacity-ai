import collections
import logging
from utilities import *

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'A1': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    logging.info('Implementing Naked Twins technique')
    for unit in unit_list:
        # Finding all the boxes with two digints on a given unit
        values_in_unit = {key: values[key] for key in unit if len(values[key]) == 2}
        # Getting number of occurrences per value
        value_occurrences = collections.Counter(values_in_unit.values())
        # Values that repeat themselves in a given unit, and length == 2, is our definition of naked twins
        twins_in_current_unit = [key for key in values_in_unit if value_occurrences[values_in_unit[key]] == 2]

        # Eliminate the naked twins as possibilities for their peers
        # I am removing naked twins from same rows, columns and squares. I need to iterate over the units
        for key in unit:
            # I don't want to replace naked twins -> (key not in twins_in_current_unit)
            # I don't want to override the boxes that are already solved -> (len(values[key])>1)
            if key not in twins_in_current_unit and len(values[key]) > 1 and len(twins_in_current_unit) > 0:
                # repeated_digits = set(values[digits] for digits in twins_in_current_unit)
                # print(repeated_digits)
                digits = values[twins_in_current_unit[0]]
                for value in digits:
                    # values[key] = values[key].replace(value, '')
                    values = assign_value(values, key, values[key].replace(value, ''))
    assert len(values) == 81
    return values



def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'
    # values = [all_digits if x == '.' else x for x in values]
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form i.e. {'A1': '123456789', ...}
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    """
    This function uses elimination technique to simplify the sudoku given as a parameter
    :param values: The sudoku in dictionary form i.e. {'A1': '123456789', ...}
    :return: values: in dictionary form after applying elimination technique
    """

    logging.info('Implementing Elimination technique')
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            # values[peer] = values[peer].replace(digit, '')
            values = assign_value(values, peer, values[peer].replace(digit, ''))
    assert len(values) == 81
    return values


def only_choice(values):
    """
        This function uses only-choice technique to simplify the sudoku given as a parameter
        :param values: The sudoku in dictionary form i.e. {'A1': '123456789', ...}
        :return: values: in dictionary form after applying elimination technique
    """
    logging.info('Implementing Only-Choice technique')
    for unit in unit_list:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                # values[dplaces[0]] = digit
                values = assign_value(values, dplaces[0], digit)
    assert len(values) == 81
    return values

def reduce_puzzle(values):
    """
        This function uses elimination/only-choice/naked-twins technique to simplify the sudoku given as a parameter
        :param values: The sudoku in dictionary form i.e. {'A1': '123456789', ...}
        :return: values: in dictionary form after applying elimination technique
                 False: if given sudoku is not deterministic and cannot be solved
    """

    stalled = False
    logging.info('Reducing puzzle by implementing Elimination/Only-Choice/Naked-Twins technique')
    while not stalled:
        # Getting solved values before applying eliminate/only choice/naked twins techniques
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Applying techniques
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        # Getting solved values after applying eliminate/only choice/naked twins techniques
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # Verifying we are making some progress
        stalled = solved_values_before == solved_values_after
        # If we have a non deterministic sudoku should return false
        if len([box for box in values.keys() if len(values[box]) == 0]):
            logging.warning('This is a non-deterministic sudoku')
            return False
    assert len(values) == 81
    return values

def search(values):
    """
        Search uses deep level first, to try different possibilities and combinations until the solution is found
        :param values: The sudoku in dictionary form i.e. {'A1': '123456789', ...}
        :return: values: in dictionary form after applying elimination technique
    """
    values = reduce_puzzle(values)
    if values is False:
        return False
    # Sudoku is solved when all boxes have one (different) digit
    if all(len(values[s]) == 1 for s in boxes):
        return values
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    assert len(values) == 81
    return values


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    values = grid_values(diag_sudoku_grid)
    display(values)
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        logging.warning('System was not able to start Pygame')
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')