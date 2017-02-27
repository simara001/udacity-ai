# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The same way I used elimination and only option techniques. The algorithm tries to reduce the puzzle (or solve it) in iterations.
As you can see:

```python
def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Getting solved values before applying eliminate/only choice/naked twins techniques
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Applying techniques
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
```

I have combined the 3 different techniques in each iteration so I can propagate the constrains of each one of them, until
the algorithm finds what we are looking for (single values for all the boxes).

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The most important part is understanding how `unit_list` influences all the techniques. Let's remember that `unit_list`
is the variable that contains the constraints for our algorithm. Initially, it was only the combination of:

```python
unit_list =  column_units + row_units + square_units
```

I calculated the new 2 constraints and include them on unit_list:

```python
# Getting diagonal values (we can hardcode it also i.e. ['A1','B2','C3'...]
diagonal_left = [[rows[i]+cols[i] for i in range(len(rows))]]
diagonal_right = [[rows[i]+cols[len(rows)-1-i] for i in range(len(rows))]]
unit_list =  column_units + row_units + square_units + diagonal_left + diagonal_right
```

After that, `peers` will add another 2 arrays (diagonals), and the technicques that use peers for back propagating 
constraints will take the new constraints (diagonals) in consideration

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.