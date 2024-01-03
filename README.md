# Peg Solitaire Engine
## Our Motive
[Peg solitaire](https://en.wikipedia.org/wiki/Peg_solitaire), a game now most known for its presence in Cracker Barrel, has been around for the last few centuries. It has gained multiple variants alongside its followers and has stumped many for as long as it has existed. We seek to provide a set of algorithms that help solve peg solitaire, specifically the triangular variant.
## The Setup
To solve this problem, we first had to frame it in terms of a program. To do this, some more formal terminology is introduced:
### Board
A board is represented as a set of coordinate values within a triangle of size n. A triangle of size n has (n*(n+1))/2 coordinates since that is the [nth triangular number](https://en.wikipedia.org/wiki/Triangular_number). Each coordinate represents a cell, which has a value of 1 or 0. This value identifies whether the cell contains a peg or not.
### Positions
We identify all the positions within a board. A position is a tuple of three collinear cells.
This allows us to efficiently represent jumps, which are positions that follow the patterns (1,1,0) or (0,1,1).
## The Algorithms
### Backtracking
Backtracking is the specific use of depth-first search. This means that it is our brute force solution, which has some major downsides such as exponential runtime.\
Our implementation can be seen in algorithms/backtracking/backtracking.py
### Dynamic Programming
Dynamic programming is just an extension of Backtracking, where we store bad states in a set that we reference later throughout backtracking. This allows us to identify previously seen bad states.\
Our implementation can be seen in algorithms/backtracking/backtracking.py
### Pagoda Functions
Pagoda functions are a method of pruning states from the search tree by tracking the values found by the function throughout the recursion.\
Our implementation of a pagoda function can be found in algorithms/pagoda/pagoda.py

## Paper
We uncovered some interesting heuristics, methods, and algorithmic variations to solve peg solitaire. Our findings can be further explored in our [research paper](solving_peg_solitaire_with_adv_backtracking.pdf)

## Running Solutions
To run solutions, use user_test.py. You will then be asked whether you want to use the console visualizer or the web app visualizer. Both allow you to choose board sizes and run solutions on the chosen boards. Then the solution to get from the initial board to the goal board is shown.

### Using the web app
This portion of the project is still in testing and is a little buggy, but works for basic operations such as setting the board size, choosing the initial and goal states and vizualizing the solution for the given board.
\
Once a board size is chosen, the initial and goal boards can be made, and the solver can be run. Once a solution is found, the solver will automatically display the solution step by step.
