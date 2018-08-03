import mazerunner.Config as Config
from mazerunner.Cell import Cell, get_index


class BidirectionalUninformedSolver:
    """ Solver which implements a Bidirectional Uninformed Search. One search commences forward from the start cell
    and the other backwards from the goal. The search terminates when a cell has been visited by both the forward and
    backward search. """

    def __init__(self, runner):
        self.runner = runner
        self.path = []
        self.f_queue = []
        self.b_queue = []
        # Current and goal cells for forward and backward searches
        # The cells assigned here are discarded once search is commenced
        self.f_current_cell = Cell(0, 0)
        self.f_goal_cell = Cell(0, 0)
        self.b_current_cell = Cell(0, 0)
        self.b_goal_cell = Cell(0, 0)

    def run(self):
        """ Performs the Bidirectional Uninformed Search. The queue behaviour is defined by inheriting solvers. """
        self.f_queue.append(self.runner.cells[0])
        self.b_queue.append(self.runner.cells[get_index(Config.MAZE_COLUMNS - 1, Config.MAZE_ROWS - 1)])
        self.f_goal_cell = self.b_queue[0]
        self.b_goal_cell = self.f_queue[0]
        while True:
            if not Config.get_runner_running():
                break
            self.f_current_cell = self.get_next_cell(self.f_queue)
            self.b_current_cell = self.get_next_cell(self.b_queue)

            self.f_current_cell.set_f_visited()
            self.f_current_cell.set_visited()
            self.f_current_cell.set_queue(False)

            self.b_current_cell.set_visited()
            self.b_current_cell.set_b_visited()
            self.b_current_cell.set_queue(False)

            # If the two paths have overlapped, break the loop
            if self.f_current_cell.both_visited():
                self.construct_path(self.f_current_cell)
                break
            elif self.b_current_cell.both_visited():
                self.construct_path(self.b_current_cell)
                break
            else:
                for cell in self.runner.get_neighbours(self.f_current_cell):
                    if cell.get_f_parent() is None:
                        self.f_queue.append(cell)
                        cell.set_f_parent(self.f_current_cell)
                        cell.set_queue()

                for cell in self.runner.get_neighbours(self.b_current_cell):
                    if cell.get_b_parent() is None:
                        self.b_queue.append(cell)
                        cell.set_b_parent(self.b_current_cell)
                        cell.set_queue()
            self.runner.display.update_scene()

    def construct_path(self, cell):
        """ Constructs the solution path by traversing the search tree which was constructed. Bidirectional search exits
        when the two search paths overlap, this method requires that the parameter cell is the cell at which this
        overlap occurs. """
        # From the middle, iterate through forward parents until the start cell is reached. The path is reversed after
        # being constructed to avoid the added complexity of prepending.
        new_cell = cell
        while not new_cell == self.b_goal_cell:
            new_cell.set_solution()
            self.path.append(new_cell.get_f_parent())
            new_cell = new_cell.get_f_parent()
        self.b_goal_cell.set_solution()
        self.path.reverse()

        # Next add the overlapping cell and iterate through backward parents toward the goal. By appending cells here
        # the order of the path is maintained.
        new_cell = cell
        self.path.append(new_cell)
        while not new_cell == self.f_goal_cell:
            new_cell.set_solution()
            self.path.append(new_cell.get_b_parent())
            new_cell = new_cell.get_b_parent()
        self.f_goal_cell.set_solution()
        print(self.path)
        self.runner.solved = True
        self.runner.display.update_scene(self.path)

    def get_path(self):
        """ Returns the solution path. If the solver has not yet been run, the path returned is an empty array. """
        return self.path

    def get_next_cell(self, queue):
        """ Returns the next cell from the given queue, must be overridden by the class which inherits from this
        one. """
        pass