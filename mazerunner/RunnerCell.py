import mazerunner.Config as Config
from mazerunner.GeneratorCell import GeneratorCell


class RunnerCell(GeneratorCell):
    """ Object representing a cell on the runner grid which inherits from the generator cell and adds properties to
    facilitate the search procedures. Each cell can only have walls on its lower or right edge and these are defined
    upon creation. Its x and y coordinates define where in the grid the cell resides. """

    def __init__(self, x, y, bottom, right, scene):
        GeneratorCell.__init__(self, x, y, scene)
        self.walls = {'bottom': bottom,
                      'right': right
                      }
        # Forward and backward variants of visited flag for bidirectional searches
        self.f_visited = False
        self.b_visited = False
        # The parent of the cell in a search tree
        self.parent = None
        self.f_parent = None
        self.b_parent = None
        # Whether the cell is part of the solution path, used for rendering
        self.solution = False
        # The cost of reaching this cell from the start cell
        self.cost = 0
        # Generate start and goal cell fills
        self.start = True if x == 0 and y == 0 else False
        self.goal = True if x == self.scene.get_columns() - 1 and y == self.scene.get_rows() - 1 else False
        if self.start or self.goal:
            self.generate_fill()

    def generate_fill(self):
        """ Sets the fill rectangle, pen and brush based on the cell's state. """
        del self.fill_rect[:]
        if self.solution:
            # Solution cell
            self.set_fill_rect(Config.CELL_END_PEN, Config.CELL_END_BRUSH)
        elif self.goal:
            # Goal cell
            self.set_fill_rect(Config.CELL_END_PEN, Config.CELL_END_BRUSH)
        elif self.start:
            # Start cell
            self.set_fill_rect(Config.CELL_START_PEN, Config.CELL_START_BRUSH)
        elif self.in_queue:
            # In queue
            self.set_fill_rect(Config.CELL_QUEUE_PEN, Config.CELL_QUEUE_BRUSH)
        elif self.visited:
            # Visited
            self.set_fill_rect(Config.CELL_VISITED_PEN, Config.CELL_VISITED_BRUSH)

    def reset(self):
        """ Reset the cell for a new search. """
        self.clear_visited()
        self.clear_parents()
        self.cost = 0
        self.set_in_queue(False)
        self.set_solution(False)

    def get_f_visited(self):
        """ Returns the cell's forward visited status. """
        return self.f_visited

    def set_f_visited(self, value=True):
        """ Sets forward visited to value (default True). """
        self.changed = True
        self.f_visited = value

    def get_b_visited(self):
        """ Returns the cell's backward visited status. """
        return self.b_visited

    def set_b_visited(self, value=True):
        """ Sets backward visited to value (default True). """
        self.changed = True
        self.b_visited = value

    def clear_visited(self):
        """ Set all visited status' to false. """
        self.changed = True
        self.visited = False
        self.f_visited = False
        self.b_visited = False

    def get_parent(self):
        """ Returns the cell's parent cell. """
        return self.parent

    def set_parent(self, parent):
        """ Sets the parent cell. """
        self.parent = parent

    def get_f_parent(self):
        """ Returns the cell's forward parent cell. """
        return self.f_parent

    def set_f_parent(self, parent):
        """ Sets the forward parent cell. """
        self.f_parent = parent

    def get_b_parent(self):
        """ Returns the cell's backward parent cell. """
        return self.b_parent

    def set_b_parent(self, parent):
        """ Sets the backward parent cell. """
        self.b_parent = parent

    def both_visited(self):
        """ Returns true if cell has been visited by both forward and backward search. """
        return self.f_visited and self.b_visited

    def clear_parents(self):
        """ Sets all parent cells to None. """
        self.parent = None
        self.f_parent = None
        self.b_parent = None

    def get_solution(self):
        """ Returns the cell's solution status. """
        return self.solution

    def set_solution(self, value=True):
        """ Sets solution status to value (default True). """
        self.changed = True
        self.solution = value

    def get_cost(self):
        """ Returns the heuristic cost. """
        return self.cost

    def set_cost(self, cost):
        """ Sets the heuristic cost. """
        self.cost = cost

    def set_start(self, value):
        """ Sets this cell as the starting cell. """
        self.start = value
        self.changed = True

    def set_goal(self, value):
        """ Sets this cell as the goal cell. """
        self.goal = value
        self.changed = True
