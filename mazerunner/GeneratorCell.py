from PyQt5.QtCore import QLineF, QRectF

import mazerunner.Config as Config


class GeneratorCell:
    """ Object representing a cell on the generator grid. Each cell starts with walls on its lower or right edge and
    these are removed by the generation algorithm. Its x and y coordinates define where in the grid the cell resides.
    """

    def __init__(self, x, y, scene):
        # Coordinates of the cell
        self.x = x
        self.y = y
        # The parent scene which contains this cell
        self.scene = scene
        # Whether the cell walls should be rendered
        self.walls = {'bottom': True,
                      'right': True
                      }
        # Whether or not the cell has been visited
        self._visited = False
        # Whether the cell has been added to the queue, used for rendering
        self._in_queue = False
        # Whether it has been changed since last render
        self.changed = False
        # The cell walls
        self._lines = []
        self.generate_lines()
        # Store reference to line objects in order to remove them later
        self.line_items = []
        # The cell fill rect, pen and brush
        self.fill_rect = []
        self.rect_item = None

    def generate_lines(self):
        """ Populates the lines array with the cell walls defined by self.walls."""
        del self._lines[:]

        side_length = self.scene.cell_dimension
        xc = self.x * side_length  # x position of top left corner
        yc = self.y * side_length  # y position of top left corner

        """
        Due to the way the cells are created, each cell can only have a bottom or right wall to ensure internal walls 
        are not duplicated. That is a cell (3, 4) with a right wall would mean cell (4, 4) has a left wall. Thus to
        complete the grid, left and top walls are also returned for external walls, namely row and 
        column 0. For an (n x m) grid this saves 2(n-1)(m-1) lines from being rendered.
        """

        if self.walls.get('bottom'):
            self._lines.append(QLineF(xc, yc + side_length, xc + side_length, yc + side_length))  # Bottom
        if self.walls.get('right'):
            self._lines.append(QLineF(xc + side_length, yc, xc + side_length, yc + side_length))  # Right
        if self.y == 0:
            self._lines.append(QLineF(xc, yc, xc + side_length, yc))  # Top, only cells in the first row
        if self.x == 0:
            self._lines.append(QLineF(xc, yc, xc, yc + side_length))  # Left, only cells in the first column

    def generate_fill(self):
        """ Sets the fill rectangle, pen and brush based on the cell's state. """
        del self.fill_rect[:]
        if self._in_queue:
            # In queue
            self.set_fill_rect(Config.CELL_QUEUE_PEN, Config.CELL_QUEUE_BRUSH)
        elif self._visited:
            # Visited
            self.set_fill_rect(Config.CELL_VISITED_PEN, Config.CELL_VISITED_BRUSH)

    def get_fill_rect(self):
        """ Returns a QRect which defines the cell's colour based on its current status. """
        self.generate_fill()
        return self.fill_rect

    def set_fill_rect(self, pen, brush):
        """ Creates a rect to fill the cell with the given pen and brush and sets it as the fill_rect. """
        side_length = self.scene.cell_dimension
        rect = QRectF(self.x * side_length + 1, self.y * side_length + 1, side_length - 1, side_length - 1)
        self.fill_rect = [rect, pen, brush]

    def set_wall(self, wall, value):
        """ Sets the render value for wall. Wall must be in {bottom, right} and value must be boolean. """
        self.walls[wall] = value
        self.changed = True

    @property
    def visited(self):
        """ Returns the visited status of this cell. """
        return self._visited

    @visited.setter
    def visited(self, value):
        """ Sets the visited status to value. """
        self._visited = value
        self.changed = True

    @property
    def in_queue(self):
        """ Returns the queue status of this cell. """
        return self._in_queue

    @in_queue.setter
    def in_queue(self, value):
        """ Sets queue status to value. """
        self._in_queue = value
        self.changed = True

    @property
    def lines(self):
        """ Returns the line's to render the cell's walls. """
        self.generate_lines()
        return self._lines

    def add_line_item(self, line):
        """ Stores a QGraphicsLineItem. These are generated by QGraphicsScene.addLine and a reference must be stored in
        order to remove it from the scene. """
        self.line_items.append(line)

    def clear_line_items(self):
        """ Clears the stored QGraphicsLineItems. """
        del self.line_items[:]

    def __repr__(self):
        """ Override the string representation. """
        return "({}, {})".format(self.x, self.y)

    def __lt__(self, other):
        """ Override the less than comparator with an arbitrary result, this is used to fix priority queue breaking
        when two cells are the same distance from the goal. """
        return False
