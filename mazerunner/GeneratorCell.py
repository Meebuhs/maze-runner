from PyQt5.QtCore import QLineF, QRectF

import mazerunner.Config as Config


class GeneratorCell:
    """ Object representing a cell on the generator grid. Each cell starts with walls on its lower or right edge and
    these are removed by the generation algorithm. Its x and y coordinates define where in the grid the cell resides.
    """

    def __init__(self, x, y):
        # Coordinates of the cell
        self.x = x
        self.y = y
        # Whether the cell walls should be rendered
        self.walls = {'bottom': True,
                      'right': True
                      }
        # Whether or not the cell has been visited
        self.visited = False
        # Whether the cell has been added to the queue, used for rendering
        self.queue = False
        # Whether it has been changed since last render
        self.changed = False
        # The cell walls
        self.lines = []
        self.generate_lines()
        # Store reference to line objects in order to remove them later
        self.line_objects = []
        self.rect_object = None
        # The cell fill rect, pen and brush
        self.fill_display = []

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

    def get_queue(self):
        """ Returns the cell's queue status """
        return self.queue

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

    def get_side_length(self):
        """ Returns the current side length. """
        return Config.GENERATOR_CELL_DIMENSION

    def generate_lines(self):
        """ Populates the lines array with the cell walls defined by self.walls."""
        del self.lines[:]

        side_length = self.get_side_length()
        xc = self.x * side_length  # x position of top left corner
        yc = self.y * side_length  # y position of top left corner

        """
        Due to the way the cells are created, each cell can only have a bottom or right wall to ensure internal walls 
        are not duplicated. That is a cell (3, 4) with a right wall would mean cell (4, 4) has a left wall. Thus to
        complete the grid, left and top walls are also returned for external walls, namely row and 
        column 0. For an (n x m) grid this saves 2(n-1)(m-1) lines from being rendered.
        """

        if self.walls.get('bottom'):
            self.lines.append(QLineF(xc, yc + side_length, xc + side_length, yc + side_length))  # Bottom
        if self.walls.get('right'):
            self.lines.append(QLineF(xc + side_length, yc, xc + side_length, yc + side_length))  # Right
        if self.y == 0:
            self.lines.append(QLineF(xc, yc, xc + side_length, yc))  # Top, only cells in the first row
        if self.x == 0:
            self.lines.append(QLineF(xc, yc, xc, yc + side_length))  # Left, only cells in the first column

    def generate_fill(self):
        """ Sets the fill rectangle, pen and brush based on the cell's state. """
        del self.fill_display[:]
        if self.get_queue():
            # In queue
            self.set_fill_display(Config.CELL_QUEUE_PEN, Config.CELL_QUEUE_BRUSH)
        elif self.get_visited():
            # Visited
            self.set_fill_display(Config.CELL_VISITED_PEN, Config.CELL_VISITED_BRUSH)

    def set_fill_display(self, pen, brush):
        side_length = self.get_side_length()
        rect = QRectF(self.x * side_length + 1, self.y * side_length + 1, side_length - 1, side_length - 1)
        self.fill_display = [rect, pen, brush]

    def set_wall(self, wall, value):
        """ Sets the render value for wall. Wall must be in {bottom, right} and value must be boolean """
        self.changed = True
        self.walls[wall] = value

    def set_visited(self, value=True):
        """ Sets visited to value (default True) """
        self.changed = True
        self.visited = value

    def set_queue(self, value=True):
        """ Sets queue status to value (default True) """
        self.changed = True
        self.queue = value

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    def __lt__(self, other):
        """ Override the less than comparator, this is used to fix priority queue breaking when two cells are the same
        distance from the goal. """
        return False


def get_index(x, y):
    """ Returns the array index for the cell at position (x, y) in the maze generator. """
    return y * Config.GENERATOR_MAZE_COLUMNS + x
