class UninformedSolver:
    """ Base class for solvers which perform a search without calculating any heuristic costs. """

    def __init__(self, runner):
        self.runner = runner
        self.path = []
        self.queue = []
        # Current and goal cells
        self.current_cell = self.runner.start_cell
        self.goal_cell = self.runner.goal_cell

    def start(self):
        """ Starts the solver."""
        self.initialise()
        self.run()

    def initialise(self):
        """ Initialises the start and goal cells for the search. """
        self.queue.append(self.current_cell)

    def run(self):
        """ Performs an uninformed search. The queue behaviour is defined by solvers which inherit from this one. """
        while True:
            if not self.runner.get_running() or self.runner.get_paused():
                break
            self.current_cell = self.get_next_cell()
            self.current_cell.set_visited()
            self.current_cell.set_in_queue(False)
            if self.current_cell == self.goal_cell:
                self.construct_path()
                break
            else:
                for cell in self.runner.get_neighbours(self.current_cell):
                    if cell.get_parent() is None:
                        self.queue.append(cell)
                        cell.set_parent(self.current_cell)
                        cell.set_in_queue()
            self.runner.display.update_scene()

    def recommence(self):
        """ Recommence the search. """
        self.run()

    def construct_path(self):
        """ Constructs the solution path to the current cell by traversing the search tree which was constructed. """
        cell = self.current_cell
        self.path.append(cell)
        while not cell == self.runner.start_cell:
            cell.set_solution()
            self.path.append(cell.get_parent())
            cell = cell.get_parent()
        self.runner.start_cell.set_solution()
        self.path.reverse()
        print(self.path)
        self.runner.solved = True
        self.runner.running = False
        self.runner.display.update_scene(self.path)

    def get_path(self):
        """ Returns the solution path. If the solver has not yet been run, the path returned is an empty array. """
        return self.path

    def get_next_cell(self):
        """ Returns the next cell to be visited, must be overridden. """
        pass
