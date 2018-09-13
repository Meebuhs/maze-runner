import mazerunner.utils.Config as Config
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
        self._f_visited = False
        self._b_visited = False
        # The parent of the cell in a search tree
        self.parent = None
        self.f_parent = None
        self.b_parent = None
        # Whether the cell is part of the solution path, used for rendering
        self._solution = False
        # The cost of reaching this cell from the start cell
        self.cost = 0
        # Generate start and goal cell fills
        self._start = True if x == 0 and y == 0 else False
        self._goal = True if x == self.scene.columns - 1 and y == self.scene.rows - 1 else False
        if self._start or self._goal:
            self.generate_fill()

    def generate_fill(self):
        """ Sets the fill rectangle, pen and brush based on the cell's state. """
        del self.fill_rect[:]
        if self._solution:
            # Solution cell
            self.set_fill_rect(Config.CELL_END_PEN, Config.CELL_END_BRUSH)
        elif self._goal:
            # Goal cell
            self.set_fill_rect(Config.CELL_END_PEN, Config.CELL_END_BRUSH)
        elif self._start:
            # Start cell
            self.set_fill_rect(Config.CELL_START_PEN, Config.CELL_START_BRUSH)
        elif self._in_queue:
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
        self._in_queue = False
        self._solution = False

    @property
    def f_visited(self):
        """ Returns the forward visited status of this cell. """
        return self._f_visited

    @f_visited.setter
    def f_visited(self, value):
        """ Sets forward visited to value. """
        self._f_visited = value
        self.changed = True

    @property
    def b_visited(self):
        """ Returns the backward visited status of this cell. """
        return self._b_visited

    @b_visited.setter
    def b_visited(self, value):
        """ Sets backward visited to value. """
        self._b_visited = value
        self.changed = True

    def clear_visited(self):
        """ Set all visited status' to false. """
        self.changed = True
        self._visited = False
        self._f_visited = False
        self._b_visited = False

    def both_visited(self):
        """ Returns true if cell has been visited by both forward and backward search. """
        return self._f_visited and self._b_visited

    def clear_parents(self):
        """ Sets all parent cells to None. """
        self.parent = None
        self.f_parent = None
        self.b_parent = None

    @property
    def solution(self):
        """ Returns whether this cell is part of the solution. """
        return self._solution

    @solution.setter
    def solution(self, value):
        """ Sets solution status to value. """
        self._solution = value
        self.changed = True

    @property
    def start(self):
        """ Returns whether this cell is the starting cell. """
        return self._start

    @start.setter
    def start(self, value):
        """ Sets this cell as the starting cell. """
        self._start = value
        self.changed = True

    @property
    def goal(self):
        """ Returns whether this cell is the goal cell. """
        return self._goal

    @goal.setter
    def goal(self, value):
        """ Sets this cell as the goal cell. """
        self._goal = value
        self.changed = True
