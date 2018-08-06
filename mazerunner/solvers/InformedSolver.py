from queue import PriorityQueue

import mazerunner.Config as Config
from mazerunner.Cell import Cell, get_runner_index


class InformedSolver:
    """ Base class for an informed search. The fringe nodes are stored in a priority queue, sorted by an
    estimation of their cost. The function which defines how the cost is calculated is different for each solver. """

    def __init__(self, runner):
        self.runner = runner
        self.path = []
        self.queue = PriorityQueue(maxsize=0)
        # Current and goal cells, the cells assigned here are discarded once search is commenced
        self.current_cell = Cell(0, 0, 'runner')
        self.goal_cell = Cell(0, 0, 'runner')

    def run(self):
        """ Performs the informed search. The cost function f(c) is defined by inheriting solvers. """
        self.queue.put((self.calculate_cost(self.runner.cells[0]), self.runner.cells[0]))
        self.runner.cells[0].set_cost(0)
        self.goal_cell = self.runner.cells[
            get_runner_index(Config.RUNNER_MAZE_COLUMNS - 1, Config.RUNNER_MAZE_ROWS - 1)]
        while True:
            if not Config.get_runner_running():
                break
            self.current_cell = self.queue.get()[1]
            self.current_cell.set_visited()
            self.current_cell.set_queue(False)
            if self.current_cell == self.goal_cell:
                self.construct_path()
                break
            else:
                for cell in self.runner.get_neighbours(self.current_cell):
                    if cell.get_parent() is None:
                        self.queue.put((self.calculate_cost(cell), cell))
                        cell.set_parent(self.current_cell)
                        # Cost to cell is ignored by greedy search
                        cell.set_cost(self.current_cell.get_cost() + 1)
                        cell.set_queue()
            self.runner.display.update_scene()

    def construct_path(self):
        """ Constructs the solution path to the current cell by traversing the search tree which was constructed. """
        self.path.append(self.current_cell)
        cell = self.current_cell
        while not cell == self.runner.cells[0]:
            cell.set_solution()
            self.path.append(cell.get_parent())
            cell = cell.get_parent()
        self.runner.cells[0].set_solution()
        self.path.reverse()
        print(self.path)
        self.runner.solved = True
        self.runner.display.update_scene(self.path)

    def get_path(self):
        """ Returns the solution path. If the solver has not yet been run, the path returned is an empty array. """
        return self.path

    def calculate_cost(self, cell):
        """ Returns the cost of the cell, must be overridden by inheriting solvers. """
        pass
