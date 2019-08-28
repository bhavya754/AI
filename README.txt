All code is written in Python3

Sudoku: 
We use Least Constraining Value to choose the order in which we test the values that each variable can take. During the forward checking process, I am counting the number of possible values that other empty cells could take if we plug in a particular value at that position. We then order the values at that particular position by the descending number of total possible values of other cells. 

2048:
Models 2048 as an adversarial game. Uses Alpha-Beta pruning, Expectiminimax as Search algorithm

N-puzzle:
Usually called the 8-tile puzzle. Implements BFS, DFS, and A* search. 