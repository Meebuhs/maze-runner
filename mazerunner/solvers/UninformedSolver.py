import mazerunner.Config as Config
from mazerunner.Cell import Cell, get_runner_index


class UninformedSolver:
    """ Base class for solvers which perform a search without calculating any heuristic costs. """

    def __init__(self, runner):
        self.runner = runner
        self.path = []
        self.queue = []
        # Current and goal cells, the cells assigned here are discarded once search is commenced
        self.current_cell = Cell(0, 0, 'runner')
        self.goal_cell = Cell(0, 0, 'runner')

    def run(self):
        """ Performs an uninformed search. The queue behaviour is defined by solvers which inherit from this one. """
        self.queue.append(self.runner.cells[0])
        self.goal_cell = self.runner.cells[
            get_runner_index(Config.RUNNER_MAZE_COLUMNS - 1, Config.RUNNER_MAZE_ROWS - 1)]
        while True:
            if not Config.get_runner_running():
                break
            self.current_cell = self.get_next_cell()
            self.current_cell.set_visited()
            self.current_cell.set_queue(False)
            if self.current_cell == self.goal_cell:
                self.construct_path()
                break
            else:
                for cell in self.runner.get_neighbours(self.current_cell):
                    if cell.get_parent() is None:
                        self.queue.append(cell)
                        cell.set_parent(self.current_cell)
                        cell.set_queue()
            self.runner.display.update_scene()

    def construct_path(self):
        """ Constructs the solution path to the current cellby traversing the search tree which was constructed. """
        cell = self.current_cell
        self.path.append(cell)
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

    def get_next_cell(self):
        """ Returns the next cell to be visited, must be overridden. """
        pass
