assignments = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [(s + t) for s in A for t in B]

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# Getting diagonal values (we can hardcode it also i.e. ['A1','B2','C3'...]
diagonal_left = [[r+c for r,c in zip(rows,cols)]]
diagonal_right = [[r+c for r,c in zip(rows,cols[::-1])]]

# No considering diagonals
unit_list =  column_units + row_units + square_units

# Considering diagonals
unit_list =  column_units + row_units + square_units + diagonal_left + diagonal_right

units = dict((s, [u for u in unit_list if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)