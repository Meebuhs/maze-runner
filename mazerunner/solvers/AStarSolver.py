from math import sqrt

import mazerunner.Config as Config
from mazerunner.solvers.InformedSolver import InformedSolver


class AStarSolver(InformedSolver):
    """ Solver which implements an A* search. The fringe nodes are stored in a priority queue, sorted by f(c) = g(c) +
    h(c) where g(c) is the cost from the root to the cell c and h(c) is the estimated cost from cell c to the goal.
    Each cell c simply increments g(parent(c)), while h(c) is calculated by determining the manhattan distance from
    the cell to the goal. As travel through a maze cannot be any shorter than the manhattan distance, the heuristic is
    both admissible and consistent, and thus the search is optimal. """

    def __init__(self, runner):
        InformedSolver.__init__(self, runner)

    def calculate_cost_euclidean(self, cell):
        """ Calculates the estimated distance from the start cell to the goal cell, via the given cell using euclidean
        distance for the heuristic h(c). """
        return cell.get_cost() + sqrt(
            (Config.MAZE_COLUMNS - cell.get_x()) ** 2 + (Config.MAZE_ROWS - cell.get_y()) ** 2)

    def calculate_cost(self, cell):
        """ Calculates the estimated distance from the start cell to the goal cell, via the given cell using manhattan
        distance for the heuristic h(c). """
        return cell.get_cost() + Config.MAZE_COLUMNS - cell.get_x() + Config.MAZE_ROWS - cell.get_y()
