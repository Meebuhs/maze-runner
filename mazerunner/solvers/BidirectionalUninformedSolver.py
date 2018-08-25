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
        self.f_current_cell = self.runner.start_cell
        self.f_goal_cell = self.runner.goal_cell
        self.b_current_cell = self.runner.goal_cell
        self.b_goal_cell = self.runner.start_cell

    def start(self):
        """ Starts the solver."""
        self.initialise()
        self.run()

    def initialise(self):
        """ Initialises the start and goal cells for the search. """
        self.f_queue.append(self.f_current_cell)
        self.b_queue.append(self.b_current_cell)

    def run(self):
        """ Performs the Bidirectional Uninformed Search. The queue behaviour is defined by inheriting solvers. """
        while True:
            if not self.runner.running or self.runner.paused:
                break
            self.f_current_cell = self.get_next_cell(self.f_queue)
            self.b_current_cell = self.get_next_cell(self.b_queue)

            self.f_current_cell.f_visited = True
            self.f_current_cell.visited = True
            self.f_current_cell.in_queue = False

            self.b_current_cell.b_visited = True
            self.b_current_cell.visited = True
            self.b_current_cell.in_queue = False

            # If the two paths have overlapped, break the loop
            if self.f_current_cell.both_visited():
                self.construct_path(self.f_current_cell)
                break
            elif self.b_current_cell.both_visited():
                self.construct_path(self.b_current_cell)
                break
            else:
                for cell in self.runner.get_neighbours(self.f_current_cell):
                    if cell.f_parent is None:
                        self.f_queue.append(cell)
                        cell.f_parent = self.f_current_cell
                        cell.in_queue = True

                for cell in self.runner.get_neighbours(self.b_current_cell):
                    if cell.b_parent is None:
                        self.b_queue.append(cell)
                        cell.b_parent = self.b_current_cell
                        cell.in_queue = True

            self.runner.display.update_scene()

    def recommence(self):
        """ Recommence the search. """
        self.run()

    def construct_path(self, cell):
        """ Constructs the solution path by traversing the search tree which was constructed. Bidirectional search exits
        when the two search paths overlap, this method requires that the parameter cell is the cell at which this
        overlap occurs. """
        # From the middle, iterate through forward parents until the start cell is reached. The path is reversed after
        # being constructed to avoid the added complexity of prepending.
        new_cell = cell
        while not new_cell == self.b_goal_cell:
            new_cell.solution = True
            self.path.append(new_cell.f_parent)
            new_cell = new_cell.f_parent
        self.b_goal_cell.solution = True
        self.path.reverse()

        # Next add the overlapping cell and iterate through backward parents toward the goal. By appending cells here
        # the order of the path is maintained.
        new_cell = cell
        self.path.append(new_cell)
        while not new_cell == self.f_goal_cell:
            new_cell.solution = True
            self.path.append(new_cell.b_parent)
            new_cell = new_cell.b_parent
        self.f_goal_cell.solution = True
        print(self.path)
        self.runner.solved = True
        self.runner.running = False
        self.runner.display.update_scene(self.path)

    def get_next_cell(self, queue):
        """ Returns the next cell from the given queue, must be overridden by the class which inherits from this
        one. """
        pass
