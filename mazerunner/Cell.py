from PyQt5.QtCore import QLineF, QRectF

import mazerunner.Config as Config


class Cell:
    """ Object representing a cell on the grid. Each cell starts with all four walls which are manipulated by the maze
    generation algorithm. The state of these walls """

    def __init__(self, x, y):
        # Coordinates of the cell
        self.x = x
        self.y = y
        # Whether the cell walls should be rendered
        self.walls = {
            'top': True,
            'right': True,
            'bottom': True,
            'left': True
        }
        # Whether or not the cell has been visited, f and b variants for bidirectional searches
        self.visited = False
        self.f_visited = False
        self.b_visited = False
        # The parent of the cell in a search tree
        self.parent = None
        self.f_parent = None
        self.b_parent = None
        # Whether the cell has been added to the queue, used for rendering
        self.queue = False
        # Whether the cell is part of the solution path, used for rendering
        self.solution = False
        # The cost of reaching this cell from the start cell
        self.cost = 0
        # Whether it has been changed since last render
        self.changed = False
        # The cell walls ordered top, right, bottom, left
        self.lines = []
        self.generate_lines()
        # Store reference to line objects in order to remove them later
        self.line_objects = []
        self.rect_object = None
        # The cell fill rect, pen and brush
        self.fill_display = []
        self.generate_fill()

    def get_x(self):
        """ Returns the cell's x coordinate """
        return self.x

    def get_y(self):
        """ Returns the cell's y coordinate """
        return self.y

    def get_walls(self):
        """ Returns the cell's walls """
        return self.walls

    def get_lines(self):
        """ Returns the cell's walls """
        self.generate_lines()
        return self.lines

    def get_visited(self):
        """ Returns the cell's visited status """
        return self.visited

    def get_f_visited(self):
        """ Returns the cell's forward visited status """
        return self.f_visited

    def get_b_visited(self):
        """ Returns the cell's backward visited status """
        return self.b_visited

    def get_solution(self):
        """ Returns the cell's solution status """
        return self.solution

    def get_queue(self):
        """ Returns the cell's queue status """
        return self.queue

    def get_parent(self):
        """ Returns the cell's parent cell """
        return self.parent

    def get_f_parent(self):
        """ Returns the cell's forward parent cell """
        return self.f_parent

    def get_b_parent(self):
        """ Returns the cell's backward parent cell """
        return self.b_parent

    def both_visited(self):
        """ Returns true if cell has been visited by both forward and backward search """
        return self.f_visited and self.b_visited

    def get_cost(self):
        """ Returns the cost """
        return self.cost

    def has_changed(self):
        """ Returns whether the cell has been changed since the last render. """
        return self.changed

    def get_wall_display(self):
        self.generate_lines()
        return self.lines

    def get_fill_display(self):
        self.generate_fill()
        return self.fill_display

    def clear_line_objects(self):
        del self.line_objects[:]

    def add_line_object(self, line):
        self.line_objects.append(line)

    def get_line_objects(self):
        return self.line_objects

    def set_rect_object(self, rect):
        self.rect_object = rect

    def get_rect_object(self):
        return self.rect_object

    def generate_lines(self):
        """ Populates the lines array with the cell walls defined by self.walls."""
        del self.lines[:]

        side_length = Config.CELL_DIMENSION
        xc = self.x * side_length  # x position of top left corner
        yc = self.y * side_length  # y position of top left corner

        """
        Due to the way the grid is initiated within the generator, every internal wall is doubled. That is a cell (3, 4)
        with a right wall would mean cell (4, 4) has a left wall. In order to remove these redundancies and ensure lines
        are not needlessly rendered twice, left and top walls are only returned for external walls, namely row and 
        column 0. For an (n x m) grid this saves 2(n-1)(m-1) lines from being rendered.
        """
        if self.y == 0:
            self.lines.append(QLineF(xc, yc, xc + side_length, yc))  # Top, only cells in the first row
        if self.walls.get('right'):
            self.lines.append(QLineF(xc + side_length, yc, xc + side_length, yc + side_length))  # Right
        if self.walls.get('bottom'):
            self.lines.append(QLineF(xc, yc + side_length, xc + side_length, yc + side_length))  # Bottom
        if self.x == 0:
            self.lines.append(QLineF(xc, yc, xc, yc + side_length))  # Left, only cells in the first column

    def generate_fill(self):
        """ Sets the fill rectangle, pen and brush based on the cell's state. """
        del self.fill_display[:]
        if self.solution:
            # Solution cell
            self.set_fill_display(Config.CELL_END_PEN, Config.CELL_END_BRUSH)
        elif self.x == Config.MAZE_COLUMNS - 1 and self.y == Config.MAZE_ROWS - 1:
            # Goal cell
            self.set_fill_display(Config.CELL_END_PEN, Config.CELL_END_BRUSH)
        elif self.get_x() == 0 and self.get_y() == 0:
            # Start cell
            self.set_fill_display(Config.CELL_START_PEN, Config.CELL_START_BRUSH)
        elif self.get_queue():
            # In queue
            self.set_fill_display(Config.CELL_QUEUE_PEN, Config.CELL_QUEUE_BRUSH)
        elif self.get_visited():
            # Visited
            self.set_fill_display(Config.CELL_VISITED_PEN, Config.CELL_VISITED_BRUSH)

    def set_fill_display(self, pen, brush):
        rect = QRectF(self.x * Config.CELL_DIMENSION + 1, self.y * Config.CELL_DIMENSION + 1,
                      Config.CELL_DIMENSION - 1, Config.CELL_DIMENSION - 1)
        self.fill_display = [rect, pen, brush]

    def reset(self):
        """ Reset the cell for a new search """
        self.clear_visited()
        self.clear_parents()
        self.cost = 0
        self.set_queue(False)
        self.set_solution(False)

    def set_wall(self, wall, value):
        """ Sets the render value for wall. Wall must be in {top, right, bottom, left} and value must be boolean """
        self.changed = True
        self.walls[wall] = value

    def set_visited(self, value=True):
        """ Sets visited to value (default True) """
        self.changed = True
        self.visited = value

    def set_f_visited(self, value=True):
        """ Sets forward visited to value (default True) """
        self.changed = True
        self.f_visited = value

    def set_b_visited(self, value=True):
        """ Sets backward visited to value (default True) """
        self.changed = True
        self.b_visited = value

    def clear_visited(self):
        """ Set all visited status' to false """
        self.changed = True
        self.visited = False
        self.f_visited = False
        self.b_visited = False

    def set_queue(self, value=True):
        """ Sets queue status to value (default True) """
        self.changed = True
        self.queue = value

    def set_solution(self, value=True):
        """ Sets solution status to value (default True) """
        self.changed = True
        self.solution = value

    def set_parent(self, parent):
        """ Sets the parent cell """
        self.parent = parent

    def set_f_parent(self, parent):
        """ Sets the forward parent cell """
        self.f_parent = parent

    def set_b_parent(self, parent):
        """ Sets the backward parent cell """
        self.b_parent = parent

    def clear_parents(self):
        """ Sets all parent cells to None """
        self.parent = None
        self.f_parent = None
        self.b_parent = None

    def set_cost(self, cost):
        """ Sets the cost """
        self.cost = cost

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    def __lt__(self, other):
        """ Override the less than comparator, this is used to fix priority queue breaking when two cells are the same
        distance from the goal. """
        return False


def get_index(x, y):
    """ Returns the array index for the cell at position (x, y). """
    return y * Config.MAZE_COLUMNS + x
