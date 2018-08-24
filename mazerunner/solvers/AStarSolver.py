from math import sqrt

from mazerunner.solvers.InformedSolver import InformedSolver


class AStarSolver(InformedSolver):
    """ Solver which implements an A* search. The fringe nodes are stored in a priority queue, sorted by f(c) = g(c) +
    h(c) where g(c) is the cost from the root to the cell c and h(c) is the estimated cost from cell c to the goal.
    Each cell c simply increments g(parent(c)), while h(c) is calculated by determining the manhattan distance from
    the cell to the goal. As travel through a maze cannot be any shorter than the manhattan distance, the heuristic is
    both admissible and consistent, and thus the search is optimal. """

    def __init__(self, runner):
        InformedSolver.__init__(self, runner)

    def calculate_cost(self, cell):
        """ Calculates the estimated distance from the start cell to the goal cell, via the given cell using manhattan
        distance for the heuristic h(c). """
        return cell.get_cost() + abs(self.runner.goal_cell.get_x() - cell.get_x()) + \
               abs(self.runner.goal_cell.get_y() - cell.get_y())

    def calculate_cost_euclidean(self, cell):
        """ Calculates the estimated distance from the start cell to the goal cell, via the given cell using euclidean
        distance for the heuristic h(c). """
        return cell.get_cost() + sqrt(
            (self.runner.goal_cell.get_x() - cell.get_x()) ** 2 + (self.runner.goal_cell.get_y() - cell.get_y()) ** 2)
