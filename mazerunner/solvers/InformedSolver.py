from mazerunner.utils.PriorityQueue import PriorityQueue


class InformedSolver:
    """ Base class for an informed search. The fringe nodes are stored in a priority queue, sorted by an
    estimation of their cost. The function which defines how the cost is calculated is different for each solver. """

    def __init__(self, runner):
        self.runner = runner
        self.path = []
        self.queue = PriorityQueue()
        # Current and goal cells
        self.current_cell = self.runner.start_cell
        self.goal_cell = self.runner.goal_cell

    def start(self):
        """ Starts the solver."""
        self.initialise()
        self.run()

    def initialise(self):
        """ Initialises the start and goal cells for the search. """
        self.queue.put((self.calculate_cost(self.current_cell), self.current_cell))
        self.current_cell.cost = 0

    def run(self):
        """ Performs the informed search. The cost function f(c) is defined by inheriting solvers. """
        while True:
            if not self.runner.running or self.runner.paused:
                break
            self.current_cell = self.queue.get()[1]
            self.current_cell.visited = True
            self.current_cell.in_queue = False
            if self.current_cell == self.goal_cell:
                self.construct_path()
                break
            else:
                for cell in self.runner.get_neighbours(self.current_cell):
                    if cell.parent is None:
                        cell.parent = self.current_cell
                        # Cost to cell is ignored by greedy search
                        cell.cost = self.current_cell.cost + 1
                        self.queue.put((self.calculate_cost(cell), cell))
                        cell.in_queue = True
            self.runner.display.update_scene()

    def recommence(self):
        """ Recommence the search. """
        self.run()

    def construct_path(self):
        """ Constructs the solution path to the current cell by traversing the search tree which was constructed. """
        self.path.append(self.current_cell)
        cell = self.current_cell
        while not cell == self.runner.start_cell:
            cell.solution = True
            self.path.append(cell.parent)
            cell = cell.parent
        self.runner.start_cell.solution = True
        self.path.reverse()
        print(self.path)
        self.runner.solved = True
        self.runner.running = False
        self.runner.display.update_scene(self.path)

    def calculate_cost(self, cell):
        """ Returns the cost of the cell, must be overridden by inheriting solvers. """
        pass
