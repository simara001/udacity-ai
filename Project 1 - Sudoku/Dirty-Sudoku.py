rows = 'ABCDEFGHI'
cols = '123456789'


def cross(a, b):
    return [s + t for s in a for t in b]

boxes = cross(rows, cols)

print(boxes)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

print(row_units[0])
print(column_units[0])
print(square_units[0])

unitlist = row_units + column_units + square_units

print(unitlist)

