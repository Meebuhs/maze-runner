from mazerunner.solvers.InformedSolver import InformedSolver


class GreedySolver(InformedSolver):
    """ Solver which implements a Greedy Best First search. The fringe nodes are stored in a priority queue, sorted by
    f(c) = h(c) where h(c) is the estimated cost from cell c to the goal. h(c) is calculated by determining the
    manhattan distance from the cell to the goal. As this search does not consider the cost of reaching a cell, and only
    the cost to the goal, the solution cannot guaranteed to be optimal. """

    def __init__(self, runner):
        InformedSolver.__init__(self, runner)

    def calculate_cost(self, cell):
        """ Calculates the estimated distance from a cell to the goal cell using manhattan distance. """
        return self.runner.get_columns() - cell.get_x() + self.runner.get_rows() - cell.get_y()
